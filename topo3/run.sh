#!/bin/bash

pkill java
java -jar ../rtr.jar routers h1-hw.txt h1-sw.txt &
java -jar ../rtr.jar routers h2-hw.txt h2-sw.txt &
java -jar ../rtr.jar routers h3-hw.txt h3-sw.txt &
java -jar ../rtr.jar routers r1-hw.txt r1-sw.txt &
java -jar ../rtr.jar routers r2-hw.txt r2-sw.txt &
java -jar ../rtr.jar routers r3-hw.txt r3-sw.txt &
java -jar ../rtr.jar routers r4-hw.txt r4-sw.txt &
echo "Topologia iniciada!"

