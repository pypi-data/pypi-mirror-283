import sys
from rich.console import Console

console = Console()

def print_error(message):
  """ Prints error message in red """
  console.print(f"\n[bright_red]{message}[/bright_red]\n")


class WindTunnelError(Exception):
  """ Prints error message and exits """
  def __init__(self, message):
    self.message = message
    print_error(message)
    super().__init__(message)
    sys.exit(1)


class TokenDisplayError(WindTunnelError):
  def __init__(self, message):
    super().__init__(message)


class NotFoundError(WindTunnelError):
  def __init__(self, message):
    super().__init__(message)


class AuthenticationError(WindTunnelError):
  def __init__(self, message):
    super().__init__(message)


class EnvDataError(WindTunnelError):
  def __init__(self, message):
    super().__init__(message)