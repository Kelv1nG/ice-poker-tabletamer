from cx_Freeze import setup, Executable
import sys

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"

# Specify the build options
setup(
    name="Curb Your Tables",
    version="0.1a",
    description="Poker Table Manager",
    executables=[Executable("application.py", base='Win32GUI')] # base = None removes the console window
)
