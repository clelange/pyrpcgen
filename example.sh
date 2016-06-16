#!/bin/bash

#Generate the stubs:
mkdir out 2>/dev/null || true

./pyrpcgen example.x out

#Test the portmapper
./test.py testPortMapper

#Test server v2
#python test.py testsrv2 [tcp|udp]
./test.py testsrv2 tcp 55555 &
SERVER_PID=$!
sleep 1

#Check the server registration
./test.py testPortMapper

#Test client v2
#python test.py testclt2 [raw] [tcp|udp] hostname
./test.py testclt2 tcp 127.0.0.1 55555
./test.py testclt2 tcp 127.0.0.1

#note: the raw client does not use the portmapper

#cleanup
kill -SIGUSR1 $SERVER_PID
wait $SERVER_PID
