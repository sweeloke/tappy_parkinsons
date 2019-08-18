from util.tappy_files_parser import TappyFilesParser
import pandas as pd
import os.path

class TappyLoader:
  TAPPY_COLUMN_TYPES = {
    'UserKey': 'str',
    'Date': 'str',
    'Timestamp': 'str',
    'Hand': 'str',
    'Hold time': 'float64',
    'Direction': 'str',
    'Latency time': 'float64',
    'Flight time': 'float64'
  }
  TAPPY_COLUMN_NAMES = TAPPY_COLUMN_TYPES.keys()

  def __init__(self):
    self.parser = TappyFilesParser()

  # TODO: improve this loader: it should be smart enough to download and unzip the files
  def load_dataframe(self):
    if not os.path.isfile(self.parser.good_lines_output_file):
      print('The files are not parsed yet. Please hang on while we parse them and instantiate the dataframe...')
      self.parser.generate_output_files()
      
    return pd.read_csv(
      self.parser.good_lines_output_file,
      delim_whitespace=True,
      header=None,
      names=self.TAPPY_COLUMN_NAMES,
      dtype=self.TAPPY_COLUMN_TYPES
    )