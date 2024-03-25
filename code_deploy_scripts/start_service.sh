#!/bin/bash
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl start app.service
