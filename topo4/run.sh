#!/bin/bash

pkill java
java -jar ../rtr.jar routers h1-hw.txt h1-sw.txt &
java -jar ../rtr.jar routers h2-hw.txt h2-sw.txt &
java -jar ../rtr.jar routers h3-hw.txt h3-sw.txt &
java -jar ../rtr.jar routers h4-hw.txt h4-sw.txt &
java -jar ../rtr.jar routers r1-hw.txt r1-sw.txt &
java -jar ../rtr.jar routers r2-hw.txt r2-sw.txt &
java -jar ../rtr.jar routers r3-hw.txt r3-sw.txt &
java -jar ../rtr.jar routers r4-hw.txt r4-sw.txt &
java -jar ../rtr.jar routers r5-hw.txt r5-sw.txt &
java -jar ../rtr.jar routers r6-hw.txt r6-sw.txt &
java -jar ../rtr.jar routers r7-hw.txt r7-sw.txt &
java -jar ../rtr.jar routers r8-hw.txt r8-sw.txt &
java -jar ../rtr.jar routers r9-hw.txt r9-sw.txt &

echo "Topologia iniciada!"
