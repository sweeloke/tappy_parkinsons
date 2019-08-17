import pandas as pd
pd.set_option('display.max_columns', 10)

class ProjectSetup:
  home_dir = '/content/gdrive/My Drive/project_scs3253'
  data_dir = f'{home_dir}/data'
  raw_downloaded_dir = f'{data_dir}/raw_downloaded'
  raw_tappy_dir = f'{raw_downloaded_dir}/Tappy Data'
  raw_users_dir = f'{raw_downloaded_dir}/Archived users'