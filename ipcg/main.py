from idl.Environment import Environment


src = '''

package com.example;


interface Test{
    int32[] test();
};

'''
    

env = Environment()

module = env.compileSource(src, 'test')

iface = env.types[0]

m = iface.methods[0]

print(m.ret.isArray)



print('done')


