import subprocess

class Menu():
    """
    A class for creating a code assistant menu using the bemenu program.

    Parameters:
    cmd (str, optional): The path to the bemenu program. Defaults to "bemenu".
    args (list[str], optional): A list of arguments to pass to the bemenu program. Defaults to [].

    Attributes:
    _cmd (str): The path to the bemenu program.
    _args (list[str]): A list of arguments to pass to the bemenu program.

    """

    def __init__(self, cmd: str = "bemenu", args: list[str] = []):
        self._cmd: str = cmd
        self._args: list[str] = args

    def run(
        self,
        prompt: str,
        items: list[str] = [],
        new_args: list[str] = [],
    ) -> str | None:
        """
        Runs the bemenu program with the specified arguments and returns the selected item.

        Parameters:
        prompt (str): The prompt to display to the user.
        items (list[str], optional): A list of items to display in the menu. Defaults to [].
        new_args (list[str], optional): A list of additional arguments to pass to the bemenu program. Defaults to [].

        Returns:
        str | None: The selected item, or None if no item was selected.

        """
        out = subprocess.run(
            [self._cmd] + self._args + new_args + ["-p", prompt],
            input="\n".join(items).encode("utf-8"),
            stdout=subprocess.PIPE,
        )
        if not (out.returncode == 0 or out.returncode == 1):
            print(f"code: {out.returncode}\nerr: {out.stderr}")
        if out.stdout.decode("utf-8") is not None:
            return out.stdout.decode("utf-8")
        if out.returncode == 1:
            return None


