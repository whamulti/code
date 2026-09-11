@echo off
cd /d "%~dp0"
set /p url="Cole o link do video (ou caminho do arquivo local): "
set /p idioma="Idioma de destino (ENTER = pt): "
if "%idioma%"=="" set idioma=pt
python legendar.py "%url%" %idioma%
echo.
pause
