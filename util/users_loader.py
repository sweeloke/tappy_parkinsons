from util.project_setup import ProjectSetup
from util.users_files_parser import UsersFilesParser
from util.columns_renamer import ColumnsRenamer
import pandas as pd
import os.path

class UsersLoader:
  def __init__(self):
    self.parser = UsersFilesParser()
    self.users_parsed_dataframe_file = f'{ProjectSetup.data_dir}/users_parsed_dataframe_file.csv'

  def load_raw_dataframe(self):
    if not os.path.isfile(self.parser.raw_parsed_users_file):
      print('The files are not parsed yet. Please hang on while we parse them and instantiate the dataframe...')
      self.parser.generate_output_files()

    return pd.read_csv(self.parser.raw_parsed_users_file, sep=',', index_col=0)

  def load_dataframe(self):
    if not os.path.isfile(self.users_parsed_dataframe_file):
      print('There is no raw dataframe available. Please hang on while we parse and load it...')
      raw_df = self.load_raw_dataframe()
      return self.convert_and_dump_dataframe(raw_df)
    
    return pd.read_csv(self.users_parsed_dataframe_file, sep=',', index_col=0)

  def convert_and_dump_dataframe(self, raw_df):
    temp_df = raw_df.reset_index().rename(columns={'index': 'UserKey'})
    temp_df = ColumnsRenamer(temp_df).rename_columns_to_standard_format()
    temp_df.to_csv(self.users_parsed_dataframe_file, index=True, header=True)
    print(f'Dataframe exported to {self.users_parsed_dataframe_file}')
    return temp_df
