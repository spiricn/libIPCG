
from ipcg.generator.binder.BinderGenerator import BinderGenerator
from tests.TestBase import TestBase


class ProjectTest(TestBase):
    def setUp(self):
        pass

    def test_project(self):
        generator = BinderGenerator(self.getOutPath('Project/native'),
                                    'libTest',
                                    self.getOutPath('Project/java'),
                                    'com.example.test',
                                    self.getOutPath('Project/build'))

        generator.env.compileTree(self.getIdlPath('project'))

        generator.generate()
