from distutils.util import strtobool

def to_bool(value, default=False):
    try:
        return strtobool(value)
    except ValueError:
        return default