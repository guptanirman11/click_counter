#!/bin/bash

pip3 install -r /home/ec2-user/app/requirements.txt
cp /home/ec2-user/code_deploy_scripts/app.service /etc/systemd/system/