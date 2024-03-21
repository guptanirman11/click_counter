#!/bin/bash

pip3 install -r /home/ec2-user/app/requirements.txt
export FLASK_APP=application:application
cp /home/ec2-user/app/scripts/app.service /etc/systemd/system/