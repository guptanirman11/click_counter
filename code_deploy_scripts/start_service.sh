#!/bin/bash
systemctl daemon-reload
systemctl enable app.service
systemctl start app.service
