import re

# Class responsible for parsing tappy files. It loads the tappy data in memory separating good records (paseable lines)
# and bad records (unparseable lines). The main function here is `parse()` which does the whole heavy-lifting.
#
# The big takeaway here is that all good lines will:
#  - Have the expected user. The one which the file was named after
#  - No null values for any field
#  - No unexpected format for any field
#  - Will be ready to be loaded in a dataframe
class TappyParser:
  # The class initializer
  #
  # Input:
  # - file_path [string]: the full file path of the tappy file that will be parsed
  # - verbose [int]: (optional) the verbosity level. The higher the number, more verbose will be.
  #                  By default, this variable is initialized with 0
  def __init__(self, file_path, verbose=0):
    self.file_path = file_path
    self.verbose = verbose
    self.line_pattern = self.__regex_pattern()

  # Loads the tappy file (from `file_path`) in memory, separating good (parseable) and
  # bad lines (unparseable). The goal is to select which rows/records/lines we can work
  # out of the box because they are respecting the expected format.
  #
  # This strategy was adopted because we noticed a pattern of positional fields and also
  # interruptions in the middle of a line (truncated lines). Most likely due to bugs in the
  # reader/writer from the keyboard to the file, and finaly to the FTP server.
  #
  # Output:
  # - [dict]: dictionary with the keys `good_lines` and `bad_lines`. The values are arrays of strings with each line
  #           from the file (each line as a string)
  def parse(self):
    with open(self.file_path, 'r') as file:
      good_lines = []
      bad_lines = []
      line_number = 0

      lines = file.readlines()
      for line in lines:
        match = re.search(self.line_pattern, line)

        if not match:
          bad_lines.append(line)
          if self.verbose > 1:
            line_to_print = line.replace('\r', '').replace('\n', '')
            line_position = len(good_lines) + len(bad_lines)
            print(f'WARNING: unparseable line at {line_position}: {line_to_print}')
        else:
          good_lines.append(line)

      parsed_lines = {
        'good_lines': good_lines,
        'bad_lines': bad_lines
      }
      return parsed_lines

  ###################
  # Private Methods #
  ###################
  
  # Extracts a hash with the `user_key` and the partial date (YYMM), `year_month` from the file_path
  #
  # Output:
  #  - [dict]: dictionary with the keys `user_key` and `year_month` extracted from the tappy file path
  def __get_metadata_from_file_path(self):
    match = re.match(r'.*/(?P<user_key>\w{10})_(?P<year_month>\d{4}).txt$', self.file_path)
    metadata = {
      'user_key': match.group('user_key'),
      'year_month': match.group('year_month')
    }
    return metadata

  # Generates a regular expression pattern to parse the lines of the file.
  # Uses the `file_path` as part of the expected `user_key` and `date` fields.
  #
  # Output:
  #  - [string]: the regex pattern expected to be matched for all lines of the file
  def __regex_pattern(self):
    metadata = self.__get_metadata_from_file_path()

    user_rex   = f"(?P<user_key>{metadata['user_key']})"
    date_rex   = f"(?P<date>{metadata['year_month']}\d{{2}})"
    ts_rex     = f"(?P<timestamp>\d{{2}}:\d{{2}}:\d{{2}}.\d{{3}})"
    hand_rex   = f"(?P<hand>[RLS])"
    hold_rex   = f"(?P<hold_time>\d{{4,6}}\.\d{{1}})"
    dir_rex    = f"(?P<direction>[RLS]{{2}})"
    lat_rex    = f"(?P<latency_time>\d{{4}}\.\d{{1}})"
    flight_rex = f"(?P<flight_time>\d{{4}}\.\d{{1}})"
    
    return f"^{user_rex}\s+{date_rex}\s+{ts_rex}\s+{hand_rex}\s+{hold_rex}\s+{dir_rex}\s+{lat_rex}\s+{flight_rex}\s*$"
