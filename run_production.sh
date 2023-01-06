#!/bin/bash

# Setup from https://gist.github.com/mplewis/6076082
uwsgi --socket 127.0.0.1:4242 --plugins python --module run_flask --callab app
