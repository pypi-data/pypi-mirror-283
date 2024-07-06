from typing import List, cast
from rich.console import Console, JustifyMethod
from rich.table import Table
from model import Staff, Timeslot
from errors import print_error, WindTunnelError
from helpers import hhmm
import os
import pandas
import re

#Decorators
def space_before(function):
  """ Decorator: adds a print before the function """
  def wrapper(*args, **kwargs):
    print()
    return function(*args, **kwargs)
  return wrapper

def space_after(function):
  """ Decorator: adds a print after the function """
  def wrapper(*args, **kwargs):
    result = function(*args, **kwargs)
    print()
    return result
  return wrapper

def space_around(function):
  """ Decorator: adds a print before and after the function """
  def wrapper(*args, **kwargs):
    print()
    result = function(*args, **kwargs)
    print()
    return result
  return wrapper


class View:
  """ MVC system's view """

  def __init__(self): pass

  def clear_screen(self) -> None:
    """ Clears terminal screen """
    if os.name == "nt":
      os.system("cls")
    else:
      os.system("clear")
    return None

  @space_around
  def cancel(self):
    raise WindTunnelError("You interrupted the program.")

  @space_around
  def print_tunn3l_employee_names(self, employees_df: pandas.DataFrame) -> None:
    """ Displays the list of employees (needed prior to staff confirmations) """
    print(employees_df["name"].to_string(index=True, name=False))

  @space_after
  def ask_for_staff_indexes_among_tunn3l_employees(self, employees_df: pandas.DataFrame) -> List[int]: # type: ignore
    """ Asks to user and returns indexes of employees who are staffs """

    got_indexes:bool = False
    while not got_indexes:
      indexes_input = input("> Confirm instructor indexes (press enter for all, or use -prefix to remove):")
      # Empty input is a shortcut to tell that all employees
      # are staff, we return all indexes
      all_indexes: List[int] = employees_df.index.tolist()
      if indexes_input == "":
        return all_indexes

      # Else we process the input, separators can be . or ,
      regex = r"^(-?\d+([,.]-?\d+)*)$"
      if not re.match(regex, indexes_input):
        print_error("Please type only numbers or -number separated by commas or dots, or type enter.")
        continue

      indexes_array = re.split(r'[.,]', indexes_input, 0)

      # Checks if all inputs starts with - or all without,
      # else prints error and ask again
      dash_pattern = re.compile(r'^-')
      digit_pattern = re.compile(r'^\d')

      all_start_with_dash = all(dash_pattern.match(index) for index in indexes_array)
      all_start_with_digit = all(digit_pattern.match(index) for index in indexes_array)

      if not(all_start_with_dash or all_start_with_digit):
        print_error("Please type only -index or only +index, but you can't mix it")
        continue

      # We convert string inputs as int
      try:
        confirmed_indexes = [int(i) for i in indexes_array]
      except ValueError:
        print_error("Please type only numbers separated by commas or dots, or type enter.")
        continue

      # we check all typed indexes exist
      not_existing_indexes: List[int] = [index for index in confirmed_indexes if abs(index) not in all_indexes]
      if len(not_existing_indexes) == 0:
        deduplicated_indexes = []
        seen = set()
        for index in indexes_array:
          if index not in seen:
            deduplicated_indexes.append(index)
            seen.add(index)

        # In case of minus
        if any(index.startswith("-") for index in indexes_array):
          indexes_to_remove: List[int] = [abs(int(i)) for i in indexes_array]
          indexes_to_keep: List[int] = [i for i in all_indexes if i not in indexes_to_remove]
          # Forbids empty list
          if len(indexes_to_keep) == 0:
            print_error("You can't remove every one, someone must do the job!")
            continue
        else:
          indexes_to_keep = [int(i) for i in indexes_array]
        return indexes_to_keep
      else:
        print_error(f"You typed indexes that are not in the displayed list: {not_existing_indexes}.")
        continue

  @space_after
  def print_staff_counters(self, staffs: List[Staff]) -> None:
    """ Nicely print the given input """
    console = Console()

    printed_staffs = [
      {**vars(staff), "planning":str }
      for staff in staffs
    ]

    # Formats working ranges
    for staff in printed_staffs:
      str_ranges: List[str] = []
      for wr in staff["working_ranges"]:
        str_ranges.append(f"{hhmm(wr.first_slot)}-{hhmm(wr.last_slot)}")

      staff["planning"] = " / ".join(str_ranges)

    # Sorts list by planning
    printed_staffs.sort(key=lambda staff: staff["planning"])

    # Removes unwanted columns for display
    printed_staffs = pandas.DataFrame(printed_staffs).drop(columns=["working_ranges"])

    # Moves planning column to 2nd position
    columns = list(printed_staffs.columns)
    columns.remove("planning")
    columns.insert(1, "planning")
    columns.remove("should_run")
    printed_staffs = printed_staffs[columns]

    printed_staffs.columns = [col.upper() for col in printed_staffs.columns]
    styles = {
      "PLANNING": "bright_green",
      "TOTAL": "bright_yellow",
      "NAME": "bright_cyan"
    }

    table_to_print = Table(show_header=True)

    justifys = { "NAME": "left" }
    for column in printed_staffs.columns:
      header_style = f"bold {styles.get(column, "bright_white")}"
      column_justify:str = f"{justifys.get(column, "right")}"
      table_to_print.add_column(
        column,
        header_style=header_style,
        justify=cast(JustifyMethod, column_justify)
      )

    for index, row in printed_staffs.iterrows():
      table_to_print.add_row(*[f"[{styles.get(column, 'bright_white')}] {value}" for column, value in zip(printed_staffs.columns, row)])

    console.print(table_to_print)

  @space_after
  def print_shift(self, slots: List[Timeslot], details:bool) -> None:
    """ Nicely print the given input """
    console = Console()

    printed_shift = [{**vars(slot)} for slot in slots]

    # Formats, renames and duplicates Timeslot column
    for slot in printed_shift:
      slot["time_"] = hhmm(slot["time_"])
      slot["planning"] = ", ".join(slot["planning"])
      slot["available"] = ", ".join(staff.name for staff in slot["available"])

    printed_shift = pandas.DataFrame(printed_shift)

    # Changes boolean value for handifly to "H" or ""
    printed_shift["has_handifly"] = printed_shift["has_handifly"].apply(lambda has_handifly: "H" if has_handifly else "")
    # Changes booked value to "-" when "Reserved" or "Briefing"
    printed_shift["booked"] = printed_shift.apply(
      lambda row: "-" if row["type_"] in ["Reserved","BRIEFING"] else row["booked"],
      axis=1)

    # Moves planning column to 2nd position
    columns = list(printed_shift.columns)
    columns.remove("type_")
    columns.insert(3, "type_")
    columns.insert(10, "time_")

    if not details:
      columns.remove("planning")
      columns.remove("available")

    printed_shift = printed_shift[columns]

    printed_shift.rename(
      columns={
        "time_":"Timeslot",
        "type_": "type",
        "available": "disponible",
        "has_handifly": "handi"
      },
      inplace=True
    )

    # Colors columns
    printed_shift.columns = [col.upper() for col in printed_shift.columns]
    styles = {
      "TIMESLOT": "bright_green",
      "SLOT": "bright_green",
      "TYPE": "bright_blue",
      "HANDI": "plum1",
      "BOOKED": "plum1",
      "PLANNING": "cyan",
      "DISPONIBLE": "cyan",
    }
    shift_caption = f"LEGEND:\nOUCH!: \"chef, ça passe pas\".\nInstructor >>: should run to leave\n>> Instructor: should run to start\n(H): second instructor for handifly."

    table_to_print = Table(show_header=True, caption=shift_caption, caption_justify="left")

    justifys = {
      "HANDI": "center",
      "BOOKED": "right"
    }
    for column in printed_shift.columns:
      header_style = f"bold {styles.get(column, "bright_white")}"
      column_justify:str = f"{justifys.get(column, "left")}"
      table_to_print.add_column(
        column,
        header_style=header_style,
        justify=cast(JustifyMethod, column_justify)
      )

    for index, row in printed_shift.iterrows():
      table_to_print.add_row(
        *[f"[{styles.get(column, 'bright_white')}] {value}"
        for column, value in zip(printed_shift.columns, row)]
      )

    console.print(table_to_print)
