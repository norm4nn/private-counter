# Smart Counter Reader via Nextcloud Integration

## 🎯 Project Goals

This project aims to implement an automated workflow for reading numerical values from photos of utility counters (
electricity, water, etc.) using a self-hosted Nextcloud instance. The photos are captured using a smartphone and
automatically uploaded to Nextcloud, ensuring local control and privacy.

### 🧠 Core Idea

- Automate data extraction from images of utility counters.
- Support photos taken from multiple flats and of various types of counters.
- Perform processing locally (on CPU), optionally using OpenCV or a lightweight ML model.
- Work either as a Nextcloud automation (e.g., via Flow) or an independent background service on Linux.

---

## ✅ What Has Been Done

- [x] Installed and configured **Nextcloud** on a local Linux server.
- [x] Uploaded sample **photos** of counters manually.
- [x] Investigated **workflow automation options** in Nextcloud:
    - [Nextcloud Flow](https://nextcloud.com/workflow/)
    - Webhook triggers
    - Cron-based or filesystem-based watchers
- [x] Trained custom version of **YOLOv8** for digit detection
- [x] Implemented Redis-based **task queue** for processing images
- [x] Integrated task queue through a custom **NextCloud ExApp** 

---

## 🚀 Installation and Startup

### ✅ Requirements

- Linux with shell access (bash)
- Python 3.10+
- Redis (locally or in a container)
- Nextcloud with a mounted image folder, e.g., `/mnt/ncdata/admin/files/Photos`

---

### 🧰 1. Clone the repository

```bash
git clone https://github.com/norm4nn/private-counter.git
cd private-counter
```

---

### 🧪 2. Create and activate the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 🔧 3. Start Redis (if not running)

```bash
redis-server --daemonize yes
```

or if using Docker:

```bash
docker compose up -d redis
```

---

### ⚙️ 4. Run the startup script

```bash
export APP_ID=private_counter
export APP_PORT=9031
export APP_SECRET=12345
export APP_VERSION=1
export NEXTCLOUD_USER='admin'
export NEXTCLOUD_URL='http://127.0.0.1:8080'
./bin/start.sh [--workers <num_workers>]
```

This will:

- create and activate the virtual environment,
- install dependencies (if missing),
- launch the RQ workers (in background),

---

### Start APP:

```bash
export APP_ID=private_counter
export APP_PORT=9031
export APP_SECRET=12345
export APP_VERSION=1
export NEXTCLOUD_USER='admin'
export NEXTCLOUD_URL='http://127.0.0.1:8080'
cd lib && uvicorn main:APP --port 9031 --reload
```

Then register the app in Nextcloud:

```bash
make register
```

and go to the Apps and enable the "Private Counter" app.

### 📁 Monitored directory

The following settings can be adjusted on ExApp Settings page in Nextcloud:
- Directory to monitor for new images
- Time interval for checking new images
- Enabled/disabled state of the monitoring

### 📊 Check system activity

```bash
tail -f logs/worker_1.log
```

---

## 🧪 Expected Outcome

- 📦 A GitHub repository with:
    - This `README.md`
    - A directory for scripts and ML/OpenCV logic
    - Defined [issues](https://github.com/) to track individual tasks
- 🧾 Counter readings exported to a structured format (CSV, JSON, or a small database)
- 🧠 Basic counter detection & digit extraction workflow
- 🧪 Demo with large dataset of pre-existing photos
- 💬 Ongoing discussion with supervisor/teacher on progress and direction

---

## ⚙️ Architecture Overview

```text
Smartphone (Nextcloud App)
          │
          ▼
     Nextcloud Server
     (Linux, CPU only)
          │
          ▼
     Nextcloud ExApp
          ├── Workflow (Asyncio + Redis)
          ▼
  Counter Reader Script (YOLOv8)
          │
          ▼
   Parsed readings saved to:
   - CSV
   - Local DB
```
