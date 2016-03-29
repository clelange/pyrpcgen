#!/bin/bash

#Generate the stubs:

./pyrpcgen example.x .

#Test the portmapper
python test.py testPortMapper

#Test server v2
#python test.py testsrv2 [tcp|udp]
python test.py testsrv2 tcp 55555 &
SERVER_PID=$!
sleep 1

#Check the server registration
python test.py testPortMapper

#Test client v2
#python test.py testclt2 [raw] [tcp|udp] hostname
python test.py testclt2 tcp 127.0.0.1 55555
python test.py testclt2 tcp 127.0.0.1

#note: the raw client does not use the portmapper

#cleanup
kill -SIGUSR1 $SERVER_PID
wait $SERVER_PID
