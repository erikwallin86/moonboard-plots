#!/bin/bash

# Setup from https://gist.github.com/mplewis/6076082

# Here's a working uWSGI setup:
# 
#     that communiates with a web server via port 4242
#     for file server.py
#     with app name myapp
# uwsgi --socket 127.0.0.1:4242 --module run_flask --callab app
uwsgi --socket 127.0.0.1:4242 --plugins python --module run_flask --callab app

# I had to install the following, system wide
# python -m pip install flask
# python -m pip install matplotlib
# python -m pip install colorcet

# And the following packages
# sudo pacman -S uwsgi
# sudo pacman -S uwsgi-plugin-python
# sudo pacman -S nginx-mainline

# For nginx, I commented out a 'server' section in the config file  /etc/nginx/nginx.conf
# and started the service as
# sudo systemctl start nginx
# sudo systemctl enable nginx
