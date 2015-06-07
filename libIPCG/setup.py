#!/usr/bin/env python

from distutils.core import setup
from ipcg import tmp


setup(
      name = 'libIPCG',
      
      version = ipcg.tmp.__version__,
      
      description = 'IPC generator tool',
      
      author = 'Nikola Spiric',
      
      author_email = 'nikola.spiric.ns@gmail.com',
      
      package_dir = {'tmp' : 'tmp'},
      
      packages = ['tmp', 'tmp.binder', 'tmp.lang', 'tmp.installer'],
)
