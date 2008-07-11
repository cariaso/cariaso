
import prepenv
    

import sys, os
import shutil
from distutils.core import setup

changeArgv=False
if sys.platform == 'darwin':
    changeArgv=True
    
prepenv.preHack(changeArgv=changeArgv)





shutil.rmtree('dist', True) 
shutil.rmtree('build', True) 




rawfile = 'promethease.py'

if sys.platform == 'darwin':
    import ez_setup
    ez_setup.use_setuptools()
    obfile = 'promethease_ob.py'
    os.system('~/mypy/bin/python2.4 pyobfuscate2 %s > %s' % (rawfile, obfile))
    mainscript = obfile


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


    extra_options = dict(
        version=prepenv.__VERSION__,
        description="Makes an html report about genotypes",
        author="cariaso",
        author_email="cariaso@yahoo.com",
        url="http://www.promethease.com",

        data_files=['icon1.ico',
                    "C:\\WINDOWS\\system32\\msvcr71.dll",
#                    "C:\\Python25\\lib\\site-packages\\wx-2.8-msw-ansi\\wx\\gdiplus.dll",
#                    "C:\\Python25\\lib\\site-packages\\wx-2.8-msw-ansi\\wx\\MSVCP71.dll",

                    "C:\\Program Files\\Python25\\lib\\site-packages\\wx-2.8-msw-unicode\\wx\\gdiplus.dll",
                    "C:\\Program Files\\Python25\\lib\\site-packages\\wx-2.8-msw-unicode\\wx\\MSVCP71.dll",


                    ],
        options = {"py2exe": {
                        "compressed": 1,
                        "optimize": 1,
                        "ascii": 1,
                        "bundle_files": 1,
                        "packages":["encodings",],
                        'excludes' : [
                                "pywin", "pywin.debugger", "pywin.debugger.dbgcon",
                                "pywin.dialogs", "pywin.dialogs.list",
                                "Tkconstants","Tkinter","tcl"
                                ]
                        }
                    },
        console=[{"script":rawfile,
                "icon_resources": [(1, "icon1.ico")]
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


