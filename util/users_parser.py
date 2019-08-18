import re, glob
import numpy as np
import pandas as pd

class UsersParser:
  USERS_COLUMN_TYPES = {
    'Gender'       : 'str',
    'BirthYear'    : 'int64', 
    'Parkinsons'   : 'bool',
    'Tremors'      : 'bool',
    'DiagnosisYear': 'int64', 
    'Sided'        : 'category',
    'UPDRS'        : 'str',
    'Impact'       : 'str',
    'Levadopa'     : 'bool',
    'DA'           : 'bool',
    'MAOB'         : 'bool',
    'Other'        : 'bool',
  }
  USERS_COLUMN_NAMES = USERS_COLUMN_TYPES.keys()

  def __init__(self, file_path, verbose=0):
    self.file_path = file_path
    self.verbose = verbose


  # Parses the given file in the `file_path` (instance variable), returning a
  # pandas dataframe with a new row representing the extracted user.
  #
  # Output:
  #  - [pandas.dataframe] the dataframe with the extracted user
  def parse(self):
    index_list = [] 
    user_key = self.__get_user_key_from_file_path()
    index_list.append(user_key)
    temp_df = pd.DataFrame(np.nan, index=index_list, columns=self.USERS_COLUMN_NAMES)

    if self.verbose > 1:
      print(f'Parsing {self.file_path}')

    with open(self.file_path, 'r') as file:
      lines = file.readlines()
      for line in lines:                    
        match = re.search(r'.+(?<=: ).+.', line)

        if (match):
          data = match.group(0).split(": ")
          temp_df.loc[user_key, data[0]] = data[1]

    if self.verbose > 2:
      print(f'Parsed data:\n {temp_df}')

    return temp_df


  ###################
  # Private Methods #
  ###################

  # Extracts the `user_key` from the file `file_path` (instance variable) being parsed.
  #
  # Output:
  #  - [string]: the extracted `user_key`
  def __get_user_key_from_file_path(self):
    match = re.match(r'.*/User_(?P<user_key>\w{10}).txt$', self.file_path)
    return match.group('user_key')
