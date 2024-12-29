import os
import json
from datetime import datetime

def save_object_locally(my_object):
    # Get the current date and format it as YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Define the data folder in the root directory
    data_folder = os.path.join(os.getcwd(), 'data')

    # Create the data folder if it doesn't exist
    os.makedirs(data_folder, exist_ok=True)

    # Define the file name with the current date
    file_path = os.path.join(data_folder, f'{current_date}.json')

    # Save the object to the file as JSON
    with open(file_path, 'w') as file:
        json.dump(my_object, file, indent=4)

def load_object_from_today():
    # Get the current date and format it as YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define the data folder in the root directory
    data_folder = os.path.join(os.getcwd(), 'data')
    
    # Define the file name with today's date
    file_path = os.path.join(data_folder, f'{current_date}.json')
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the object from the file as a dictionary
        with open(file_path, 'r') as file:
            my_object = json.load(file)
        return my_object
    else:
        print(f"No file found for today's date: {current_date}")
        return None