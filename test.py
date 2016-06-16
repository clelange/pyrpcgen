#!/usr/bin/env python3
from server import exampleProgram as Server
from client import exampleProgram as Client

import sys

def fixDefs():
    global protocol, port, ServerV1, ServerV2, ClientV1, ClientV2
    if protocol == "udp":
        ServerV1 = Server.UDPexampleVersion
        ServerV2 = Server.UDPexampleVersion2

        if port != "mapper":
            ClientV1 = Client.RawUDPexampleVersion
            ClientV2 = Client.RawUDPexampleVersion2
        else:
            ClientV1 = Client.UDPexampleVersion
            ClientV2 = Client.UDPexampleVersion2
    elif protocol == "tcp":
        ServerV1 = Server.TCPexampleVersion
        ServerV2 = Server.TCPexampleVersion2

        if port != "mapper":
            ClientV1 = Client.RawTCPexampleVersion
            ClientV2 = Client.RawTCPexampleVersion2
        else:
            ClientV1 = Client.TCPexampleVersion
            ClientV2 = Client.TCPexampleVersion2
protocol = "tcp"
debug = False
port = "mapper"
fixDefs()
    
def runServer(s):
    s.debug = debug
    def signal_handler(signal, frame):
        print('Intercepting SIGNAL & deregistering')
        s.unregister()
        sys.exit(0)
    import signal
    signal.signal(signal.SIGUSR1, signal_handler)
    try:
        s.unregister()
    except RuntimeError as msg:
        print('RuntimeError:', msg, '(ignored)')
    s.register()
    print('Service started...')
    try:
        s.run(debug)
    except KeyboardInterrupt:
        print('You pressed Ctrl+C!')
        s.unregister()
        sys.exit(0)
    finally:
        s.unregister()
        print('Service interrupted.')

def testsrv(port):
    if port=="mapper":
        port=44444
    class S(ServerV1):
        def __init__(self, *args, **kwargs):
            ServerV1.__init__(self, *args, **kwargs)

        def hello(self):
            print("No message, but life is great!")
            return None
    s = S('localhost', 44444)
    runServer(s)

def testsrv2(port):
    if port=="mapper":
        port=55555
    class S(ServerV2):
        def __init__(self, *args, **kwargs):
            ServerV2.__init__(self, *args, **kwargs)

        def hello(self, message):
            print("Yay! Got a message '%s'" % message)
            return 42

    s = S('localhost', port)
    runServer(s)

def testclt(port):
    import sys
    if sys.argv[1:]: host = sys.argv[1]
    else: host = ''
    # Client for above server
    if port != "mapper":
        c = ClientV1(host, port)
    else:
        c = ClientV1(host)

    c.debug = debug
    print('making call...')
    reply = c.hello()
    print('call returned', repr(reply))

def testclt2(port):
    import sys
    if sys.argv[1:]: host = sys.argv[1]
    else: host = ''
    # Client for above server
    if port != "mapper":
        c = ClientV2(host, port)
    else:
        c = ClientV2(host)

    c.debug = debug
    print('making call...')
    reply = c.hello("Ciao mondo!")
    print('call returned', repr(reply))

import rpc

def testPortMapper():
    pmap = rpc.UDPPortMapperClient('')
    list = pmap.Dump()
    list.sort()
    for prog, vers, prot, port in list:
        print(prog, vers, end=' ')
        if prot == rpc.IPPROTO_TCP: print('tcp', end=' ')
        elif prot == rpc.IPPROTO_UDP: print('udp', end=' ')
        else: print(prot, end=' ')
        print(port)

if __name__ == "__main__":

    def testFunc(x):
        print("""
USAGE: %s [testsrv|testsrv2|testclt|testclt2|testPortMapper] [debug] [tcp|udp] [<port>]
""")

    try:
        if sys.argv[1] == "testsrv":
            testFunc = testsrv
            del sys.argv[1]
        if sys.argv[1] == "testsrv2":
            testFunc = testsrv2
            del sys.argv[1]
        if sys.argv[1] == "testclt":
            testFunc = testclt
            del sys.argv[1]
        if sys.argv[1] == "testclt2":
            testFunc = testclt2
            del sys.argv[1]
        if sys.argv[1] == "testPortMapper":
            testFunc = lambda x: testPortMapper()
            del sys.argv[1]

        if sys.argv[1] == "debug":
            debug = True
            del sys.argv[1]
        if sys.argv[1] == "tcp":
            protocol = "tcp"
            del sys.argv[1]
        if sys.argv[1] == "udp":
            protocol = "udp"
            del sys.argv[1]
        
        try:
            port = int(sys.argv[1])
            del sys.argv[1]
        except ValueError as IndexError:
            port = "mapper"

    except IndexError:
        port = "mapper"
        pass
    
    fixDefs()
    print("prot='%s', port='%s'" % (protocol, port))

    testFunc(port)

