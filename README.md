# Project Name
## ABCGovt Web scrapping
### Python Installation Process
Before proceeding, ensure Python is installed on your system. If not, you can download and install Python from [python.org](https://www.python.org/downloads/).
### Clone the Project
```bash
git clone https://github.com/exoticaitsolutions/abcbiz.abc-Project2.git
```

## Navigate to the Project Directory

```bash
  cd abcbiz.abc-Project2
```

This script will create a virtual environment, activate it, and install all required packages specified in requirements.txt. and updating the pip 

# **_Windows:_**
```
setup.bat
```
**Unix/MacOS:**
```
bash setup.sh
```

# Run Project
**Windows:**

```bash
python.exe login_screen.py
```

**Unix/MacOS/Linux:**

```bash
python3 login_screen.py
```

# To create a windows executable ".exe" file.
```bash
pip install babel
```

# Generates the exe file
```bash
pyinstaller --onefile --hidden-import=babel.numbers --hidden-import=babel.localtime --icon=ReportIcon.ico  --windowed login_screen.py  
```

# Build the executable using the spec file
```bash
pyinstaller license_report_gen.spec
```
# abcbiz.abc-Project2
