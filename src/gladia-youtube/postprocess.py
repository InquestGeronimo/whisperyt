import json
import pandas as pd

def pretty_json(response):
    """
    Convert response content to a pretty-printed JSON string and print it.

    :param response: Response object to process.
    :return: JSON data as a Python dictionary.
    """
    if response is None:
        return None

    try:
        # Decode the response content
        response_content = response.content.decode('utf-8')
        json_data = json.loads(response_content)

        # Pretty-print the JSON data
        pretty_json_str = json.dumps(json_data, indent=4)
        print(pretty_json_str)

        return json_data
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
        return None

def save_json_to_file(json_data, file_name):
    """
    Save JSON data to a file.

    :param json_data: JSON data to save.
    :param file_name: Name of the file to save the data to.
    """
    if json_data is None:
        print("No JSON data to save.")
        return

    try:
        with open(file_name, 'w') as file:
            json.dump(json_data, file, indent=4)
    except IOError as e:
        print(f"Failed to write to file {file_name}: {e}")

def get_table(file_path):
    """
    Load JSON data from a specified file and convert it into a pandas DataFrame.

    Returns:
        DataFrame: A pandas DataFrame containing data from the JSON file.
    """

    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        df = pd.json_normalize(json_data, record_path=['prediction'])
                # Drop the 'words' column from the DataFrame
        if 'words' in df.columns:
            df = df.drop(columns=['words'])
        print(df)
        return df
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_full_transcription(file_path):
    
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        # Concatenating all 'transcription' values from the 'prediction' key into a single string
    transcriptions = [prediction['transcription'] for prediction in json_data['prediction'] if 'transcription' in prediction]
    concat_transcriptions = ' '.join(transcriptions)

    print(concat_transcriptions)  # Displaying the first 500 characters for review

def get_transcription_by_turn(df):

    try:
        # Create a new column 'turn' based on consecutive rows
        df['turn'] = (df['speaker'] != df['speaker'].shift()).cumsum()
        
        # Sort the DataFrame by 'turn' for chronological order
        sorted_df = df.sort_values(by='turn')
        
        # Initialize variables to track the current speaker and text
        current_speaker = None
        current_text = []
        
        # Iterate through the sorted DataFrame and print text by speaker, chronologically
        for _, row in sorted_df.iterrows():
            speaker = row['speaker']
            text = row['transcription']
            
            if current_speaker is None:
                current_speaker = speaker
            
            if speaker != current_speaker:
                print(f'Speaker {current_speaker}: {" ".join(current_text)}')
                current_speaker = speaker
                current_text = []
            
            current_text.append(text)
        
        # Print the last speaker's text
        if current_speaker is not None:
            print(f'Speaker {current_speaker}: {" ".join(current_text)}')
    except Exception as e:
        print(f"An error occurred: {e}")