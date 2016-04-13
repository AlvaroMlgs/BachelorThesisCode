ECHO off
TITLE Dronekit caller CMD

ECHO Ensure UAV is already connected to the computer via Serial Port
set /p port=Which port is UAV connected to? 
set /p baud=Which is the baudrate used for the connection? 
ECHO.

START "MAVPROXY" /min /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\MAVProxy\" "mavproxy.exe" --master=com%port% baud=%baud% --out=127.0.0.1:14550 --out=127.0.0.1:14551

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
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\2-takeoffLand.py"
)
IF %scriptID% EQU 3 (
	ECHO Executing 3-locationRelative.py
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\3-locationRelative.py"
)
IF %scriptID% EQU 4 (
	ECHO Executing 4-returnToLaunch.py
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\4-returnToLaunch.py"
)
IF %scriptID% EQU 5 (
	ECHO Executing 5-basicMission.py
	START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3" "WinPython Command Prompt.exe" "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\WinPython-64bit-2.7.10.3\DRONEKIT\5-basicMission.py"
)

ECHO.
set /p dummy=Press Enter to END SIMULATION 
ECHO Careful! This might be dangerous if UAV is on the air
PAUSE
TASKKILL /IM MissionPlanner.exe
TASKKILL /IM mavproxy.exe
TASKKILL /IM dronekit-sitl.exe
TASKKILL /FI "Windowtitle eq C:\Windows\system32\cmd.exe - \"C:\Users\alvaro.melgosa\Dropbox\UAVLabs*"

EXIT
