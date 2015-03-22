import os

from mako.template import Template


class AGenerator:
    '''
    Base class for each generator.
    '''
    
    def __init__(self, templatesDir):
        self._templatesDir = templatesDir
    
    def _getTemplate(self, path):
        '''
        Creates a mako template from given relative file path.
        '''
        
        return Template(filename=os.path.join(os.path.dirname(__file__), self._templatesDir, path))
