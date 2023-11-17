from csv_convert import csv_convert
import os
from datetime import datetime
import json


def get_cycle_count(list):
    return len(list)

def get_status(list):
    fail_indices = [index for index, value in enumerate(list) if value != 3]
    if not fail_indices:
        status = "PASS"
    else:
        status = "FAIL"
    return status, fail_indices

def get_failed_timestamps(dict):
    for index in dict["fail_indices"]:
        dict["fail_timestamps"].append(dict["timestamp"][index])


root = "C:\\Users\\ahussain\\Documents\\products\\427\\emmc_stress"
# Get a list of subfolders starting with "23"
subfolders = [folder for folder in os.listdir(root) if os.path.isdir(os.path.join(root, folder)) and folder.startswith('23')]
print("Found the following serial numbers:", subfolders)

now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# Combine the base directory and the new folder name with the timestamp
output_folder_path = os.path.join(root, f'output_{now}')
# Create the output folder
os.makedirs(output_folder_path)

for folder in subfolders:

    data_dict = {"sernum" : "",
                "timestamp": [],
                "hs_timing" : [],
                "cycle_count" : 0,
                "status" : "",
                "fail_indices" : [],
                "fail_timestamps" : []}

    data_dict["sernum"] = folder
    data_dict["timestamp"] , data_dict["hs_timing"] = zip(*csv_convert(folder, root + "\\" + folder +"\\log.txt", output_folder_path +"\\" + folder + ".csv"))
    data_dict["cycle_count"] = get_cycle_count(data_dict["hs_timing"])
    data_dict["status"], data_dict["fail_indices"] = get_status(data_dict["hs_timing"])
    get_failed_timestamps(data_dict)
    # Pretty print the dictionary and write it to a JSON file
    with open(output_folder_path + "\\summary.json", 'a') as json_file:
        json.dump(data_dict, json_file, indent=2)  # 'indent' parameter for pretty printing

print("Completed...")