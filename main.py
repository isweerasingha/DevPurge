#!/usr/bin/env python3

import os
import shutil
import sys


TARGET_FOLDERS = {
    "node_modules",
    ".next",
    "build",
    "dist",
    "out",
    ".turbo",
    "__pycache__",
    "target",
    ".cache",
    ".serverless",
    ".docusaurus",
    "venv",
    ".venv",
}

# ANSI Colors -  macOS Terminal
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
END = "\033[0m"


def show_help():
    """Displays the manual for the cleaner tool."""
    print(
        f"""
{BOLD}{BLUE}DevPurge CLI{END}
{BOLD}Usage:{END} devpurge [OPTIONS]

{BOLD}Options:{END}
  {GREEN}--run{END}          Execute deletion (Default is DRY RUN).
  {GREEN}--ignore [PL]{END}  List of absolute or relative paths to skip.
  {GREEN}--help, -h{END}     Show this help message.

{BOLD}Examples:{END}
  devpurge --run
  devpurge --run --ignore ./MyProject ../OldWork
    """
    )
    sys.exit(0)


def parse_args():
    """Parses sys.argv for flags and paths."""
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()

    dry_run = "--run" not in sys.argv

    ignore_paths = set()
    if "--ignore" in sys.argv:
        idx = sys.argv.index("--ignore")
        for p in sys.argv[idx + 1 :]:
            if p.startswith("--"):
                break
            ignore_paths.add(os.path.abspath(p))

    return dry_run, ignore_paths


def scan_system(root, ignore_paths):
    """Walks the directory tree and finds targets."""
    found = []
    print(f"{YELLOW}🔍 Scanning from: {root}...{END}")

    for current_root, dirs, _ in os.walk(root):
        # Prune ignored paths
        current_abs = os.path.abspath(current_root)
        if any(current_abs.startswith(ignore) for ignore in ignore_paths):
            dirs[:] = []  # Stop looking inside this folder
            continue

        for folder in dirs[:]:
            if folder.lower() in TARGET_FOLDERS:
                full_path = os.path.join(current_root, folder)
                found.append(full_path)

                # Skip sub folders
                dirs.remove(folder)

    return found


def delete_items(paths):
    """Safely deletes the list of paths provided."""

    total = len(paths)
    success_count = 0

    print(f"\n{BOLD}Starting Deletion Process...{END}\n")

    for i, path in enumerate(paths, 1):
        # --- Calculate Progress Bar ---
        bar_length = 30
        filled_length = int(round(bar_length * i / float(total)))
        percent = round(100.0 * i / float(total), 1)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)

        # \r allows us to overwrite the same line in the terminal
        sys.stdout.write(
            f"\r{BOLD}[{bar}] {percent}%{END} | Current: {os.path.basename(path)} "
        )
        sys.stdout.flush()

        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            success_count += 1
        except Exception as e:
            print(f"\n{RED}Error deleting {path}:{END} {e}")

    print(f"\n{BOLD}{GREEN}Successfully cleaned {success_count} items.{END}")


def main():
    try:
        dry_run, ignore_paths = parse_args()
        root_path = os.getcwd()

        found_folders = scan_system(root_path, ignore_paths)

        if not found_folders:
            print(f"{GREEN}Everything is clean! No target folders found.{END}")
            return

        print(f"\n{BOLD}--- Scan Results ({len(found_folders)} items) ---{END}")
        for i, path in enumerate(found_folders, 1):
            print(f"{BLUE}{i}.{END} {path}")

        if dry_run:
            print(
                f"\n{YELLOW}💡 NOTE: This was a DRY RUN. Use {GREEN}--run{YELLOW} to delete.{END}"
            )
        else:
            print(f"\n{BOLD}Confirm Deletion:{END}")
            print(f" > Press {GREEN}'y'{END} for all")
            print(f" > Press {RED}'n'{END} to cancel")
            print(f" > Enter numbers (e.g. {BLUE}1,3,4{END}) for specific folders")

            choice = input(f"\n{BOLD}Choice:{END} ").strip().lower()

            if choice == "y":
                delete_items(found_folders)
            elif choice == "n" or not choice:
                print("Cancelled.")
            else:
                # Handle selective numeric input
                try:
                    indices = [
                        int(i.strip()) - 1
                        for i in choice.split(",")
                        if i.strip().isdigit()
                    ]
                    to_delete = [
                        found_folders[i] for i in indices if 0 <= i < len(found_folders)
                    ]
                    if to_delete:
                        delete_items(to_delete)
                    else:
                        print("No valid numbers selected.")
                except ValueError:
                    print("Invalid input format.")

    except KeyboardInterrupt:
        print(f"\n\n{RED}Operation stopped by user.{END}")
        sys.exit(0)


if __name__ == "__main__":
    main()
