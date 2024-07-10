@echo off
setlocal

:: Define the path to the Python executable
set PYTHON_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe

:: Define the directory containing your package
set PACKAGE_DIR=%USERPROFILE%\AppData\Local\Programs\Python\Python312\Lib\site-packages

:: Set the PYTHONPATH to include the package directory
set PYTHONPATH=%PACKAGE_DIR%

:: Set the SCRIPT_PATH to the __init__.py located in the pdf_crawler subdirectory
set SCRIPT_PATH=%PACKAGE_DIR%\pdf_crawler\__init__.py

:: Execute the __init__.py with the defined Python executable
"%PYTHON_PATH%" "%SCRIPT_PATH%"

endlocal
