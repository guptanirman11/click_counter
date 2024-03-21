#!/bin/bash

cd /home/ec2-user/app
pip install -r requirements.txt
pip install gunicorn
export FLASK_APP=application:application
gunicorn -b 0.0.0.0:5000 -w 4 application:application