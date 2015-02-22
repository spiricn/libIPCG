from ipcg.binder.BinderGenerator import BinderGenerator


def test():
    generator = BinderGenerator(
        'out/libTestIPCGNative',
        'libTestIPCGNative',
        'out/libTestIPCGJava',
        'libTestIPCGJava',
    )
    
    print('copmile')
    
    generator.env.compileTree('./idl')
    
    print('generate')
    
    generator.generate()

if __name__ == '__main__':
    test()