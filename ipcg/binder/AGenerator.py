import os

from mako.template import Template


class AGenerator:
    def __init__(self):
        pass
    
    def _getTemplate(self, path):
        return Template(filename=os.path.join(os.path.dirname(__file__), 'templates', path))
