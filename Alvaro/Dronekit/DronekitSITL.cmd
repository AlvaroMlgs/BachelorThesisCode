ECHO off
TITLE Dronekit caller CMD

START "DRONEKIT-SITL" /min /ABOVENORMAL /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Scripts\" "dronekit-sitl.exe" copter-3.3 --model x --home=40.275,-3.736,620,0

START "MAVPROXY" /min /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\MAVProxy\" "mavproxy.exe" --master=tcp:127.0.0.1:5760 --out=127.0.0.1:14550 --out=127.0.0.1:14551

START "Mission Planner" /D "C:\Program Files (x86)\Mission Planner\" "MissionPlanner.exe"
ECHO Remember to connect Mission Planner manually to UDP 127.0.0.1:14551
ECHO.

set /p scriptID=Select script to be executed: 
IF %scriptID% EQU 1 (
	ECHO Executing 1-connectArm.py
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\1-connectArm.py"
 ) 
IF %scriptID% EQU 2 (
	ECHO Executing 2-takeoffLand.py
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\2-takeoffLand.py"
)
IF %scriptID% EQU 3 (
	ECHO Executing 3-locationRelative.py
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\3-locationRelative.py"
)
IF %scriptID% EQU 4 (
	ECHO Executing 4-returnToLaunch.py
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\4-returnToLaunch.py"
)
IF %scriptID% EQU 5 (
	ECHO Executing 5-basicMission.py
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\5-basicMission.py"
)

ECHO.
set /p dummy=Press Enter to END SIMULATION 
TASKKILL /IM MissionPlanner.exe
TASKKILL /IM mavproxy.exe
TASKKILL /IM dronekit-sitl.exe
TASKKILL /FI "Windowtitle eq C:\Windows\system32\cmd.exe - \"C:\Users\alvaro.melgosa\Dropbox\UAVLabs*"

EXIT
