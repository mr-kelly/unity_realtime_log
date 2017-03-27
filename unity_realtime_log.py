#coding=utf-8

COMMENT = """
 ##############################################
##                                            ##
##            Peilin Kelly Chan               ##
##     <https://github.com/mr-kelly>          ##
##            <23110388@qq.com>               ##
##                                            ##
##     a cross-platform build script for      ##
##  Unity3D console mode realtime log output  ##
##                                            ##
##                                            ##
 ##############################################
"""


import platform
import time
import fileinput
import subprocess
import os
import sys
import thread
import time
import tail




def tail_thread(tail_file):

    print "wait for tail file ... %s" % tail_file

    while True:
        if os.path.exists(tail_file):
            print "Start tail file..... %s" % tail_file
            break

    t = tail.Tail(tail_file)
    t.register_callback(unity_log_tail)
    t.follow(s=1)

def unity_log_tail(txt):
    print(txt)

def build(method, unity_path, project_path, log_path):
    """
    call unity process to build
    """

    build_cmd = [unity_path, '-batchmode', '-projectPath', project_path, '-nographics', '-executeMethod', method, '-logFile', log_path, '-quit']
    print 'Unity running ....'

    if os.path.exists(log_path):
        os.remove(log_path)
        print 'delete %s' % log_path

    # new thread to tail log file
    thread.start_new_thread(tail_thread, (log_path, ))

    process = subprocess.Popen(
        build_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=project_path
    )

    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            sys.stdout.write("[Unity process console output]: " + out)
            sys.stdout.flush()

    time.sleep(5)
    print 'done!'





def fullpath(path):
    return os.path.abspath(os.path.expanduser(path))

if __name__ == '__main__':
    print COMMENT
    import argparse
    parser = argparse.ArgumentParser(description=u'Unity realtime log printing build!')

    parser.add_argument('-unity', required=True, help=u'Unity executable file path')
    parser.add_argument('-project', required=True, help=u'Unity project path')
    parser.add_argument('-method', required=True, help=u'Unity method to call')

    args = parser.parse_args()
    build(args.method, fullpath(args.unity), fullpath(args.project), fullpath(os.path.join(args.project, '__kellylog.txt')))
