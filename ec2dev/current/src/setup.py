from distutils.core import setup
import py2exe
import sys




try:
    import py2exe
except Exception, e:
    print e
    print 'Download py2exe at http://www.py2exe.org/'
    pause = raw_input()
    sys.exit()

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")






setup(name="AWSadmin",
      version="0.1",
      author="http://code.google.com/p/cariaso/",
      console=[{
        "script":'awsadmin.py',
        #"icon_resources":[(1, "icons/Broom.ico")],
      }],
      options = {"py2exe": {"compressed": 1,
                            "optimize": 2,
                            "ascii": 1,
                            "bundle_files": 1,
                            "packages": ['encodings'],
                            }},
      zipfile = None,
      )


