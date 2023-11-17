#!/bin/bash

sleep 5
# Get the current date and time
current_datetime=$(date +"%Y-%m-%d_%H-%M-%S")

# Define the output file
output_file="log.txt"
output_file2="stress.txt"
output_file3="dmesg.txt"
echo "$current_datetime" >> "$output_file"
echo "$current_datetime" >> "$output_file2"

# Run the command with sudo and save the output to the file
hs_timing=$(sudo mmc extcsd read /dev/mmcblk0 | grep HS_TIMING)
echo "$hs_timing" >> "$output_file"

# Check if HS_TIMING is 0x03
echo "Checking HS_TIMING"
count=$(echo "$hs_timing" | grep -c "0x03")
if [ "$count" = "1" ]; then
    echo "HS_TIMING is HS400. Running stress test..."
    sudo stress --hdd 1 --hdd-bytes 1G --timeout 30s -v | tee -a "$output_file2"
	exit_code=$?
	if [ "$exit_code" -eq 0 ]; then
		echo "Rebooting..."
		sleep 5
		sudo reboot
	else
		echo "Stress exited with code " "$exit_code".
		read
	fi
else
    echo "Saving dmesg..."
    echo "$current_datetime" >> "$output_file3"
    sudo dmesg | grep mmc | tee -a "$output_file3"
    echo "HS_TIMING is not HS400. No reboot needed."
	read
fi
