from cx_Freeze import Executable, setup  # type: ignore

setup(
    name="Simple Auto Clicker",
    description="A simple auto clicker with a text-based UI",
    executables=[Executable("main.py", base=None, target_name="SimpleAutoClicker")],
)
