class OpenStruct(object):
    """Malleable class objects to Forge with."""
    
    def __init__(self, **dict):
        self.__dict__.update(dict)
    
    def __getattr__(self, key):
        return self.__dict__[key]
    
    def __setattr__(self, key, value):
        self.__dict__.update({key: value})