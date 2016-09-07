import os
import traceback
import unittest

from idl.Environment import Environment

from ipcg.generator.binder.java.JavaGenerator import JavaGenerator
from ipcg.generator.binder.native.NativeGenerator import NativeGenerator


class TestBase(unittest.TestCase):
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    IDL_DIR = os.path.join(SCRIPT_DIR, 'idls')
    OUT_DIR = os.path.join(SCRIPT_DIR, 'out')

    def setUp(self):
        pass

    def getIdlPath(self, relPath):
        return os.path.join(self.IDL_DIR, relPath)

    def getOutPath(self, relPath):
        return os.path.join(self.OUT_DIR, relPath)

    def getEnvFile(self, path):
        javaGen = JavaGenerator()
        nativeGen = NativeGenerator('todo', 'todo', 'todo')
        env = Environment()

        module = env.compileFile(self.getIdlPath(path))

        return javaGen, nativeGen, env, module

    def saveOutput(self, output, suffix=''):
        stack = traceback.extract_stack()

        filename, codeline, funcName, text = stack[-2]

        # Remove test_ prefix
        name = '_'.join(funcName.split('_')[1:]) + suffix

        relPath = os.path.join(os.path.splitext(os.path.basename(filename))[0], name)

        outPath = self.getOutPath(relPath)

        dirPath = os.path.dirname(outPath)
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)

        with open(outPath, 'w') as fileObj:
            fileObj.write(output)
