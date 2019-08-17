from util.project_setup import ProjectSetup
from util.tappy_parser import TappyParser
import glob

class TappyFilesParser:
  def __init__(self, error_threshold=0.06, verbose=1):
    self.verbose = verbose
    self.error_threshold = error_threshold
    self.tappy_files = self.__tappy_files()
    
    self.parsed_lines = {}
    self.good_lines_output_file = f'{ProjectSetup.data_dir}/good_lines.txt'
    self.bad_lines_output_file = f'{ProjectSetup.data_dir}/bad_lines.txt'
    
  def generate_output_files(self):
    if len(self.parsed_lines) == 0:
      self.parse()

    self.__generate_output_file(self.parsed_lines['good_lines'], self.good_lines_output_file)
    self.__log_output_file(self.good_lines_output_file)
    
    self.__generate_output_file(self.parsed_lines['bad_lines'], self.bad_lines_output_file)
    self.__log_output_file(self.bad_lines_output_file)

  def parse(self):
    self.__log_start()

    all_good_lines = []
    all_bad_lines = []
    file_count = 0

    for file_path in self.tappy_files:
      self.__log_file_start(file_path)
      file_count += 1

      parser = TappyParser(file_path)
      parsed_lines = parser.parse()
    
      all_bad_lines.extend(parsed_lines['bad_lines'])
      all_good_lines.extend(parsed_lines['good_lines'])

      self.__log_file_end(file_path, parsed_lines, file_count)
      self.__assert_error_threshold(file_path, parsed_lines)


    self.parsed_lines = {
      'good_lines': all_good_lines,
      'bad_lines': all_bad_lines
    }
    self.__log_end(self.parsed_lines)
    
    return self.parsed_lines
  
  ###################
  # Private Methods #
  ###################
  
  def __tappy_files(self):
    return glob.glob(f'{ProjectSetup.raw_tappy_dir}/*.txt')
  
  def __log_start(self):
    if self.verbose > 0:
      print(f'Starting to parse tappy files')
      print(f'Files to process: {len(self.tappy_files)}')
      
  def __log_file_start(self, file_path):
    if self.verbose > 1:
      print(f'Processing {file_path}')
      
  def __log_file_end(self, file_path, parsed_lines, file_count):
    if self.verbose > 1:
      log_message = f'({file_count}/{len(self.tappy_files)}) {file_path}'
      self.__log_stats(parsed_lines, log_message)
      
  def __log_end(self, parsed_lines):
    if self.verbose > 0:
      self.__log_stats(parsed_lines, 'all files')
      
  def __log_stats(self, parsed_lines, log_message):
    good_lines_count = len(parsed_lines['good_lines'])
    bad_lines_count = len(parsed_lines['bad_lines'])
    total_lines_count = good_lines_count + bad_lines_count
    error_percentage = self.__error_percentage(parsed_lines)

    print(f'Finished processing - {log_message}')
    print(f'  - Lines processed: {total_lines_count}')
    print(f'  - Unparseable lines: {bad_lines_count}')
    print(f'  - Error percentage: {error_percentage}%')
      
  def __error_percentage(self, parsed_lines):
    bad_lines_count = len(parsed_lines['bad_lines'])
    good_lines_count = len(parsed_lines['good_lines'])
    lines_count = good_lines_count + bad_lines_count
    
    error_percentage = 0.0
    if lines_count > 0:
      error_percentage = round((float(bad_lines_count) / float(lines_count)) * 100, 4)
      
    return error_percentage
  
  def __assert_error_threshold(self, file_path, parser_lines):
    error_perc = self.__error_percentage(parser_lines)
    threshold_perc = self.error_threshold * 100
    
    message = f'File {file_path} has an error rate of {error_perc}% which is higher than {threshold_perc}%. Aborting the parse.'
    assert (error_perc < threshold_perc), message
    
  def __generate_output_file(self, lines, file_path):
    with open(file_path, 'w+') as file:
      for line in lines:
        file.write(f'{line}')

  def __log_output_file(self, file_path):
    if self.verbose > 0:
      print(f'Output file created: {file_path}')