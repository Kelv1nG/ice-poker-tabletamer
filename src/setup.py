from cx_Freeze import setup, Executable

# Specify the build options
setup(
    name="Curb Your Tables",
    version="0.1a",
    description="Poker Table Manager",
    executables=[Executable("application.py")],
)
