#!/usr/bin/python
"""This is a simple markdown readme generator. It walks through the directory it is in,
imports every module/package in the directory and dumps the documentation of every source file
in a readme file in that directory"""
import os
import importlib
import types
if __name__ == '__main__':
    rootdir = os.getcwd()
    rootname = rootdir[rootdir.rfind('/')+1:]
    pkg = dict()
    for root, dirs, files in os.walk(rootdir):
        if root.find('.git') == -1:
            packagename = root.replace(rootdir, '')
            if packagename == '':
                packagename = root[root.rfind('/')+1:]
            packagename = packagename.strip('/')
            packagename = packagename.replace('/','.')
            modules = dict()

            for package in dirs:
                try:
                    pkg[package] = __import__(package)
                except ImportError, e:
                    #print 'could not import', package, e
                    pass
                except ValueError:
                    pass

            for module in files:
                try:
                    if packagename != rootname:
                        modules[module] = __import__(packagename+'.'+module[:module.find('.')],globals(), locals(), files, -1)
                    else:
                        modules[module] = __import__(module[:module.find('.')], globals(), locals(), files, -1)
                except ImportError,e :
                    #print 'could not import', module, e
                    pass
                except ValueError:
                    pass

            if len(modules) > 1 or len(pkg) >1:
                readme = open(root+'/README.md', 'wb')
                readme.write('\n')
                readme.write(packagename+'\n')
                readme.write('='*len(packagename)+'\n')
                readme.write('\n')
                if '__init__.py' in modules and modules['__init__.py'].__doc__!= None:
                    readme.write(modules['__init__.py'].__doc__+'\n')

                for module in modules:
                    if module != '__init__.py' and module.find('.pyc') == -1:
                        readme.write('\n')
                        readme.write(module+'\n')
                        readme.write('-'*len(module)+'\n')
                        if modules[module].__doc__ != None:
                            readme.write('\n')
                            readme.write(modules[module].__doc__+'\n')
                        for func in modules[module].__dict__:
                            if isinstance(modules[module].__dict__[func], types.FunctionType) and modules[module].__dict__[func].__doc__ != None:
                                readme.write('\n')
                                readme.write('###'+func+'###'+'\n')
                                readme.write('\n')
                                readme.write(modules[module].__dict__[func].__doc__+'\n')
                readme.close()