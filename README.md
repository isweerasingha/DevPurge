# 🧹 DevPurge

A high-performance Python CLI tool for macOS to reclaim disk space by removing heavy folders like `node_modules`, `.next`, `build`, `dist`, `out`, `.turbo`, `__pycache__`, and `target`.



## 🚀 Features
- **Dry Run by Default:** Never delete anything by accident.
- **Selective Deletion:** Choose specific projects to clean using index numbers.
- **Ignore Logic:** Skip specific projects using the `--ignore` flag.
- **Global Access:** Run it from any directory in your terminal.

## 📦 Installation
1. Move `main.py` to `/usr/local/bin/cleaner`
2. Make it executable:
   ```bash
   chmod +x /usr/local/bin/cleaner