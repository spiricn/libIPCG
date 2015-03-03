from ipcg.binder.BinderGenerator import BinderGenerator


def test():
#     out = 'D:/home/dev/workspace/testIPCG'

    out = '/home/nikola/prog/workspace/LAOSP_5.0.0.R7/external/test'
    
    generator = BinderGenerator(
        out + '/libTestIPCGNative',
        'libTestIPCGNative',
        out + '/libTestIPCGJava',
        'libTestIPCGJava',
    )
    
    generator.env.compileTree('./idl')
    
    result = generator.generate()
    
    print('%d installed / %d deleted ( %d up-to-date )' % (result.numFilesInstalled, result.numFilesDeleted, result.numFilesUpToDate))
    
if __name__ == '__main__':
    test()