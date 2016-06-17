ECHO off
TITLE Dronekit caller CMD

START "DRONEKIT-SITL" /min /ABOVENORMAL /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Scripts\" "dronekit-sitl.exe" copter-3.2.1 --model x --home=40.333266, -3.765728,620,90

START "MAVPROXY" /min /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\MAVProxy\" "mavproxy.exe" --master=tcp:127.0.0.1:5760 --out=127.0.0.1:14550 --out=127.0.0.1:14551

START "Mission Planner" /D "C:\Program Files (x86)\Mission Planner\" "MissionPlanner.exe"
ECHO Remember to connect Mission Planner manually to UDP 127.0.0.1:14551
ECHO.

set /p scriptID=Select script to be executed: 
START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\DRONEKIT\" %scriptID%

ECHO.
::set /p dummy=Press Enter to END SIMULATION 
::TASKKILL /IM MissionPlanner.exe
::TASKKILL /IM mavproxy.exe
::TASKKILL /IM dronekit-sitl.exe

EXIT
