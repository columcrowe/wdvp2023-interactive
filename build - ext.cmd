@ECHO OFF
ECHO %cd%
PAUSE
pushd \\FS1\Docs3\colum.crowe\My Documents\Python\envs\myenv\Scripts
ECHO %cd%
PAUSE
@ECHO ON
set PATH=C:\Anaconda3;%PATH%
set PATH=C:\Anaconda3\Scripts;%PATH%
set PATH=C:\Anaconda3\Library\bin;%PATH%
::REM call conda activate myenv
::REM call conda activate tf1
set "PYTHONPATH=\\FS1\Docs3\colum.crowe\My Documents\Python\envs\myenv"
set "VIRTUAL_ENV=\\FS1\Docs3\colum.crowe\My Documents\Python\envs\myenv"
set PATH=\\FS1\Docs3\colum.crowe\My Documents\Python\envs\myenv\Scripts;%PATH%
set PATH=\\FS1\Docs3\colum.crowe\My Documents\Python\envs\myenv\Lib;%PATH%
call activate.bat
set
@ECHO OFF
ECHO %cd%
PAUSE
cd ./../
cd ./../
cd ./../
popd
ECHO %cd%
PAUSE
pushd E:\
ECHO %cd%
PAUSE
cd E:\WDVP2023\wdvp2023-interactive\
ECHO %cd%
PAUSE
python -m pip install shiny
shiny create myapp
python -m pip install shinylive
shinylive export myapp docs
shiny run --reload myapp/app.py