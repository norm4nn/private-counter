#!/bin/bash
set -e

# Ustal położenie katalogu projektu
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_DIR=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_DIR"

# Zatrzymaj wszystkie procesy uruchomione przez run_worker.py
pkill -f "$SCRIPT_DIR/run_worker.py"