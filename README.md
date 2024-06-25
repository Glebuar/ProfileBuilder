
# Profile Builder

Profile Builder is a Tkinter-based application for building profiles using exported Risk Forms.

## Steps:

1. Drag and drop or select the exported *.ixt form file.
2. Save the JSON file containing all form fields.
3. Create a profile in Boomi and import from the saved file.
###
# Development Requirements

- Python 3.x
- `tkinterdnd2` library
- `cx_Freeze` for building the executable

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/Glebuar/ProfileBuilder.git
cd ProfileBuilder
```

### 2. Set up the Python environment

Ensure you have Python 3.x installed on your system. You can download it from the official [Python website](https://www.python.org/downloads/).

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Install `cx_Freeze`

```sh
pip install cx_Freeze
```

## Running the Program

If your system is prepared with Python and all required dependencies, you can run the program directly:

```sh
python ProfileBuilder.py
```
## Building the Executable

To build the executable for distribution, you can use `cx_Freeze`. Ensure you have installed `cx_Freeze` as shown above, and then run:

```sh
python setup.py build
```

The executable will be generated in the `build/exe.win-amd64-3.12/` directory (the exact path may vary).

## Notes

- Make sure you have the necessary permissions to install software and run scripts on your system.
- If you encounter any issues, please check the error messages and ensure all dependencies are correctly installed.
