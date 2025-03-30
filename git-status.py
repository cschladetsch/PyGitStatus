#!/usr/bin/env python3

import os
import subprocess

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def git_status_in_subfolders(root_folder="."):
    try:
        if not os.path.exists(root_folder):
            print(f"{Colors.RED}Error: Root folder '{root_folder}' does not exist.{Colors.RESET}")
            return

        for item in os.listdir(root_folder):
            item_path = os.path.join(root_folder, item)
            if os.path.isdir(item_path) and item != ".":
                git_dir = os.path.join(item_path, ".git")
                if os.path.exists(git_dir) and os.path.isdir(git_dir):
                    print(f"{Colors.BLUE}{item_path}:{Colors.RESET}", end='')
                    try:
                        process = subprocess.run(
                            ["git", "status", "-s"],
                            cwd=item_path,
                            capture_output=True,
                            text=True,
                            check=True,
                        )
                        if process.stdout:
                            print(process.stdout, end='') #print without extra newline.
                        else:
                            print(f"{Colors.GREEN}Clean{Colors.RESET}") #indicate clean repository.

                    except subprocess.CalledProcessError as e:
                        print(f"{Colors.RED}Error: git status failed in '{item_path}': {e}{Colors.RESET}")
                    except FileNotFoundError:
                        print(f"{Colors.RED}Error: git command not found.{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}'{item_path}' is not a git repository.{Colors.RESET}")

    except Exception as e:
        print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.RESET}")

if __name__ == "__main__":
    git_status_in_subfolders()
