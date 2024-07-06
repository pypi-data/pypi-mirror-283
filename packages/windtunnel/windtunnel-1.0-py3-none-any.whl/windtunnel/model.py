from datetime import datetime, timedelta
from typing import List, TypedDict, Union, Tuple, cast, Literal, Dict
from types import SimpleNamespace
from dataclasses import dataclass, field, asdict
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from errors import NotFoundError, AuthenticationError, TokenDisplayError, EnvDataError
from helpers import as_DataFrame, hhmm_string_to_datetime, check_time_str, get_slot_type, get_booked_duration
import pytz
import browser_cookie3
import requests
import re
import pandas
import copy
import os
import csv

# Gets env data
load_dotenv()

@dataclass
class Tunn3lAuthDict(TypedDict):
  day: str
  domain: str
  tunn3l_token: str
  tunn3l_cookie: str

@dataclass
class WorkingRangeDict(TypedDict):
  first_slot: datetime
  last_slot: datetime

@dataclass
class WorkingRange:
  """
    Represents one working range for an employee. An employee has a list
    of working ranges for the day (at least one, may have several)
  """
  first_slot: datetime
  last_slot: datetime

  @property
  def as_dict(self) -> WorkingRangeDict:
    return WorkingRangeDict(**asdict(self))

@dataclass
class EmployeeDict(TypedDict):
  name:str
  working_ranges: List[WorkingRangeDict]

@dataclass
class Employee:
  """ Employees are not detached persons from tunn3l's planning """
  # Instance variables
  name: str
  working_ranges: List[WorkingRange] = field(default_factory=list)

  @property
  def as_dict(self) -> EmployeeDict:
    return EmployeeDict(**asdict(self))

@dataclass
class StaffDict(TypedDict):
  name:str
  working_ranges: List[WorkingRangeDict]
  drive: float
  briefing: float
  instructor: float
  doorman: float
  total: float

@dataclass
class Staff(Employee):
  """ Represents the employees that are instructor and can be add to the daily shift """
  drive: float = round(0,1)
  briefing: float = round(0,1)
  instructor: float = round(0,1)
  doorman: float = round(0,1)
  total: float = round(0,1)
  should_run:bool = False

  @property
  def as_dict(self) -> StaffDict:
    staff_dict: Dict = {k:v for k,v in asdict(self).items() if k!="should_run"}
    return StaffDict(**staff_dict)

  def __post_init__(self):
    super().__init__(self.name, self.working_ranges)

  def increment_role(self, role:str, add:float) -> None:
    """ Increments by 1 the given role and total counters """
    role_count = getattr(self, role) + add
    setattr(self, role, role_count)
    self.total += add

    return None

@dataclass
class Available():
  name: str
  should_run: bool = False


@dataclass
class Annotation():
  position: Literal["before","after"]
  value: str

@dataclass
class TimeslotDict(TypedDict):
  time_: datetime
  type_: str
  has_handifly: bool
  booked: float
  drive: str
  briefing: str
  instructor: str
  doorman: str


@dataclass
class Timeslot():
  time_: datetime
  type_: str
  has_handifly: bool = False
  booked: float = round(0, 1) # 0.0
  planning: List[str] = field(default_factory=list) # full list of staff on shift for that slot
  available: List[Available] = field(default_factory=list) # on the fly list of available staff (once added to shift they are removed)
  drive: str = ""
  briefing: str = ""
  instructor: str = ""
  doorman: str = ""

  @property
  def as_dict(self) -> TimeslotDict:
    timeslot_dict: Dict = {k:v for k,v in asdict(self).items() if k not in ["planning", "available"]}
    return TimeslotDict(**timeslot_dict)

  def set_role(self, staff:Staff|None, role:str, annotations:List[Annotation]|None) -> None:
    """ Sets the given staff's name into the appropriate role with the given annotations """

    if annotations is not None:
      text_annotations = copy.deepcopy(annotations)
    else :
      text_annotations:List[Annotation] = []

    # If staff is flagged as "should run", we add the appropriate annotation
    if staff and staff.should_run == True:
      text_annotations.append(Annotation("before",">>"))

    staff_infos: str = staff.name if staff is not None else "OUCH!"


    if text_annotations is not None and len(text_annotations) > 0:
      annotations_before: str = f"{''.join([ann.value for ann in text_annotations if ann.position=="before"])} "
      annotations_before: str = annotations_before if annotations_before!="() " else ""

      annotations_after: str = f" ({''.join([ann.value for ann in text_annotations if ann.position=="after"])})"
      annotations_after: str = annotations_after if annotations_after!=" ()" else ""

      staff_infos = f"{annotations_before}{staff_infos}{annotations_after}".strip()

    setattr(self, role, staff_infos)

    return None


@dataclass
class Model:
  """ MVC system's model """
  # Instance's variables
  APP_INPUTS: SimpleNamespace = field(default_factory=lambda: copy.deepcopy(
    SimpleNamespace(
      DAY="",
      DOMAIN="",
      TUNN3L_TOKEN="",
      TUNN3L_COOKIE="",
    )
  ))

  employees: List[Employee] = field(default_factory=list)
  staffs: List[Staff] = field(default_factory=list)
  staffs_temp: List[Staff] = field(default_factory=list)
  slots: List[Timeslot] = field(default_factory=list)

  @property
  def employees_df(self) -> pandas.DataFrame:
    # Returns employees list as a pandas DataFrame
    return as_DataFrame(self.employees)

  @property
  def employees_dicts(self) -> List[EmployeeDict]:
    # Returns employees list as a list of dictionnaries
    return [e.as_dict for e in self.employees]

  @property
  def staffs_df(self) -> pandas.DataFrame:
    # Returns staffs list as a pandas DataFrame
    return as_DataFrame(self.staffs)

  @property
  def staffs_dicts(self) -> List[StaffDict]:
    # Returns staffs list as a list of dictionnaries
    return [s.as_dict for s in self.staffs]

  @property
  def slots_dicts(self) -> List[TimeslotDict]:
    # Returns slot list as a list of dictionnaries
    return [s.as_dict for s in self.slots]

  @property
  def day_(self) -> str:
    return self.APP_INPUTS.DAY.replace("-","_")

  @property
  def daily_agenda_url(self) -> str:
    return f"https://back.{self.APP_INPUTS.DOMAIN}.com/index.php?ctrl=page&page=backoffice-daily&token={self.APP_INPUTS.TUNN3L_TOKEN}&time={self.day_}"

  # PRIVATE METHODS
  def set_day(self, day_str:str|None) -> None:
    """ Gets day in env data and checks validity """
    try:
      # Gets day from env file
      env_day: str = cast(str, day_str)
      input_day = re.sub(r"\D", "-", env_day)
      # Tries datetimte conversion as type test
      datetime.strptime(input_day, "%Y-%m-%d")
      self.APP_INPUTS.DAY = env_day
    except ValueError:
      raise EnvDataError(f"Please type a date in yyy-m-d format, here is the day you provided: {day_str}")

    return None
  def set_tunn3l_domain(self, domain:str|None) -> None:
    # Gets tunn3l's domain as it is
    if domain is not None:
      self.APP_INPUTS.DOMAIN = domain
    else:
      raise EnvDataError(f"You must provide a domain as in https://back.[domain].com.\nHere is the one you provided: {domain}")
    return None
  def set_tunn3l_token(self, token:str|None) -> None:
    # Checks given token
    if token is not None and re.match(r'^[a-z0-9]{30,50}$', token):
      self.APP_INPUTS.TUNN3L_TOKEN = token
    else:
      raise EnvDataError(f"This does not look like a token, it should be between 30 and 50 alphanumeric lower caracters only.\nHere is an example: a6ef279598cb4c0c2b94j328dde3a84275eabd47\nYou wll find your token Desk>Boooking-agenda, click on the setting wheels close to 'daily planning'.\nHere is the token you provided: {token}")
    return None
  def set_tunn3l_cookie(self, cookie:str|None) -> None:
    # Checks given cookie
    if cookie is not None and re.match(r'^[a-z0-9]{25,30}$', cookie):
      self.APP_INPUTS.TUNN3L_COOKIE = cookie
    else:
      raise EnvDataError(f"This does not look like a tunn3l cookie, it should be between 25 and 30 alphanumeric lower caracters only.\nHere is an example: 1if0b4pma72nl01ach8b2ael8k\nYou wll find your cookie in the dev section of your browser, in the list of cookies, copy the value of the Tunn3l cookie.\nHere is the cookie you provided: {cookie}")
    return None

  def _get_tunn3l_auth_from_env(self) -> None:
    """ Gets env data for tunn3l authentification """
    self.set_day(os.getenv("DAY"))
    self.set_tunn3l_domain(os.getenv("DOMAIN"))
    self.set_tunn3l_token(os.getenv("TUNN3L_TOKEN"))
    self.set_tunn3l_cookie(os.getenv("TUNN3L_COOKIE"))

    return None

  def _find_staff(self, seek_staff:Staff) -> Staff | None:
    """ Returns staff reference from staff list """
    return next((staff for staff in self.staffs if staff.name == seek_staff.name), None)

  def _find_staff_temp(self, seek_staff:Staff) -> Staff | None:
    """ Returns staff reference from temporary staff list """
    return next((staff for staff in self.staffs_temp if staff.name == seek_staff.name), None)

  def _find_staff_from_name(self, seek_name:str) -> Staff:
    """ Returns staff reference in self.staffs from his name"""
    return next((staff for staff in self.staffs if staff.name == seek_name))

  def _copy_staff_from_name(self, seek_name:str) -> Staff:
    """ Returns copy of staff from his name """
    copied_staff = copy.deepcopy(next((staff for staff in self.staffs if staff.name == seek_name)))
    copied_staff.drive = 0
    copied_staff.briefing = 0
    copied_staff.instructor = 0
    copied_staff.doorman = 0
    copied_staff.total = 0
    copied_staff.should_run = False
    return copied_staff

  def _get_less_of(self, role:str, slot:Timeslot, i:int) -> Staff | None:
    """
      Returns the staff with the less number of the given role then less
      total from temporary staff list first for not running staff. In case of a tie,
      we do the same at the global daily level. If no one is available, we
      do the same among he staff that must run.
    """
    selected_staff: Staff | None = None

    # Copies should_run info from availables to self.staffs_temp
    for staff in self.staffs_temp:
      for available in slot.available:
        if available.name == staff.name:
          staff.should_run = available.should_run

    # FIRST WE CHECK AMONG NOT RUNNING AVAILABLE STAFFS

    # Filters staff table on available staff only
    available_temp: List[str] =  [staff.name for staff in slot.available if staff.should_run == False]

    # For briefing, instructor must also be available in next slot
    if role == "briefing":
      next_availables: List[str] = [staff.name for staff in self.slots[i+1].available if staff.should_run == False]
      overall_availables: List[str] = list(set(available_temp) & set(next_availables))
    else:
      overall_availables = available_temp
    available_staffs: List[Staff] = [staff for staff in self.staffs_temp if staff.name in overall_availables]

    # Sorts staff by role then total
    sorted_staffs: List[Staff] = sorted(available_staffs, key= lambda staff: (getattr(staff, role), staff.total))

    # If only one staff is found we select it
    if len(sorted_staffs) == 1:
      selected_staff = sorted_staffs[0]

    elif len(sorted_staffs) > 1:
      lowest_score: int = getattr(sorted_staffs[0], role)
      lowest_score_staffs = [staff for staff in sorted_staffs if getattr(staff, role)==lowest_score]

      lowest_total = min(staff.total for staff in lowest_score_staffs)
      lowest_staffs = [staff for staff in lowest_score_staffs if staff.total==lowest_total]

      # If only one staff is found we select it
      if len(lowest_staffs) == 1:
        selected_staff = copy.deepcopy(lowest_staffs[0])
        selected_staff.should_run = False
      # If we found several staff, there is a tie, we do the same at the daily global level
      else:
        available_staffs = [staff for staff in self.staffs if staff.name in overall_availables]
        sorted_staffs = sorted(available_staffs, key= lambda staff: (getattr(staff, role), staff.total))
        if len(sorted_staffs) > 0:
          selected_staff = copy.deepcopy(sorted_staffs[0])
          selected_staff.should_run = False

    # THEN WE CHECK AMONG SHOULD RUN AVAILABLE STAFFS
    else:
      # Filters staff table on available staff only
      available_temp =  [staff.name for staff in slot.available if staff.should_run == True]

      # For briefing, instructor must also be available in next slot
      if role == "briefing":
        next_availables: List[str] = [staff.name for staff in self.slots[i+1].available if staff.should_run == False]
        overall_availables: List[str] = list(set(available_temp) & set(next_availables))
      else:
        overall_availables = available_temp
      available_staffs: List[Staff] = [staff for staff in self.staffs_temp if staff.name in overall_availables]

      # Sorts staff by role then total
      sorted_staffs: List[Staff] = sorted(available_staffs, key= lambda staff: (getattr(staff, role), staff.total))

      # If none is available we return None
      if len(sorted_staffs) == 1:
        selected_staff = sorted_staffs[0]

      elif len(sorted_staffs) > 1:
        lowest_score: int = getattr(sorted_staffs[0], role)
        lowest_score_staffs = [staff for staff in sorted_staffs if getattr(staff, role)==lowest_score]

        lowest_total = min(staff.total for staff in lowest_score_staffs)
        lowest_staffs = [staff for staff in lowest_score_staffs if staff.total==lowest_total]

        # If only one staff is found we return him
        if len(lowest_staffs) == 1:
          selected_staff = copy.deepcopy(lowest_staffs[0])
          selected_staff.should_run = True
        # If we found several staff, there is a tie, we do the same at the daily global level
        else:
          available_staffs = [staff for staff in self.staffs if staff.name in overall_availables]
          sorted_staffs = sorted(available_staffs, key= lambda staff: (getattr(staff, role), staff.total))
          if len(sorted_staffs) > 0:
            selected_staff = copy.deepcopy(sorted_staffs[0])
            selected_staff.should_run = True

    return selected_staff

  def _increment_staff(self, seek_staff:Staff|None, role:str, add:float) -> None:
    """ Increments staff in both global and temporary counters """
    if seek_staff is not None:
      # Finds and increment staff in global list
      staff = cast(Staff, self._find_staff(seek_staff))
      staff.increment_role(role, add=add)

      # Finds and increment staff in temporary list
      staff = cast(Staff, self._find_staff_temp(seek_staff))
      staff.increment_role(role, add=add)
    return None

  # PUBLIC METHODS
  def set_tunn3l_auth(self, auth_data: Dict):
    self.APP_INPUTS.DAY = auth_data["day"]
    self.APP_INPUTS.DOMAIN = auth_data["day"]
    self.APP_INPUTS.DAY = auth_data["day"]
    self.APP_INPUTS.DAY = auth_data["day"]
    return 0

  def set_daily_employees_from_tunn3l(self) -> None:
    """ Sets into model the list of daily employees from tunn3l's bacoffice planning """

    def __convert_to_utc_timestamp(date_str: str) -> int:
      """
        Returns the given date string converted as a timestamp integer.
        Since Tunn3l system is in UTC, it adds 00:00:00 to the day then
        applies the local timezone before to convert it to uts timestamp
      """
      local_time = datetime.strptime(date_str, "%Y-%m-%d")
      local_time = local_time.replace(hour=0, minute=0, second=0)
      utc_time = local_time.astimezone(pytz.utc)
      utc_timestamp = int(utc_time.timestamp())

      return utc_timestamp

    def __get_cookie_value(cookie_jar) -> str | None:
      """ Returns tunn3l's cookie if found in cookie jar else returns None """
      name = "Tunn3l"
      domain = f"back.{self.APP_INPUTS.DOMAIN}.com"

      for cookie in cookie_jar:
        if cookie.name == name and domain in cookie.domain:
          return cookie.value

      return None

    def __check_cookie_in_browsers() -> Union[Tuple[str, str], Tuple[None, None]]:
      """ Returns browser name and cookie value if found, else returns None """
      browsers = {
        'Chrome': browser_cookie3.chrome,
        'Firefox': browser_cookie3.firefox,
        'Opera': browser_cookie3.opera,
        'Edge': browser_cookie3.edge,
        'Safari': browser_cookie3.safari,
        'Chromium': browser_cookie3.chromium,
        'Brave': browser_cookie3.brave,
        'Vivaldi': browser_cookie3.vivaldi
      }

      for browser_name, browser_func in browsers.items():
        try:
          cookies = browser_func()
          cookie_value = __get_cookie_value(cookies)
          if cookie_value:
            return browser_name, cookie_value
        except Exception as e:
          print(f"{browser_name}: {e}")

      return None, None

    def __getAttrs(element) -> str:
      """ Returns full tag with attribute """
      tag_name = element.name
      attrs = ' '.join([f'{key}="{value}"' for key, value in element.attrs.items()])
      opening_tag = f'<{tag_name} {attrs}>'
      return opening_tag

    def __convert_timestamp_to_hhmm_string(timestamp: str) -> str:
      """ Returns the given timestamp as date string hh:mm """
      utc_time = datetime.fromtimestamp(int(timestamp))
      time_string = utc_time.strftime('%H:%M')
      return time_string

    def __get_working_ranges(timestamp_strings: List[str]) -> List[WorkingRange]:
      """ Returns working hour ranges from planning """

      def timestamp_string_string_to_datetime(timestamp_str: str) -> datetime:
        """ Returns the datetime of the given timestamp string """
        time_str =  __convert_timestamp_to_hhmm_string(timestamp_str)
        return datetime.strptime(time_str, '%H:%M')

      def datetime_to_time_string(dt:datetime) -> str:
        """ Returns the time as string of the given datetime """
        return dt.strftime('%H:%M')

      working_ranges: List[WorkingRange] = []
      if not timestamp_strings:
        return working_ranges

      start_time = timestamp_string_string_to_datetime(timestamp_strings[0])
      previous_time = start_time

      for i in range(1, len(timestamp_strings)):
        current_time = timestamp_string_string_to_datetime(timestamp_strings[i])
        # Vérifier si l'écart est supérieur à 15 minutes
        if current_time - previous_time > timedelta(minutes=15):
          # Ajouter le créneau actuel à la liste
          end_time = previous_time + timedelta(minutes=15)
          last_slot = end_time - timedelta(minutes=30)
          working_ranges.append(WorkingRange(start_time, last_slot))
          # Commencer un nouveau créneau
          start_time = current_time
        previous_time = current_time

      # Ajouter le dernier créneau
      end_time = previous_time + timedelta(minutes=15)
      last_slot = end_time - timedelta(minutes=30)
      working_ranges.append(WorkingRange(start_time, last_slot))

      return working_ranges

    timestamp = __convert_to_utc_timestamp(self.APP_INPUTS.DAY)

    # Checks for Tunn3l's cookie in major browsers if cookie is not providen by user
    if self.APP_INPUTS.TUNN3L_COOKIE == "":
      browser_name, cookie_value = __check_cookie_in_browsers()
      if cookie_value:
        print(f"Cookie found in {browser_name}: {cookie_value}")
        self.APP_INPUTS.TUNN3L_COOKIE = cookie_value
      else:
        print(f"Cookie not found in major browsers")

    # Builds tunn3l's url and header
    cookies = { "Tunn3l": f"{self.APP_INPUTS.TUNN3L_COOKIE}" }
    planning_url = f"https://back.{self.APP_INPUTS.DOMAIN}.com/backoffice-staff-schedule_{self.APP_INPUTS.DAY}"

    # Gets tunn3l's planning page
    try:
      planning_page = requests.get(planning_url, cookies=cookies)
      planning = BeautifulSoup(planning_page.content, "html.parser")
    except:
      raise NotFoundError(f"Site not found while accessing planning.\nPlease check the url: {planning_url}")

    # Checks authentification with the providen cookie
    title = planning.title
    if title is not None:
      if "Authentification" in title.text:
        raise AuthenticationError(f"Authentification failed while accessing the planning.\nPlease update the tunn3l cookie value: {cookies}")

    # Browses html page until day div
    main_div = planning.find("div", id="main")
    del planning
    container_div = main_div.find("div", class_="container-fluid") # type: ignore
    del main_div
    section_divs = container_div.findAll("div", class_="row", recursive=False) # type: ignore
    del container_div
    schedule_div = section_divs[2]
    del section_divs
    day_divs = schedule_div.findAll("div", class_="staff-schedule-day")
    del schedule_div

    employees: List[Employee] = []
    for day_div in day_divs:
      second_child_div = day_div.find_all("div", recursive=False)[1]
      label = second_child_div.find("label")
      input_elem = label.find("input")

      if input_elem:
        input_tag = __getAttrs(input_elem)

        if f"setPublicHoliday('{timestamp}');" in input_tag:

          staff_div_container = day_div.find("div", class_="staff-schedule-day-container", recursive=False)
          staff_divs = staff_div_container.findAll("div", class_="staff-schedule-col-staff", recursive=False)
          del staff_div_container

          for staff_div in staff_divs:
            nb_hours_div = staff_div.find(
              "div",
              id=re.compile(r'^staff-schedule-staff-nb-hours(?!.*real).*'),
              class_="staff-schedule-staff-nb-hours",
              recursive=False
            )
            if nb_hours_div and nb_hours_div.text != "":
              code_div = staff_div.find("div", class_="staff-schedule-staff-name")
              code_name = re.search(r'>([^<]+)<', code_div.get("title")).group(1).strip() # type: ignore
              code_name_arr = code_name.split(" ")
              code_name = f"{code_name_arr[0]} {code_name_arr[1][0]}"

              shift_column = staff_div.find("div", class_="staff-schedule-col-staff-selectable")
              shift_divs = shift_column.findAll("div", class_="schedule-onshift")

              # timestamps will get working ranges only if employee is not detached
              timestamp_strings: List[str] = []
              for shift_div in shift_divs:
                if not any(re.search(r'detached', class_name) for class_name in shift_div.get('class', [])):
                  timestamp_strings.append(shift_div.get("data-hour"))

              employee_working_ranges = __get_working_ranges(timestamp_strings)
              if employee_working_ranges:
                employees.append(Employee(code_name, employee_working_ranges))

    self.employees = employees.copy()

    return None

  def set_staffs_from_employees_indexes(self, staff_indexes: List[int]) -> None:
    # Sets the list of staff from the employees indexes
    self.staffs = [Staff(**self.employees[i].__dict__) for i in staff_indexes]

    return None

  def set_timeslots_from_tunn3l(self) -> None:

    def __map_spans_to_slots(slots_divs) -> List[Timeslot]:
      """ Returns the slots (datetime and type) of the day """
      slots = []
      for slot in slots_divs:
        # Gets slot time and type
        header_divs = slot.find("div", class_="panel-heading", recursive=False)
        spans = header_divs.find_all("span")
        time_str = spans[0].get_text(strip=True)
        slot_time = hhmm_string_to_datetime(time_str)
        slot_type = get_slot_type(spans[1].get_text(strip=True))

        # Gets slot booked duration
        available_duration_span = header_divs.find("span", class_="pull-right")
        booked_duration: float = get_booked_duration(available_duration_span.get_text(strip=True))

        # Gets special infos about the slot
        # - handifly
        details_div = slot.find("div", class_='panel-body daily_panel_body')
        handiflys = details_div.find_all(text=re.compile('handifly', re.IGNORECASE))
        has_handi: bool = True if len(handiflys) > 0 else False

        slots.append(Timeslot(
          time_=slot_time,
          type_=slot_type,
          booked=booked_duration,
          has_handifly=has_handi
        ))
      return slots

    # Gets tunn3l"s daily page
    try:
      daily_page = requests.get(self.daily_agenda_url)
      daily = BeautifulSoup(daily_page.content, "html.parser")
    except:
      raise NotFoundError(f"Site not found while accessing the daily agenda,\nPlease check the url: {self.daily_agenda_url}")

    if "Réservations" in daily.title.text: # type: ignore
      raise TokenDisplayError(f"Authentification failed while accessing the daily agenda.\nPlease check tunn3l token at https://back.{self.APP_INPUTS.DOMAIN}.com/backoffice-booking-agenda\nActual token: {self.APP_INPUTS.TUNN3L_TOKEN}")

    # Gets daily slots regarding the unique class daily-container
    div_daily = daily.find("div", class_="daily-container")
    slots_divs = div_daily.find_all("div", class_='row panel panel-default', attrs={'data-timestamp': True}) # type: ignore

    # Maps all spans to make the slot list
    self.slots: List[Timeslot] = __map_spans_to_slots(slots_divs)

    return None

  def set_staffs_from_csv(self, csv_path:str|None=None) -> None:
    """ Parses the list of staffs if given in a csv """
    # Gets file's path
    staffs_csv_file = f"../{os.getenv("STAFF_CSV")}" if csv_path is None else csv_path
    # Reads and parses the csv file
    try:
      if staffs_csv_file is not None:
        with open(staffs_csv_file, "r", encoding="utf-8") as file:
          reader = csv.DictReader(file)

          for row in reader:
            staff_name: str = row["name"]

            # Parses working hour rangges
            working_ranges_str: str = row["working_ranges"]
            working_ranges_array: List[str] = working_ranges_str.split(";")

            working_hour_ranges = []
            for range_ in working_ranges_array:
              start_end_str: List[str] = range_.split("-")

              if len(start_end_str) != 2:
                raise EnvDataError(f"A working range must be made of 2 hours, start and end, your csv has in it: {"-".join(start_end_str)}")

              # checks time validity
              check_time_str(time_string=start_end_str[0])
              check_time_str(time_string=start_end_str[1])

              working_range_start: datetime = hhmm_string_to_datetime(start_end_str[0])
              working_range_end: datetime = hhmm_string_to_datetime(start_end_str[1])

              # We set last slot 30 minutes prior to end working time
              working_range_last_slot: datetime = working_range_end - timedelta(minutes=30)

              if not working_range_start <= working_range_end:
                raise EnvDataError(f"Range end must be after range start, your csv has in it: {"-".join(start_end_str)}")

              working_hour_ranges.append(WorkingRange(
                first_slot=working_range_start,
                last_slot=working_range_last_slot,
              ))

            self.staffs.append(Staff(name=staff_name, working_ranges=copy.deepcopy(working_hour_ranges)))

    except KeyError as e:
      raise EnvDataError(f"Your staff csv file must have fields name,working_ranges, we couldn't find: {e}")
    except FileNotFoundError:
      raise EnvDataError(f"Please provide a valid csv file path in your .env file. or parameter")

    return None

  def set_timeslots_from_csv(self, csv_path:str|None=None) -> None:
    # Gets file's path
    timeslots_csv_file = f"../{os.getenv("TIMESLOTS_CSV")}" if csv_path is None else csv_path
    # Reads and parses the csv file
    try:
      if timeslots_csv_file is not None:
        with open(timeslots_csv_file, "r", encoding="utf-8") as file:
          reader = csv.DictReader(file)

          for row in reader:
            input_time_str: str = row["time"]
            check_time_str(time_string=input_time_str)
            input_time_ = hhmm_string_to_datetime(input_time_str)

            input_type_str: str = row["type"].upper()
            if input_type_str == "FTPRO":
              input_type_str = "PROFT"
            elif input_type_str not in ["FT","PRO","PROFT"]:
              raise EnvDataError(f"The type must be 'FT', 'PRO' or 'PROFT', your csv has in it '{input_type_str}'")
            input_type_: Literal["PRO","FT","FTPRO"] = cast(Literal["PRO","FT","FTPRO"],input_type_str)

            input_has_handifly_str: str = row["has_handifly"].capitalize()
            if input_has_handifly_str not in ["True", "False"]:
              raise EnvDataError(f"The has_handifly must be 'True' or 'False', your csv has in it '{input_has_handifly_str}'")
            else:
              input_has_handifly: bool = { "True": True, "False": False}[input_has_handifly_str]

            try:
              input_booked: int = int(row["booked"])
            except ValueError:
              raise EnvDataError(f"The booked must be a number, your csv has in it '{input_booked}'")

            self.slots.append(Timeslot(
              time_=input_time_,
              type_=input_type_,
              has_handifly=input_has_handifly,
              booked=input_booked
            ))

    except KeyError as e:
      raise EnvDataError(f"Your staff csv file must have fields name,working_ranges, we couldn't find: {e}")
    except FileNotFoundError:
      raise EnvDataError(f"Please provide a valid csv file path in your .env file.")

    return None

  def make_shift(self) -> None:
    """ Returns the daily shift from parsed dailt agenda and stored staffs """

    def __add_prior_brief_slot_to_starting_ft() -> None:
      """ Adds a briefing slot prior to the first one of any range if it is FT """
      for i,slot in enumerate(self.slots):
        # Only FT timeslots need a prior briefing timeslot
        if "FT" in slot.type_:
          needed_prior_slot_time = slot.time_ - timedelta(minutes=30)

          prior_slot: Timeslot
          # if it is the very first slot of the day we add the briefing
          if i == 0:
            prior_slot = Timeslot(time_=needed_prior_slot_time, type_="BRIEFING")
            self.slots.insert(0, prior_slot)

          # If there is no timeslot just before the FT timeslot we add it
          else:
            real_prior_slot_time = self.slots[i-1].time_
            if real_prior_slot_time < needed_prior_slot_time:
              prior_slot = Timeslot(time_=needed_prior_slot_time, type_="BRIEFING")
              self.slots.insert(i, prior_slot)

      return None

    def __add_planning_staff_to_timeslots() -> None:
      """
        Returns the list of timeslots filled with planning staff and
        available staff regarding their working ranges
      """
      for slot in self.slots:

        for staff in self.staffs:
          for staff_range in staff.working_ranges:
            if staff_range.first_slot <= slot.time_ <= staff_range.last_slot:
              slot.planning.append(staff.name)

        # at init, available staff = plannning staff, should_run is false by default
        slot.available = [
          Available(name=staff_name, should_run=False)
          for staff_name in slot.planning
        ]
      return None

    def __next_slot_type(i) -> str:
      if i >= len(self.slots)-1: return "empty"

      after_30_slot = self.slots[i].time_ + timedelta(minutes=30)
      next_slot_time = self.slots[i+1].time_

      if next_slot_time > after_30_slot: return "empty"
      else: return self.slots[i+1].type_

    def __next_is_following(i:int) -> bool:
      """ checks if next slot is right after the slot at the given index """
      if i >= len(self.slots)-1:
        return False

      current_slot = self.slots[i].time_
      should_be_next_slot = current_slot + timedelta(minutes=30)
      real_next_slot = self.slots[i+1].time_

      return True if real_next_slot == should_be_next_slot else False

    def __flag_as_should_run(slot_index:int, staff_name:str) -> None:
      """ Flags an instrcutor as should run for the given slot """
      if slot_index < len(self.slots):
        for staff in self.slots[slot_index].available:
          if staff.name == staff_name:
            staff.should_run = True
            break

      return None

    def __remove_from_availables(slot_index:int, staff_name:str) -> None:
      """ Removes the given staff from the available list """
      if slot_index < len(self.slots):
        for i, staff in enumerate(self.slots[slot_index].available):
          if staff.name == staff_name:
            self.slots[slot_index].available.pop(i)
            break

      return None

    def __remove_annotations(annotated_name:str) -> str:
      """ Removes all annotations to get only the staff name """
      # pattern = r'^\([^\(\)]*\) ([^\(\)]+) \([^\(\)]*\)$'
      staff_name:str = ""

      before_after = r'^(>>) (.*) (\([^()>]+\))( >>)*$'
      match_ = re.match(before_after, annotated_name)
      if  match_ is not None:
        return match_.group(2)

      before = r'^(>>) (.*)$'
      match_ = re.match(before, annotated_name)
      if  match_ is not None:
        return match_.group(2)

      after = r"^([^>].+) (\(.*\))( >>)*$"
      match_ = re.match(after, annotated_name)
      if match_ is not None:
        return match_.group(1)

      no_annotations = r"^[^()>]*$"
      match_ = re.match(no_annotations, annotated_name)
      if match_ is not None:
        return annotated_name

      return staff_name

    # If first slot is FT, we need a prior slot
    __add_prior_brief_slot_to_starting_ft()

    # Adds for each slot the staffs who are available regarding their working ranges
    __add_planning_staff_to_timeslots()

    #Sets roles for each slot
    for i, slot in enumerate(self.slots):
      # We will count only half a slot for FT or FTPRO booked 15 minutes or less
      quotation: float = 1.0 if slot.booked >= 15 else 0.5

      # Staff's totals are compared at global day level but first
      # at same working ranges level, so we'll need a temp counter
      # instance for each shared working ranges

      # If the staffs stored in planning are not the same than the previous slot,
      # we start a new temp counter else we keep the current one
      if i==0 or set(slot.planning)!=set(self.slots[i-1].planning):
        self.staffs_temp = []
        if len(slot.planning) > 0:
          for staff_name in slot.planning:
            self.staffs_temp.append(self._copy_staff_from_name(staff_name))

      # We must check the next slot: if it is a FT slot,
      # we must add a briefer in current slot and available in next slot
      next_slot = __next_slot_type(i)
      if "FT" in next_slot:
        # If available, we select previous driver as briefer
        previous_driver:str = __remove_annotations(self.slots[i-1].drive)
        if any(previous_driver==staff.name for staff in slot.available):
          briefer: Staff | None = self._copy_staff_from_name(previous_driver)
        # Else we select one regarding counters
        else:
          briefer = self._get_less_of("instructor", slot, i)

        self._increment_staff(seek_staff=briefer, role="briefing", add=1.0)
        slot.set_role(staff=briefer, role="briefing", annotations=None)

        if briefer is not None:
          # We remove briefer from availables for current slot
          __remove_from_availables(i, briefer.name)
          __remove_from_availables(i+1, briefer.name)
          # If selected is flagged as should_run, we also add
          # "leave fast" annotation to the previous instructor if same
          previous_instructor = __remove_annotations(self.slots[i-1].instructor)
          if (__next_is_following(i-1)
              and briefer.should_run
              and previous_instructor == briefer.name):
            self.slots[i-1].instructor += " >>"

      # Then we process the current slot
      if "FT" in slot.type_:
        # If slot is a FT, we add the previous brief role as instructor
        previous_briefer_name = __remove_annotations(self.slots[i-1].briefing)
        if previous_briefer_name != "OUCH!":
          instructor = self._find_staff_from_name(previous_briefer_name)
          __remove_from_availables(i, instructor.name)

        else:
          instructor = self._get_less_of("instructor", slot, i)

        self._increment_staff(seek_staff=instructor, role="instructor", add=quotation)
        slot.set_role(staff=instructor, role="instructor", annotations=None)

        if instructor is not None:
          # We don't remove instructor from availables for the next slot but
          # we flag him as "should run" except if total booked duration for
          # the slot is less than 15 minutes
          if __next_is_following(i) == True:
            if slot.booked >= 15:
              # Flags the staff as should run for the nex slot
              __flag_as_should_run(slot_index=i+1, staff_name=instructor.name)

        # Then the instructor needs a driver
        driver = self._get_less_of("drive", slot, i)
        self._increment_staff(seek_staff=driver, role="drive", add=quotation)
        slot.set_role(staff=driver, role="drive", annotations=None)

        if driver is not None:
          __remove_from_availables(i, driver.name)
          # If selected is flagged as should_run, we also add
          # "leave fast" annotation to the previous instructor if same
          previous_instructor = __remove_annotations(self.slots[i-1].instructor)
          if (__next_is_following(i-1)
              and driver.should_run
              and previous_instructor == driver.name):
            self.slots[i-1].instructor += " >>"

      # Processes only proflyer slots
      elif slot.type_ == "PRO":
        doorman = self._get_less_of("doorman", slot, i)
        self._increment_staff(seek_staff=doorman, role="doorman", add=1.0)
        slot.set_role(staff=doorman, role="doorman", annotations=None)

        if doorman is not None:
          __remove_from_availables(i, doorman.name)
          # If selected is flagged as should_run, we also add
          # "leave fast" annotation to the previous instructor if same
          previous_instructor = __remove_annotations(self.slots[i-1].instructor)
          if (__next_is_following(i-1)
              and doorman.should_run
              and previous_instructor == doorman.name):
            self.slots[i-1].instructor += " >>"

      # If slot has handiflys, we must add a doorman
      if slot.has_handifly:
        doorman = self._get_less_of("doorman", slot, i)
        self._increment_staff(seek_staff=doorman, role="doorman", add=quotation)
        slot_annotations: List[Annotation] = [Annotation("after","H")]
        slot.set_role(staff=doorman, role="doorman", annotations=slot_annotations)

        if doorman is not None:
          __remove_from_availables(i, doorman.name)
          # If selected is flagged as should_run, we also add
          # "leave fast" annotation to the previous instructor if same
          previous_instructor = __remove_annotations(self.slots[i-1].instructor)
          if (__next_is_following(i-1)
              and doorman.should_run
              and previous_instructor == doorman.name):
            self.slots[i-1].instructor += " >>"

    return None


