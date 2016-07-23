
from tests.TestBase import TestBase


class StructTest(TestBase):
    # Simple

    def test_simpleJava(self):
        javaGen, nativeGen, env, module = self.getEnvFile('StructSimple.idl')

        struct = module.getType('TestStruct')

        self.saveOutput(javaGen.generateStructParcelable(struct), '.java')

    def test_simpleNative(self):
        javaGen, nativeGen, env, module = self.getEnvFile('StructSimple.idl')

        struct = module.getType('TestStruct')

        self.saveOutput(nativeGen.generateStructParcelableHeader(struct), '.h')
        self.saveOutput(nativeGen.generateStructParcelableSource(struct), '.cpp')

    # Complex

    def test_complexJava(self):
        javaGen, nativeGen, env, module = self.getEnvFile('StructComplex.idl')

        struct = module.getType('TestStruct')

        self.saveOutput(javaGen.generateStructParcelable(struct), '.java')

    def test_complexNative(self):
        javaGen, nativeGen, env, module = self.getEnvFile('StructComplex.idl')

        struct = module.getType('TestStruct')

        self.saveOutput(nativeGen.generateStructParcelableHeader(struct), '.h')
        self.saveOutput(nativeGen.generateStructParcelableSource(struct), '.cpp')

    # Arrays

    def test_arraysJava(self):
        javaGen, nativeGen, env, module = self.getEnvFile('StructArrays.idl')

        struct = module.getType('TestStruct')

        self.saveOutput(javaGen.generateStructParcelable(struct), '.java')

    def test_arraysNative(self):
        javaGen, nativeGen, env, module = self.getEnvFile('StructArrays.idl')

        struct = module.getType('TestStruct')

        self.saveOutput(nativeGen.generateStructParcelableHeader(struct), '.h')
        self.saveOutput(nativeGen.generateStructParcelableSource(struct), '.cpp')
