import os

from mako.template import Template


class AGenerator:
    '''
    Base class for each generator.
    '''
    
    def __init__(self):
        pass
    
    def _getTemplate(self, path):
        '''
        Creates a mako template from given relative file path.
        '''
        
        return Template(filename=os.path.join(os.path.dirname(__file__), 'templates', path))
