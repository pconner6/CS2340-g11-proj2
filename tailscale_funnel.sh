#!/bin/bash

# Kill other processes
pkill -f tailscale_funnel.sh & nohup

# Run the Server
python3 manage.py runserver

# Enable funnel on 8000
tailscale funnel 8000

# Keep the script running indefinitely
tail -f /dev/null
