#!/bin/bash

# Run the Server
python3 manage.py runserver

# Enable funnel on localhost:2001
tailscale funnel 8000

# Keep the script running indefinitely
tail -f /dev/null
