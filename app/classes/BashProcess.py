import subprocess
from typing import List, Union


class BashProcess:
    """Executes bash commands and returns the output."""

    def __init__(self, location: str, strip_newlines: bool = False, return_err_output: bool = False):
        """Initialize with stripping newlines."""
        self.strip_newlines = strip_newlines
        self.return_err_output = return_err_output
        self.location = location

    def run(self, commands: Union[str, List[str]]) -> str:
        """Run commands and return final output."""
        if isinstance(commands, str):
            commands = [commands]
        commands = ";".join(commands)

        try:
            output = subprocess.run(
                "cd dst && "+commands,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            ).stdout
            if (isinstance(output, int)):
                output = output.decode()
        except subprocess.CalledProcessError as error:
            if self.return_err_output:
                return error.stdout.decode()
            return str(error)
        if self.strip_newlines:
            output = output.strip()
        return output
