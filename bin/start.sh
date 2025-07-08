#!/bin/bash
set -e

WORKER_COUNT=1
while [[ $# -gt 0 ]]; do
  case "$1" in
    --workers)
      WORKER_COUNT="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

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


# 3. Uruchamiamy RQ worker w tle
echo "[LSC] Starting $WORKER_COUNT RQ workers in background..."
for i in $(seq 1 ${WORKER_COUNT:-1}); do
    nohup python $PROJECT_DIR/lib/run_worker.py > logs/worker_$i.log 2>&1 &
done

# Potwierdzenie
echo "[LSC] All components started. Logs in ./logs/"

