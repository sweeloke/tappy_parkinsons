from util.project_setup import ProjectSetup
from util.tappy_files_parser import TappyFilesParser
from util.columns_renamer import ColumnsRenamer
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
    self.tappy_parsed_dataframe_file = f'{ProjectSetup.data_dir}/tappy_parsed_dataframe_file.csv'

  def load_raw_dataframe(self):
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

  def load_dataframe(self):
    if not os.path.isfile(self.tappy_parsed_dataframe_file):
      print('There is no raw dataframe available. Please hang on while we parse and load it...')
      raw_df = self.load_raw_dataframe()
      return self.convert_and_dump_dataframe(raw_df)
    
    return pd.read_csv(self.tappy_parsed_dataframe_file, sep=',', index_col=0)

  def convert_and_dump_dataframe(self, raw_df):
    temp_df = ColumnsRenamer(raw_df).rename_columns_to_standard_format()
    temp_df.to_csv(self.tappy_parsed_dataframe_file, index=True, header=True)
    print(f'Dataframe exported to {self.tappy_parsed_dataframe_file}')
    return temp_df