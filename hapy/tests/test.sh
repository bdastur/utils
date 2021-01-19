#!/bin/bash

retcode=${1:-0}

echo "This is a test command"
sleep 1
echo "We wait for some time and do something"
sleep 4
echo "hello 1"
sleep 1
echo "hello 2"
echo "Ret code exit: $retcode"
exit $retcode
