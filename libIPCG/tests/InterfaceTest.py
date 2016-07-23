
from tests.TestBase import TestBase


class InterfaceTest(TestBase):
    def setUp(self):
        pass

    # Simple

    def test_simpleJava(self):
        javaGen, nativeGen, env, module = self.getEnvFile('InterfaceSimple.idl')

        iface = module.getType('TestInterface')

        self.saveOutput(javaGen.generateInterfaceAIDL(iface), '.java')

    def test_simpleNative(self):
        javaGen, nativeGen, env, module = self.getEnvFile('InterfaceSimple.idl')

        iface = module.getType('TestInterface')

        self.saveOutput(nativeGen.generateInterfaceHeader(iface), '.h')
        self.saveOutput(nativeGen.generateInterfaceBnHeader(iface), '_bn.h')
        self.saveOutput(nativeGen.generateInterfaceBpSource(iface), '_bp.cpp')
        self.saveOutput(nativeGen.generateInterfaceBnSource(iface), '_bn.cpp')

    # Complex

    def test_complexJava(self):
        javaGen, nativeGen, env, module = self.getEnvFile('InterfaceComplex.idl')

        iface = module.getType('TestInterface')

        self.saveOutput(javaGen.generateInterfaceAIDL(iface), '.java')

    def test_complexNative(self):
        javaGen, nativeGen, env, module = self.getEnvFile('InterfaceComplex.idl')

        iface = module.getType('TestInterface')

        self.saveOutput(nativeGen.generateInterfaceHeader(iface), '.h')
        self.saveOutput(nativeGen.generateInterfaceBnHeader(iface), '_bn.h')
        self.saveOutput(nativeGen.generateInterfaceBpSource(iface), '_bp.cpp')
        self.saveOutput(nativeGen.generateInterfaceBnSource(iface), '_bn.cpp')


    # Arrays


    def test_arraysJava(self):
        javaGen, nativeGen, env, module = self.getEnvFile('InterfaceArrays.idl')

        iface = module.getType('TestInterface')

        self.saveOutput(javaGen.generateInterfaceAIDL(iface), '.java')

    def test_arraysNative(self):
        javaGen, nativeGen, env, module = self.getEnvFile('InterfaceArrays.idl')

        iface = module.getType('TestInterface')

        self.saveOutput(nativeGen.generateInterfaceHeader(iface), '.h')
        self.saveOutput(nativeGen.generateInterfaceBnHeader(iface), '_bn.h')
        self.saveOutput(nativeGen.generateInterfaceBpSource(iface), '_bp.cpp')
        self.saveOutput(nativeGen.generateInterfaceBnSource(iface), '_bn.cpp')
