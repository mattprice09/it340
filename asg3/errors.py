import json


class Asg3Error(Exception):
  """
    Custom error handling to avoid messy printing and sys.exit calls
    in the main program.
  """


  def __init__(self, error_type):
    error_types = self.load_json_file('resources/error_types.json')

    if error_type not in error_types:
      # error...invalid error.
      msg = error_types['invalid_error']
    else:
      msg = error_types[error_type]
    msg = '\n'.join(msg)

    super(Asg3Error, self).__init__(msg)


  def load_json_file(self, fp):
    """ Load json from file """
    with open(fp, 'rU') as data:
      return json.load(data)
