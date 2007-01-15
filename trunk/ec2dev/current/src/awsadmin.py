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






import EC2
import sys
import getopt


class Application:
    def __init__(self, opts, args):
 	AWS_ACCESS_KEY_ID = '<INSERT YOUR AWS ACCESS KEY ID HERE>'
        AWS_SECRET_ACCESS_KEY = '<INSERT YOUR AWS SECRET ACCESS KEY HERE>'
 
	terminateIDs=[]
	runIDs=[]
	for o, a in opts:
            if o in ("-a", "--public"):
                AWS_ACCESS_KEY_ID = a
            if o in ("-s", "--private"):
                AWS_SECRET_ACCESS_KEY = a

            if o in ("--terminate-instance", "--terminate"):
                terminateIDs.append(a)
            if o in ("--run-instance", "--run"):
                runIDs.append(a)


        SECURITY_GROUP_NAME = "endog-ec2-example-rb-test-group"
        
        conn = EC2.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        
	if terminateIDs:
	    print "-- terminating %s --" % terminateIDs
	    print conn.terminate_instances(terminateIDs)

	if runIDs:
	    print "-- running %s --" % runIDs
	    for ami in runIDs:
	        print conn.run_instances(ami)


        print "----- listing images -----"
        print conn.describe_images()
        
        print "----- listing instances -----"
        print conn.describe_instances()
        
        print "----- listing security groups -----"
        print conn.describe_securitygroups

        print "----- listing keypairs -----"
        print conn.describe_keypairs()
        
        #print "----- creating a security group -----"
        #print conn.create_securitygroup(SECURITY_GROUP_NAME, "ec-example.rb test group")
        #print "----- deleting a security group -----"
        #print conn.delete_securitygroup(SECURITY_GROUP_NAME)
        


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ha:s:", ["help", 
				"public=", "private=",
				"terminate-instance=", "terminate=",
				"run-instance=", "run=",
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
