#!/bin/sh

sleep 20
echo 'Starting stream processor ...'
cd /home/stream-processing/streams.examples
rm -rf target
mvn clean install
ls target/classes
mvn exec:java -Dexec.mainClass="myapps.WordCountApplication"