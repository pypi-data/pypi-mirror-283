from types import SimpleNamespace
from errors import EnvDataError
from datetime import datetime
from typing import List
import pandas
import re

def hhmm(dt:datetime) -> str:
  """ Returns a hh:mm string representation of the given datetime """
  return dt.strftime('%H:%M')


def as_DataFrame(instance_list:List) -> pandas.DataFrame:
  """ Returns the given list of instance as a pandas DataFrame"""
  dictionnary_list = [instance.__dict__ for instance in instance_list]
  return pandas.DataFrame(dictionnary_list)


def hhmm_string_to_datetime(time_string:str) -> datetime:
  """ Returns datetime from hh:mm string """
  return datetime.strptime(time_string, "%H:%M")


def check_time_str(time_string:str) -> None:
  """ Checks the given string is formated as hh:mm """
  regex = r"^(?:[01]?\d|2[0-3]):(?:0{1,2}|30)$"
  if not re.match(regex, time_string):
    raise EnvDataError(f"You must enter a valid time in hh:mm format and it must be HH:00 or HH:30, your csv has in it: {time_string}")
  return None


def get_slot_type(input_string:str) -> str:
  """ Returns the slot type extracted from html span """
  match = re.match(r"^(.*?)\s*-\s*", input_string)
  if match: return match.group(1)
  return input_string


def get_booked_duration(input_string:str) -> float:
  booked_duration_str:str = input_string.replace("'","")
  booked_duration:float = round(30.0 - float(booked_duration_str), 1)
  return booked_duration


def print_simple_namespace(self, app_inputs: SimpleNamespace) -> None:
  """ Prints all key of the given SimpleNamespace """
  for key, value in vars(app_inputs).items():
    print(f"{key.lower()}: {value}")

  return None

