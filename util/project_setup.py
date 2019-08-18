# In this class we basically centralize the directories from where
# we read and write the dataset used in the project. In the long-
# term, we might want/need to introduce more configuration variables,
# but for now, this was enough.
#
# TODO: consider migrating from a class to a JSON or YAML config file.
class ProjectSetup:
  # This is our main configuration variable. Please ensure you are
  # pointing to the correct directory
  home_dir = '/content/gdrive/My Drive/tappy_parkinsons'
  data_dir = f'{home_dir}/data'
  raw_downloaded_dir = f'{data_dir}/raw_downloaded'
  raw_tappy_dir = f'{raw_downloaded_dir}/Tappy Data'
  raw_users_dir = f'{raw_downloaded_dir}/Archived users'
