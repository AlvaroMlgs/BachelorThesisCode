#!/bin/bash

echo "Ensure UAV is already connected to the computer via Serial Port"
echo "Which port is UAV connected to? (Try ttyACM0) "
read port
echo "Which is the baudrate used for the connection? "
read baud

sudo mavproxy.py --master=/dev/$port --baud=$baud --out=127.0.0.1:14550 --out=127.0.0.1:14551 &

echo "Select script to be executed: "
read script

python $script





