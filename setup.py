from cx_Freeze import setup, Executable

target = Executable(
    script="ProfileBuilder.py",
    base="Win32GUI",
    icon="icon.ico"
    )
setup(
    name = "Profile Builder",
    version = "1.0",
    author="Hlib Bochkarov",
    description = "Profile Builder",
    executables = [target]
)
