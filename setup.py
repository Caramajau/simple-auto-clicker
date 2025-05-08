from cx_Freeze import setup, Executable # type: ignore

setup(
    name="Simple Auto Clicker",
    description="A simple auto clicker with a text-based UI",
    executables=[Executable("main.py")]
)
