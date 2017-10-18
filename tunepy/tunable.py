class tunable(object):
    def __init__(self, kind, definition=None, **kwargs):
       self.kind = kind
       self.definition = definition
       self.kwargs = kwargs

    @classmethod
    def int(cls, definition=None, **kwargs):
        return cls(int, definition, **kwargs)
    
    @classmethod
    def float(cls, definition=None, **kwargs):
        return cls(float, definition, **kwargs)

    @classmethod
    def list(cls, definition=None, **kwargs):
        return cls(list, definition, **kwargs)
    
    @classmethod
    def bool(cls, definition=None, **kwargs):
        return cls(list, [True, False], **kwargs)
    
    @classmethod
    def str(cls, definition='', **kwargs):
        return cls(str, definition, **kwargs)
