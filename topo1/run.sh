#!/bin/bash

pkill java
java -jar ../rtr.jar routers h1-hw.txt h1-sw.txt &
java -jar ../rtr.jar routers r1-hw.txt r1-sw.txt &
java -jar ../rtr.jar routers h2-hw.txt h2-sw.txt &
