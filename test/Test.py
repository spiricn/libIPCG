from ipcg.binder.BinderGenerator import BinderGenerator


def test():
    out = 'D:/home/dev/workspace/testIPCG'

#     out = 'out'
    
    generator = BinderGenerator(
        out + '/libTestIPCGNative',
        'libTestIPCGNative',
        out + '/libTestIPCGJava',
        'libTestIPCGJava',
    )
    
    print('copmile')
    
    generator.env.compileTree('./idl')
    
    print('generate')
    
    generator.generate()
    
    print('done')

if __name__ == '__main__':
    test()