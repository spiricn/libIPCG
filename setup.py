#!/usr/bin/env python

import ipcg


from setuptools import setup, find_packages


setup(
      name = 'libIPCG',
      
      description = 'IPC generator tool',
      
      author = 'Nikola Spiric',
      
      author_email = 'nikola.spiric.ns@gmail.com',
      
      package_dir = {'ipcg' : 'ipcg'},
      
      packages=find_packages(),
)
