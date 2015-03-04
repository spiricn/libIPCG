#!/usr/bin/env python

from distutils.core import setup

import idl

setup(
      name = 'libIPCG',
      
      version = idl.__version__,
      
      description = 'IPC generator tool',
      
      author = 'Nikola Spiric',
      
      author_email = 'nikola.spiric.ns@gmail.com',
      
      package_dir = {'ipcg' : 'ipcg'},
      
      packages = ['ipcg', 'ipcg.binder', 'ipcg.lang', 'ipcg.installer'],
)
