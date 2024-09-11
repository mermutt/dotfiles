#!/usr/bin/env python2.7

"""
Launches lldb and sends lldb a command to start the test app.
"""

import sys
from argparse import ArgumentParser

def launch_lldb_and_test_program(lldb_command, exe, exe_options):
    import pexpect, time

    prompt = "\(lldb\) "
    lldb = pexpect.spawn(lldb_command)
    # Turn on logging for what lldb sends back.
    lldb.logfile_read = sys.stdout
    lldb.expect(prompt)

    # Now issue the file command.
    #print "sending 'file %s' command..." % exe
    lldb.sendline('file %s' % exe)
    lldb.expect(prompt)

    lldb.sendline('b PC_UT_Debug_Dump' )
    lldb.expect(prompt)

    #print "sending 'process launch -- %s' command..." % (exe_options)
    lldb.sendline('process launch -- %s' % exe_options)

    while True:
        lldb.timeout=5000
        index = lldb.expect( ['Process .* exited with status = 0', 'Process .* exited with status', 'Process .* stopped', pexpect.TIMEOUT] )

        if index == 0:
            sys.exit(0)
        elif index == 1:
            sys.exit(1)
        elif index == 2:
            lldb.expect(prompt)
            lldb.sendline('udsdump' )
            lldb.expect(prompt)
            lldb.expect(prompt)
            lldb.sendline('continue' )
        elif index == 3:
            print "TIMEOUT occurred:", str(lldb)        
            lldb.sendcontrol('c' )
            lldb.expect(prompt)
            lldb.sendline('udsdump' )
            lldb.expect(prompt)
            lldb.expect(prompt)
            lldb.sendline('exit' )
            sys.exit(1)

    # Give control of lldb shell to the user.
    #lldb.interact()

def main():

    parser = ArgumentParser( usage='' )
    parser.add_argument( 'executable', help='(Mandatory) The executable to launch via lldb.' )
    parsed, options = parser.parse_known_args()

    if not parsed.executable:
        parser.print_help()
        sys.exit(1)

    string = ''
    for i in options:
        string = string + i + ' '

    launch_lldb_and_test_program( 'lldb', parsed.executable, string )

if __name__ == '__main__':
    main()
