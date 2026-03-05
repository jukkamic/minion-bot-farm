## 🚨 CRITICAL WARNING: System Requirements Warning 🚨

**Running this container chokes your harddrive**

**This project requires at least 5GB to 10GB of free disk space.** While the Minion scripts themselves are tiny, this Dev Container downloads heavy AI infrastructure to run locally:
* **Docker WSL2 Virtual Disk:** ~3GB+ overhead.
* **PyTorch & AI Libraries:** ~2.5GB.
* **Local HuggingFace Models:** ~100MB.

Do not spin up this container if your hard drive is critically full!

## ⚠️ Data Persistence & Docker Volumes 

**DO NOT rely on your local hard drive as a backup for this project.**

This project is built using VS Code Dev Containers. If you use the "Clone Repository in Container Volume" feature, your code does **not** live in a normal folder on your Windows/Mac host machine. 

Instead, the entire codebase lives inside a **Docker Named Volume** (a virtual Linux hard drive managed by Docker). 

**What this means for you:**
* If you uninstall Docker, you lose the code.
* If you run `docker system prune --volumes`, you lose the code.
* If you purge Docker data to free up disk space, **the entire project is permanently deleted.**

**Best Practice:**
Treat the local Dev Container as highly volatile, temporary workspace. **Push your code to GitHub constantly.** If your local Docker environment crashes or needs to be purged, you can simply delete the volume, re-clone from GitHub, and the container will rebuild itself perfectly in minutes.