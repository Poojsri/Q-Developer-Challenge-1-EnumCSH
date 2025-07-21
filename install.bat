@echo off
echo Installing enumCSh...

REM Check if pip is installed
where pip >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: pip is not installed. Please install Python and pip first.
    exit /b 1
)

REM Check if Nmap is installed
where nmap >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Warning: Nmap is not installed. Some features may not work.
    echo To install Nmap, download from https://nmap.org/download.html
)

REM Install the package with all dependencies
pip install --user -e .

REM Verify installation of key dependencies
pip show typer rich click shellingham

REM If any dependencies are missing, install them individually
pip install --user typer rich click shellingham typing-extensions markdown-it-py pygments mdurl

REM Create a batch file in the user's directory to run the tool directly
echo @echo off > "%USERPROFILE%\enumcsh.bat"
echo python "%~dp0\enumcsh.py" %%* >> "%USERPROFILE%\enumcsh.bat"

echo.
echo To use the tool directly, copy %USERPROFILE%\enumcsh.bat to a location in your PATH
echo or add %USERPROFILE% to your PATH environment variable.

echo Installation complete!
echo You can now use enumCSh by running: enumcsh
echo For help, run: enumcsh --help