# Smart Counter Reader via Nextcloud Integration

## 🎯 Project Goals

This project aims to implement an automated workflow for reading numerical values from photos of utility counters (electricity, water, etc.) using a self-hosted Nextcloud instance. The photos are captured using a smartphone and automatically uploaded to Nextcloud, ensuring local control and privacy.

### 🧠 Core Idea

- Automate data extraction from images of utility counters.
- Support photos taken from multiple flats and of various types of counters.
- Perform processing locally (on CPU), optionally using OpenCV or a lightweight ML model.
- Work either as a Nextcloud automation (e.g., via Flow) or an independent background service on Linux.

---

## ✅ What Has Been Done (Kickstart)

- [x] Installed and configured **Nextcloud** on a local Linux server.
- [x] Uploaded sample **photos** of counters manually.
- [x] Investigated **workflow automation options** in Nextcloud:
  - [Nextcloud Flow](https://nextcloud.com/workflow/)
  - Webhook triggers
  - Cron-based or filesystem-based watchers

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

---

### ⚙️ 4. Run the full system

```bash
./bin/start.sh
```

This will:
- activate the virtual environment,
- install dependencies (if missing),
- start Redis (if not already running),
- launch the RQ worker (in background),
- start the image watcher (foreground).

---

### 📁 Monitored directory

The watcher monitors:

```
/mnt/ncdata/admin/files/Photos
```

All `.jpg`, `.jpeg`, and `.png` images placed in this directory will be:
- enqueued in Redis,
- processed by the worker,
- marked with a `.done` file upon completion.

---

### 📊 Check system activity

```bash
tail -f logs/watcher.log logs/worker.log
```

---

### 🧹 Reset state (optional)

```bash
rm /mnt/ncdata/admin/files/Photos/*.done
redis-cli DEL queued_files
```


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
          ├── Manual/Auto upload
          ├── Workflow Trigger (Flow / inotify / cron)
          ▼
  Counter Reader Script (OpenCV or local ML)
          │
          ▼
   Parsed readings saved to:
   - CSV / JSON
   - Local DB
   - Dashboard (optional)
# private-counter
