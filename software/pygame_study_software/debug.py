import json

# Read the JSONL file
def get_last_wrist_threshold(jsonl_file):
        last_wrist_threshold = None
        with open(jsonl_file, 'r') as f:
                for line in f:
                        data = json.loads(line.strip())
                        if "Wrist threshold value" in data:
                                last_wrist_threshold = data["Wrist threshold value"]
        return last_wrist_threshold

# Provide the path to your JSONL file
jsonl_file = "./P0/P0-calibration.json"
last_wrist_threshold = get_last_wrist_threshold(jsonl_file)

if last_wrist_threshold is not None:
        print("Last Wrist threshold value:", last_wrist_threshold)
else:
        print("No Wrist threshold value found in the file.")
