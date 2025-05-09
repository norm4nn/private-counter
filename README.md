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

- [ ]Installed and configured **Nextcloud** on a local Linux server.
- [ ] Uploaded sample **photos** of counters manually.
- [ ] Investigated **workflow automation options** in Nextcloud:
  - [Nextcloud Flow](https://nextcloud.com/workflow/)
  - Webhook triggers
  - Cron-based or filesystem-based watchers

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
