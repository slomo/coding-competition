#! /bin/bash

echo "START" > $2

read LINE < $1

if [[ $LINE = "Hello, World" ]]; then
    echo "OK" > $2
    exit;
else
    exit -1;
fi

