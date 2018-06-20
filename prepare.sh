#!/bin/bash

touch .env

grep "^UID=" .env &> /dev/null
if [ "$?" == "1" ]; then
  echo "UID=`id -u`" >> .env
fi
