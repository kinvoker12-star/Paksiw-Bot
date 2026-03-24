#!/bin/bash

echo "=== STARTING BUILD PROCESS ==="

# 1. Siguroha nga ang pip updated ug i-install ang requirements
# Gigamit nato ang python3.12 kay mao ni ang default sa Vercel karon
python3.12 -m pip install -r requirements.txt

# 2. I-collect ang tanang Static Files (CSS, JS, Images)
# Kinahanglan ni para sa WhiteNoise aron dili "plain text" ang imong site
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear

# 3. I-update ang Database schema sa Neon
# Importante ni para mahimo ang imong ChatMessage tables
echo "Running database migrations..."
python3.12 manage.py migrate --noinput

echo "=== BUILD FINISHED ==="