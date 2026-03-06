# 🚀 FastDevPurge CLI

**FastDevPurge** is a lightning-fast, recursive cleanup utility for macOS developers. It identifies and removes heavy build artifacts and dependency bloat that accumulate over time, reclaiming gigabytes of disk space in seconds.

## 🛠 Supported Artifacts

FastDevPurge targets folders that are **reproducible** (can be recreated by running a build or install command).

| Folder | Description | Project Type |
| --- | --- | --- |
| `node_modules` | External packages/dependencies. | Node.js / Web |
| `.next` | Build output and cache for Next.js. | React / Next.js |
| `build` / `dist` | Compiled production code and assets. | General Web / Apps |
| `out` | Static exported files. | Next.js / Static Sites |
| `.turbo` | Remote and local build cache. | Turborepo |
| `__pycache__` | Compiled Python bytecode. | Python |
| `target` | Compiled binaries and build artifacts. | Rust / Maven |
| `.cache` | Temporary storage for various CLI tools. | General |
| `venv` / `.venv` | Local Python Virtual Environments. | Python |
| `.serverless` | Hidden build data for cloud deployments. | Serverless Framework |

> **💡 Note:** You can easily customize this list by editing the `TARGET_FOLDERS` set at the top of the `main.py` script.

---

## ⚙️ Arguments & Usage

| Argument | Description |
| --- | --- |
| `--run` | **Execute mode.** Without this, the script runs in "Dry Run" (safe) mode. |
| `--ignore [paths]` | Skip specific directories. Supports multiple paths. |
| `--help` / `-h` | Display the manual and version info. |

### Examples

```bash
# Safe scan of the current directory
devpurge

# Delete artifacts in the current project, ignoring the 'Archives' folder
devpurge --run --ignore ./Archives

# Select specific folders to delete by typing their index numbers (e.g., 1, 3, 5)
devpurge --run

```

---

## 📦 Installation

To use FastDevPurge globally from any terminal window, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/isweerasingha/FastDevPurge.git
cd FastDevPurge

```

### 2. Move to Global Bin

Move the script to your local bin and rename it to `devpurge`:

```bash
sudo cp main.py /usr/local/bin/devpurge

```

### 3. Make it Executable

Give your Mac permission to run the script:

```bash
sudo chmod +x /usr/local/bin/devpurge

```