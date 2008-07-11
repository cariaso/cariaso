# Cezar
#
# I've begun some commenting and refactorings, if anything seems amiss please check the earliest version from the svn repos
#





    


    

import sys, os
import shutil
from distutils.core import setup

__VERSION__ = '0.1'



shutil.rmtree('dist', True) 
shutil.rmtree('build', True) 




rawfile = 'demo.py'

if sys.platform == 'darwin':
    import ez_setup
    ez_setup.use_setuptools()
    mainscript = rawfile

    import py2app
    sys.argv.append('py2app')
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=dict(argv_emulation=True,
                                 compressed=True,
                                 optimize=2,
                                 #iconfile='icon1.icns',
                                 plist=dict(CFBundleIconFile='icon1.icns'),

                                 )),
        )

elif sys.platform == 'win32':
    
    import py2exe
    sys.argv.append('py2exe')

    datafiles = []
    for f in (
        'icon1.ico',
        "C:\\WINDOWS\\system32\\msvcr71.dll",
        ):
        if os.path.exists(f):
            datafiles.append(f)
           

    extra_options = dict(
        version=__VERSION__,
        description="Makes an html report about genotypes",
        author="cariaso",
        author_email="cariaso@yahoo.com",
        url="http://www.promethease.com",

        # I'm fairly certain this isn't doing anything for me
        data_files=datafiles,

        options = {"py2exe": {
                        "compressed": 1,
                        "optimize": 1,
                        "ascii": 1,

                        # 3 = no bundling
                        # 1 = bundle as much as possible, which has worked for me sometimes, but seems not to with this tkinter demo app
                        
                        "bundle_files": 3,
                        "packages":["encodings",],
                        'excludes' : [
                                #"pywin", "pywin.debugger", "pywin.debugger.dbgcon",
                                #"pywin.dialogs", "pywin.dialogs.list",
                                #"Tkconstants","Tkinter",
                                #"tcl"
                                ]
                        }
                    },
        console=[{"script":rawfile,
                # failing since no icon file
                #"icon_resources": [(1, "icon1.ico")]
                }],
        zipfile=None,
        )

else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install"
        # and install the main script as such
        scripts=[mainscript],
        )

setup(name="Promethease",
      **extra_options
      )



if sys.platform == 'darwin':
    try:
        os.remove('Promethease.dmg')
    except OSError, e:
        print e
    os.system('hdiutil create -imagekey zlib-level=9 -srcfolder dist/Promethease.app Promethease')



