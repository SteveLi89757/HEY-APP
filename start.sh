#!/bin/bash
gunicorn -w 4 app:app
chmod +x start.sh
