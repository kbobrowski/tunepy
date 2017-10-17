class tunable(object):
    def __init__(self, kind, definition=None, **kwargs):
       self.kind = kind
       self.definition = definition
       self.kwargs = kwargs

       if kind == bool:
           self.kind = list
           self.definition = [True, False]

       if kind == str:
           if definition is None:
               self.definition = ''
