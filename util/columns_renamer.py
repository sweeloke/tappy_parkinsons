# Very simple util class that renames the columns from a pandas dataframe
# to follow a pattern (all downcase and spaces are replaced with underscore)
class ColumnsRenamer:
  # The initializer of the class
  #
  # Input:
  #  - [df]: an instantiated Pandas dataframe to be used by the renaming method
  def __init__(self, df):
    self.df = df

  # Renames the columns from `df` returning the new dataframe
  #
  # Output:
  #  - [df]: the new Pandas dataframe with the renamed columns
  def rename_columns_to_standard_format(self):
    rename_dict = self.__rename_columns_dict()
    return self.df.rename(columns=rename_dict)

  ###################
  # Private Methods #
  ###################

  def __rename_columns_dict(self):
    transform_column_name = lambda column: (column, column.lower().replace(' ', '_'))
    return dict(map(transform_column_name, self.df.columns))
