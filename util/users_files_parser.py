from util.project_setup import ProjectSetup
from util.users_parser import UsersParser
import pandas as pd
import glob

class UsersFilesParser:
  def __init__(self, verbose=1):
    self.verbose = verbose
    self.users_files = self.__users_files()    
    self.raw_parsed_users_file = f'{ProjectSetup.data_dir}/raw_parsed_users.txt'


  def generate_output_files(self):
    parsed_df = self.parse()
    self.__generate_output_file(parsed_df, self.raw_parsed_users_file)
    self.__log_output_file(self.raw_parsed_users_file)


  def parse(self):
    self.__log_start()

    final_df = pd.DataFrame()
    file_count = 0

    for file_path in self.users_files:
      self.__log_file_start(file_path)      
      file_count += 1

      parser = UsersParser(file_path, verbose = self.verbose)
      parsed_df = parser.parse()

      final_df = pd.concat(
        [final_df, parsed_df], axis=0, join='outer', ignore_index=False, keys=None,
        levels=None, names=None, verify_integrity=False, copy=True, sort=False
      )
      self.__log_file_end(file_path, file_count)

    self.__log_end()
    return final_df


  ###################
  # Private Methods #
  ###################

  def __users_files(self):
    return glob.glob(f'{ProjectSetup.raw_users_dir}/*.txt')

  def __log_start(self):
    if self.verbose > 0:
      print(f'Starting to parse users files')
      print(f'Files to process: {len(self.users_files)}')

  def __log_file_start(self, file_path):
    if self.verbose > 1:
      print(f'Processing {file_path}')

  def __log_file_end(self, file_path, file_count):
    if self.verbose > 1:
      log_message = f'({file_count}/{len(self.users_files)}) {file_path}'
      print(f'Finished processing - {log_message}')

  def __log_end(self):
    if self.verbose > 0:
      print(f'Finished processing - all files')

  def __generate_output_file(self, parsed_df, file_path):
    parsed_df.to_csv(file_path, index=True, header=True)

  def __log_output_file(self, file_path):
    if self.verbose > 0:
      print(f'Output file created: {file_path}')
