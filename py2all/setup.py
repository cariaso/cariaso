import sys, os
import shutil
from distutils.core import setup


shutil.rmtree('dist', True) 
shutil.rmtree('build', True) 


rawfile = 'demo.py'


options = dict(
    version='0.1',
    name='DemoProg',
    description="opens a demo window",
    author="cariaso",
    author_email="cariaso@yahoo.com",
    url="http://www.promethease.com",
    )


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


    # this allows me to build the dist directory by double clicking setup.py
    sys.argv.append('py2exe')

    extra_options = dict(

        # data_files will be copied into the dist directory, useful for
        # msvcr71.dll, often necessary on very clean windows machines

        data_files = [
        "C:\\WINDOWS\\system32\\msvcr71.dll",
##        'icon1.ico',
##        "C:\\Program Files\\Python25\\lib\\site-packages\\wx-2.8-msw-unicode\\wx\\gdiplus.dll",
##        "C:\\Program Files\\Python25\\lib\\site-packages\\wx-2.8-msw-unicode\\wx\\MSVCP71.dll",
                ],
        options = {"py2exe": {
                        "compressed": 1,
                        "optimize": 1,
                        "ascii": 1,

                        # 3 = no bundling
                        # 1 = bundle as much as possible, which has worked for me sometimes, but seems not to with this tkinter demo app
                        
                        "bundle_files": 3,
                        "packages":["encodings",],
                        'excludes' : [
                                # all of these seem to be frequently added into the dist directory, but are often not needed
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

options.update(extra_options)

setup(**options)



if sys.platform == 'darwin':
    try:
        os.remove('Promethease.dmg')
    except OSError, e:
        print e
    os.system('hdiutil create -imagekey zlib-level=9 -srcfolder dist/Promethease.app Promethease')


elif sys.platform == 'win32':
    os.system('"c:\Program Files\NSIS\makensis.exe" makepromethease.nsi')
