#!/usr/bin/env python
# http://www.cariaso.com
# http://code.google.com/p/cariaso/

"""

Prerequisites:

An Amazon Web Services Developer account signed up for Amazon EC2.


Dependencies:

The ElementTree XML library <http://effbot.org/zone/element-index.htm> is
required for versions of Python prior to 2.5.  From version 2.5, the Python
standard library includes ElementTree and it does not have to be installed
separately.

"""





import S3
import EC2
import sys
import getopt
import os




class Application:
    def __init__(self, opts, args):

 	AWS_ACCESS_KEY_ID = ""
        AWS_SECRET_ACCESS_KEY = ""

        if os.environ.has_key('AWS_ACCESS_KEY_ID'):
            AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

        if os.environ.has_key('AWS_SECRET_ACCESS_KEY'):
            AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
 
	terminateIDs=[]
	runIDs=[]
	deregisterIDs=[]
	deleteBuckets=[]

	for o, a in opts:
            if o in ("-h", "--help"):
                raise Usage()


            if o in ("-a", "--public"):
                AWS_ACCESS_KEY_ID = a
            if o in ("-s", "--private"):
                AWS_SECRET_ACCESS_KEY = a

            if o in ("--terminate-instance", "--terminate"):
                terminateIDs.append(a)
            if o in ("--run-instance", "--run"):
                runIDs.append(a)

            if o in ("--deregister-image"):
                deregisterIDs.append(a)

            if o in ("--delete-bucket"):
                deleteBuckets.append(a)


        connEC2 = EC2.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        connS3  = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        
	if terminateIDs:
	    print "-- terminating %s --" % terminateIDs
	    print connEC2.terminate_instances(terminateIDs)

	if runIDs:
	    print "-- running %s --" % runIDs
	    for ami in runIDs:
	        print connEC2.run_instances(ami)

	if deregisterIDs:
	    print "-- deregistering %s --" % deregisterIDs
	    for ami in deregisterIDs:
	        print connEC2.deregister_image(ami)


	conn = connS3

	if deleteBuckets:
	    for name in deleteBuckets:
	        print "-- not-yet deleting %s --" % name		


        print "----- listing images -----"
        print connEC2.describe_images(owners=['self'])
        
        print "----- listing instances -----"
        print connEC2.describe_instances()
        
        #print "----- listing security groups -----"
        #print connEC2.describe_securitygroups

        print "----- listing keypairs -----"
        print connEC2.describe_keypairs()

        print "----- buckets ------"
        for bucket in connS3.list_all_my_buckets().entries:
	    print bucket.creation_date, bucket.name


        

class Usage(Exception):
    def __init__(self, msg=None):
        if msg:
            self.msg = msg
        else:
            self.msg = """\
%(self-name)s -a AWS_ACCESS_KEY_ID -s AWS_SECRET_ACCESS_KEY

or you can set environment variables and omit the -a and -s switches
set AWS_ACCESS_KEY_ID=MY_KEY_ID
set AWS_SECRET_ACCESS_KEY=MY_SECRET_KEY

%(self-name)s

%(self-name)s --run-instance ami-123456
%(self-name)s --run ami-123456

%(self-name)s --terminate-instance i-123456
%(self-name)s --terminate i-123456
""" % {'self-name':'awsadmin.py'}



def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ha:s:", ["help", 
				"public=", "private=",
				"terminate-instance=", "terminate=",
				"run-instance=", "run=",
				"deregister-image=",
				"delete-bucket=",
				])
        except getopt.error, msg:
             raise Usage(msg)
	Application(opts, args)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
