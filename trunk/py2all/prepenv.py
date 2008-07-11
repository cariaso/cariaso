import sys
import tempfile


__VERSION__ = '0.1.23'


def preHack(changeArgv=True):
    import sys
    import os.path
    for path in (
                 'libs/pywikipedia',
                 'libs/pywikipedia/userinterfaces'
                 ):
        if os.path.exists(path):
            print "prepending path %s" % path
            sys.path.insert(0, path)

    try:
        import terminal_interface
        print 'terminal_interface loaded'
    except Exception, e:
        print 'terminal_interface not loaded'
        pass




    dirname=tempfile.mkdtemp()

    if changeArgv:
        sys.argv.append('-dir:%s' % dirname)


    fh = file('%s/user-config.py' % dirname,'w')
    fh.write("""mylang = 'en'
family = 'snpedia'
usernames['snpedia']= {}
usernames['snpedia']['en'] = u'SNPediaBot'
""")
    fh.close()

    try:
        os.mkdir('%s/families' % dirname)
    except Exception, e:
        pass

    sys.path.append(dirname)
    sys.path.append('%s/families' % dirname)

    fh = file('%s/families/snpedia_family.py' % dirname,'w')
    fh.write("""# -*- coding: utf-8  -*-

import family

# SNPedia - a genetics wiki

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)

        self.name = 'snpedia'

        self.langs = {
                'en': 'www.snpedia.com',
        }
        self.namespaces[4] = {
            '_default': [u'SNPedia', self.namespaces[4]['_default']],
        }
        self.namespaces[5] = {
            '_default': [u'SNPedia talk', self.namespaces[5]['_default']],
        }

    def version(self, code):
        return "1.4.2"

    def path(self, code):
        return '/index.php'
""")
    fh.close()

    try:
        import snpedia_family
    except ImportError, e:
        print 'looks like pywikipedia wasn not found'



