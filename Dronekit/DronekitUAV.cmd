ECHO off
TITLE Dronekit caller CMD

ECHO Ensure UAV is already connected to the computer via Serial Port
set /p port=Which port is UAV connected to? 
set /p baud=Which is the baudrate used for the connection? 
ECHO.

START "MAVPROXY" /min /D "C:\Users\Usuario\Google Drive\TFG Alvaro Melgosa Pascual\MAVProxy\" "mavproxy.exe" --master=com%port% --baud=%baud% --out=127.0.0.1:14550 --out=127.0.0.1:14551

START "Mission Planner" /D "C:\Program Files (x86)\Mission Planner\" "MissionPlanner.exe"
ECHO Remember to connect Mission Planner manually to UDP 127.0.0.1:14551
ECHO.

set /p scriptID=Select script to be executed: 
START "DRONEKIT-SCRIPT" /D "C:\Users\Usuario\Documents\GitHub\quadcopters-tfg-lvaro\Dronekit" %scriptID%

ECHO.
::set /p dummy=Press Enter to END SIMULATION 
::ECHO Careful! This might be dangerous if UAV is on the air
::PAUSE
::TASKKILL /IM MissionPlanner.exe
::TASKKILL /IM mavproxy.exe
::TASKKILL /IM dronekit-sitl.exe

EXIT
