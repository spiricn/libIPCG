import os

from ipcg.generator.binder.BinderGenerator import BinderGenerator

def exampleMain():
    # Current directory
    exampleDirectory = os.path.dirname(__file__)

    # Generator output directory
    outDirectory = os.path.join(exampleDirectory, 'out')

    nativeLibraryName = 'libIPCGExampleNative'

    javaLibraryName = 'libIPCGExapleJava'

    nativeProjectDirectory = os.path.join(outDirectory, nativeLibraryName)

    javaProjectDirectory = os.path.join(outDirectory, javaLibraryName)

    # Temporary build directory
    buildDirectory = os.path.join(exampleDirectory, 'build_tmp')

    # Create generator
    generator = BinderGenerator(
        nativeProjectDirectory,
        nativeLibraryName,
        javaProjectDirectory,
        javaLibraryName,
        buildDirectory
    )

    # Compile source code
    generator.env.compileTree('./idl')

    # Generate code
    result = generator.generate()

    print('%d installed / %d deleted ( %d up-to-date )' % (result.numFilesInstalled, result.numFilesDeleted, result.numFilesUpToDate))

if __name__ == '__main__':
    exampleMain()
