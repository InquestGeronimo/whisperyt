import json
import pandas as pd
from typing import Optional, Union
from requests.models import Response

class DataProcessor:
    """
    A utility class for processing data, including JSON responses and files, and working with pandas DataFrames.

    This class provides methods for converting JSON responses to pretty-printed strings, saving JSON data to files,
    loading JSON data into pandas DataFrames, extracting transcriptions, and displaying transcriptions by speaker turn.

    """
    
    @staticmethod
    def pretty_json(response: Response) -> Optional[str]:
        """
        Convert response content to a pretty-printed JSON string.

        :param response: Response object to process.
        :return: Pretty-printed JSON string.
        """
        if not response:
            return None

        try:
            json_data = response.json()
            return json.dumps(json_data, indent=4)
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            return None

    @staticmethod
    def save_json_file(json_data: Union[dict, list], file_name: str) -> None:
        """
        Save JSON data to a file.

        :param json_data: JSON data to save.
        :param file_name: Name of the file to save the data to.
        """
        if not json_data:
            print("No JSON data to save.")
            return

        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4)
        except IOError as e:
            print(f"Failed to write to file {file_name}: {e}")

    @staticmethod
    def get_table(file_path: str, max_rows: int=100) -> Optional[pd.DataFrame]:
        """
        Load JSON data from a file and convert it into a pandas DataFrame.

        :param file_path: Path to the JSON file.
        :param max_rows: max rows to print in dataframe.
        :return: DataFrame containing the data, or None if an error occurs.
        """
        
        pd.set_option('display.max_rows', max_rows)  
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            df = pd.json_normalize(json_data, record_path=['prediction'])
            if 'words' in df.columns:
                df.drop(columns=['words'], inplace=True)
            return df
        except FileNotFoundError:
            print("File not found.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def get_full_transcription(file_path: str) -> Optional[str]:
        """
        Extract full transcriptions from a JSON file.

        :param file_path: Path to the JSON file.
        :return: Full transcription string, or None if an error occurs.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            transcriptions = [prediction['transcription'] for prediction in json_data['prediction'] if 'transcription' in prediction]
            return ' '.join(transcriptions)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def get_transcription_by_turn(df: pd.DataFrame) -> None:
        """
        Display transcriptions by speaker turn from a DataFrame.

        :param df: DataFrame containing transcription data.
        """
        try:
            df['turn'] = (df['speaker'] != df['speaker'].shift()).cumsum()
            sorted_df = df.sort_values(by='turn')

            current_speaker = None
            current_text = []

            for _, row in sorted_df.iterrows():
                speaker = row['speaker']
                text = row['transcription']

                if current_speaker is None:
                    current_speaker = speaker

                if speaker != current_speaker:
                    print(f'\nSpeaker {current_speaker}: {" ".join(current_text)}')
                    current_speaker = speaker
                    current_text = []

                current_text.append(text)

            if current_speaker is not None:
                print(f'\nSpeaker {current_speaker}: {" ".join(current_text)}')
        except Exception as e:
            print(f"An error occurred: {e}")
