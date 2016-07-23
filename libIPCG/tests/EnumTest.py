
from tests.TestBase import TestBase


class EnumTest(TestBase):
    def setUp(self):
        pass

    def test_simpleJava(self):
        javaGen, nativeGen, env, module = self.getEnvFile('EnumSimple.idl')

        enum = module.getType('TestEnum')

        self.saveOutput(javaGen.generateEnumParcelable(enum), '.java')

    def test_simpleNative(self):
        javaGen, nativeGen, env, module = self.getEnvFile('EnumSimple.idl')

        enum = module.getType('TestEnum')

        self.saveOutput(nativeGen.generateEnumHeader(enum), '.h')
