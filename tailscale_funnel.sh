#!/bin/bash

# Enable funnel on localhost:2001
tailscale funnel localhost:2001

# Keep the script running indefinitely
tail -f /dev/null
