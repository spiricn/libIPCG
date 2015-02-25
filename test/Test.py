from ipcg.binder.BinderGenerator import BinderGenerator


def test():
    out = 'Z:spiric/bytel/Lollipop/external/test'

#     out = 'C:/Users/Nikola/Desktop/wavt'
    
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