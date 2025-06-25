#!/bin/bash
set -e

# Ustal położenie katalogu projektu
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_DIR=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_DIR"

echo "[LSC] Starting LSC system from: $PROJECT_DIR"

# Tworzymy katalog logs jeśli nie istnieje
mkdir -p logs

# 1. Tworzymy virtualenv jeśli nie istnieje
if [ ! -d "venv" ]; then
    echo "[LSC] Creating Python virtual environment..."
    python3 -m venv venv
fi

# 2. Instalujemy zależności bez aktywacji środowiska
echo "[LSC] Installing dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 3. Uruchamiamy Redis jeśli nie działa
if ! pgrep -x "redis-server" > /dev/null; then
    echo "[LSC] Starting Redis server..."
    redis-server --daemonize yes
else
    echo "[LSC] Redis is already running."
fi

# 4. Uruchamiamy RQ worker w tle
echo "[LSC] Starting RQ worker in background..."
nohup ./venv/bin/python src/run_worker.py > logs/worker.log 2>&1 &

# 5. Uruchamiamy watcher w tle
echo "[LSC] Starting directory watcher in background..."
nohup ./venv/bin/python src/watcher.py > logs/watcher.log 2>&1 &

# 6. Potwierdzenie
echo "[LSC] All components started. Logs in ./logs/"

