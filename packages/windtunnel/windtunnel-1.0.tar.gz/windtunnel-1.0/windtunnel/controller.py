from typing import List, Tuple, Dict
from view import View
from model import Model, EmployeeDict, StaffDict, TimeslotDict, Tunn3lAuthDict


class Controller:
  """ MVC system's controller """

  def __init__(self):
    self.ui = View()
    self.model = Model()

  def _set_staffs(self, from_:str) -> None:
    """ Handles inputs from tunn3l or csv """

    # Handles data if source is tunn3l
    if from_ == "tunn3l":
      # Gets list of daily employees then...
      self.model.set_daily_employees_from_tunn3l()

      # ... asks who are staffs among employees
      # # Displays retrieves employees
      self.ui.print_tunn3l_employee_names(self.model.employees_df)
      # Gets staffs indexes
      staff_indexes = self.ui.ask_for_staff_indexes_among_tunn3l_employees(self.model.employees_df)
      # Stores staff
      self.model.set_staffs_from_employees_indexes(staff_indexes)

    # Handles data if source is csv
    elif from_ == "csv":
      # Gets staffs from csv file
      self.model.set_staffs_from_csv()

    return None

  def _set_timeslots(self, from_:str) -> None:

    # Handles data if source is tunn3l
    if from_ == "tunn3l":
      # Gets timeslots for the setted day from env data
      self.model.set_timeslots_from_tunn3l()

    # Handles data if source is csv
    elif from_ == "csv":
      # Gets timeslots from csv file
      self.model.set_timeslots_from_csv()

    return None

  def make_shift_from_shell(self, data_source:str) -> None:
    """
      Run the full process in shell to make the daily shift
      from the indicated data source
      - asks user for the data source
      - handles staff data (if tunn3l, show employee list and ask for staff confirmation)
      - gets timeslots for source
      - makes shift and prints it with staff counter
    """
    try:
      # Clears terminal screen
      self.ui.clear_screen()

      # If data source is tunn3l, we need to get authentification data
      if data_source == "tunn3l":
        # Gets tunn3l's authentification data from .env
        self.model._get_tunn3l_auth_from_env()

      # Gets inputs from user or code
      self._set_staffs(from_=data_source)

      self._set_timeslots(from_=data_source)

      # Makes shift with all needed data nnow stored in model
      self.model.make_shift()

      # Prints final staff table with shift counters
      self.ui.print_staff_counters(staffs=self.model.staffs)

      # Prints final shift
      self.ui.print_shift(slots=self.model.slots, details=False)

      return None

    except KeyboardInterrupt:
      self.ui.cancel()

  # Functions for external use
  def set_tunn3l_auth(self, input_data: Tunn3lAuthDict) -> int:
    self.model.set_day(input_data["day"])
    self.model.set_tunn3l_domain(input_data["domain"])
    self.model.set_tunn3l_token(input_data["tunn3l_token"])
    self.model.set_tunn3l_cookie(input_data["tunn3l_cookie"])
    return 0

  def get_tunn3l_employees(self) -> List[EmployeeDict]:
    """
      Prerequisites: tunn3l authentification data must has been set
      first with set_tunn3l_auth()
      - Gets the daily list of employees from tunnel
      - Sets it in the controller for later use
      - Returns it
    """
    self.model.set_daily_employees_from_tunn3l()
    return self.model.employees_dicts

  def set_staffs_from_tunn3l_employees(self, indexes:List[int]) -> int:
    """
      Prerequisites: list of employees must has been set in the
      controller with get_tunn3l_employees()
      - Sets into the controller the list of employees from the given indexes
      - returns 0 on success
    """
    self.model.set_staffs_from_employees_indexes(staff_indexes=indexes)
    return 0

  def set_timeslots_from_tunn3l(self) -> int:
    """
      - Gets the timeslot list from tunn3l and sets it on the controller for later use
      - returns 0 on success
    """
    self.model.set_timeslots_from_tunn3l()
    return 0

  def set_staffs_from_csv(self, csv_path:str|None=None) -> int:
    """
      - Gets staff list from the given csv and sets it on the controller for later use
      If csv_path is None, we'll use the one provided in the .env file
      - returns 0 on success
    """
    self.model.set_staffs_from_csv(csv_path)
    return 0

  def set_timeslots_from_csv(self, csv_path:str|None=None) -> int:
    """
      - Gets timeslot list from the given csv and sets it on the controller for later use
      If csv_path is None, we'll use the one provided in the .env file
      - returns 0 on success
    """
    self.model.set_timeslots_from_csv(csv_path)
    return 0

  def get_shift_and_staff_counters(self) -> Tuple[List[StaffDict],List[TimeslotDict]]:
    """
      Prerequisites: staffs and timeslots must has been set with previous functions
      - Makes the shift and staff counters
      - Sets it in the controller
      - Returns it as tuple
    """
    self.model.make_shift()
    staff_counter_dicts: List[StaffDict] = self.model.staffs_dicts
    slots_dicts: List[TimeslotDict] = self.model.slots_dicts
    return staff_counter_dicts, slots_dicts
