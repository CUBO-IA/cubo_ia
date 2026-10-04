@echo off
REM ============================================================
REM  Genera dist\AventuraPixel.exe con PyInstaller
REM  Ejecutar desde la raiz del proyecto con el .venv activo
REM ============================================================

cd /d "%~dp0"

python -m pip install --upgrade pyinstaller

python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name AventuraPixel ^
  --icon "%~dp0assets\icon\icon.ico" ^
  --add-data "%~dp0assets;assets" ^
  --workpath build ^
  --distpath dist ^
  --specpath build ^
  "%~dp0main.py"

echo.
echo Listo: dist\AventuraPixel.exe
pause
