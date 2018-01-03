#!/usr/bin/env python
'''
# This file may be used instead of Apache mod_wsgi to run your python
# web application in a different framework.  A few examples are
# provided (cherrypi, gevent), but this file may be altered to run
# whatever framework is desired - or a completely customized service.
'''
import imp
import os
import sys

try:
    VIRT_ENV = os.path.join(os.environ.get('PYTHON_DIR', '.'), 'virtenv')
    PYTHON_VERSION = "python"+str(sys.version_info[0])+"."+str(sys.version_info[1])
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(VIRT_ENV, 'lib', PYTHON_VERSION, 'site-packages')
    VIRTUAL_ENV = os.path.join(VIRT_ENV, 'bin', 'activate_this.py')
    exec(open(VIRTUAL_ENV).read(), dict(__file__=VIRTUAL_ENV))

except IOError:
    pass

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
#
#  main():
#
import socket
import atexit

@atexit.register
def exit():
    print('Exiting WSGIServer type %s on %s:%d ... ' % (FWTYPE, IP, PORT))

if __name__ == '__main__':
    APPLICATION = imp.load_source('app', 'main.py')
    PORT = APPLICATION.app.config['PORT']
    IP = APPLICATION.app.config['IP']
    APP_NAME = APPLICATION.app.config['APP_NAME']
    HOST_NAME = APPLICATION.app.config['HOST_NAME']

    FWTYPE = "wsgiref"
    for fw in ("gevent", "cherrypy", "flask"):
        try:
            imp.find_module(fw)
            FWTYPE = fw
        except ImportError:
            pass

    hostname=socket.gethostname()
    IPAddr=socket.gethostbyname(hostname)
    print("Your Computer Name is:"+hostname)
    print("Your Computer IP Address is:"+IPAddr)

    print('Starting WSGIServer type %s on %s:%d ... ' % (FWTYPE, IP, PORT))
    if FWTYPE == "flask":
        from flask import Flask
        SERVER = Flask(__name__)
        SERVER.wsgi_app = APPLICATION.app
        SERVER.run(host=IP, port=PORT)
    else:
        from wsgiref.simple_server import make_server
        make_server(IP, PORT, APPLICATION.app).serve_forever()
