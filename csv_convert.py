import csv
import re
from datetime import datetime

def extract_values(data):
    hex_pattern = re.compile(r'0x([0-9a-fA-F]+)')
    timestamp = convert_excel_timestamp(data[0::2])
    hex = [match.group(1) for s in data[1::2] for match in [hex_pattern.search(s)] if match]
    hex_num = number_list = [int(value) for value in hex]
    return timestamp, hex_num

def convert_excel_timestamp(data):
    excel_timestamps = [datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S").strftime("%Y-%m-%dT%H:%M:%S") for ts in data]
    return excel_timestamps

def csv_convert(sernum, input_file_path, output_file_path):
    """
    Convert data from the input file to a CSV file, extracting hex values.
    """

    print("Serial Number:\t" + sernum)
    print("\tOpening " + input_file_path)
    # Read data from the input file
    with open(input_file_path, 'r') as file:
        # Assuming each line has a timestamp and a message
        data = [line.strip() for line in file]


    # Extract hex values using the extract_hex_values function
    timestamp, hex_values = extract_values(data)

    #create list from serial nummber
    sernum_values = [sernum] * len(hex_values)

    # Combine timestamps with extracted hex values
    result_data = list(zip(timestamp, hex_values))

    # Open the CSV file in write mode
    with open(output_file_path, mode='a', newline='') as file:
        print("\tAppending to " + output_file_path)
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the header if needed
        #writer.writerow(["SerialNumber", "Timestamp", "HS_TIMING"])

        # Write the data to the CSV file
        writer.writerows(result_data)
    
    return result_data

    print(f"Conversion to CSV complete. CSV file saved at {output_file_path}")