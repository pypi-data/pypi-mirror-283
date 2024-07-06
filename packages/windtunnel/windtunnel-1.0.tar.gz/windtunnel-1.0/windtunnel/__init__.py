from typing import Literal, List, Tuple, Dict, cast
from controller import Controller
from errors import WindTunnelError
from model import EmployeeDict, StaffDict, TimeslotDict, Tunn3lAuthDict

windtunnel_controller = Controller()

def make_shift_from_shell(data_source:Literal["tunn3l","csv"]="tunn3l"):
  """
    Run the full process in shell to make the daily shift
    from the indicated data source
    - asks user for the data source
    - handles staff data (if tunn3l, show employee list and ask for staff confirmation)
    - gets timeslots for source
    - makes shift and prints it with staff counter
  """
  windtunnel_controller.make_shift_from_shell(data_source)

def set_tunn3l_auth(data: Dict) -> int:
  try:
    auth_data: Tunn3lAuthDict = cast(Tunn3lAuthDict,data)
    windtunnel_controller.set_tunn3l_auth(auth_data)
  except KeyError as e:
    raise WindTunnelError(f"The tunn3l's auth data must be  a dictionnary with keys: day, domain, tunn3l_token and tunn3l_cookie.\nYou didn't provide the key: {e}")
  return 0

def get_tunn3l_employees() -> List[EmployeeDict]:
  """
    - Gets the daily list of employees from tunnel
    - Sets it in the controller for later use
    - Returns it
  """
  employees: List[EmployeeDict] = windtunnel_controller.get_tunn3l_employees()
  return employees

def set_staffs_from_tunn3l_employees(indexes:List[int]) -> int:
  """
    Prerequisites: list of employees must has been set in the controller
    with the windtunnel's get_tunn3l_employees() function
    - Sets employees as staff for the given index and sets the list in controller for later use
    - returns 0 on success
  """
  windtunnel_controller.set_staffs_from_tunn3l_employees(indexes)
  return 0

def set_timeslots_from_tunn3l() -> int:
  """
    - Gets the timeslot list from tunn3l and sets it on the controller for later use
    - returns 0 on success
  """
  windtunnel_controller.set_timeslots_from_tunn3l()
  return 0

def set_staffs_from_csv(csv_path:str|None=None) -> int:
  """
    - Gets staff list from the given csv and sets it on the controller for later use
    If csv_path is None, we'll use the one provided in the .env file
    - returns 0 on success
  """
  windtunnel_controller.set_staffs_from_csv(csv_path)
  return 0

def set_timeslots_from_csv(csv_path:str|None=None) -> int:
  """
    - Gets timeslot list from the given csv and sets it on the controller for later use
    If csv_path is None, we'll use the one provided in the .env file
    - returns 0 on success
  """
  windtunnel_controller.set_timeslots_from_csv(csv_path)
  return 0

def get_shift_and_staff_counters() -> Tuple[List[StaffDict],List[TimeslotDict]]:
  """
    Prerequisites: staffs and timeslots must has been set with previous functions
    - Makes the shift and staff counters
    - Sets it in the controller
    - Returns it as tuple (staff_counter, shift)
  """
  return windtunnel_controller.get_shift_and_staff_counters()

# RUN PACKAGE AS MAIN()
if __name__ == "__main__":
  # If run in command line, asks user to run from tunn3l or csv
  try:
    user_input = input("Type 'c' to run from csv, anything else to run from tunn3l:")
    user_choice: Literal["csv","tunn3l"] = "csv" if user_input == "c" else "tunn3l"
    make_shift_from_shell(data_source=user_choice)

  except KeyboardInterrupt:
    raise WindTunnelError("You interrupted the program.")

