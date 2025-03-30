#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

def symbol_for_status(status):
    """
    Given a two-character git status code, return an extra symbol.
    """
    if status == "??":
        return f"{Colors.YELLOW}+{Colors.RESET}"
    elif status[0] != " ":
        code = status[0]
        if code == "A":
            return f"{Colors.GREEN}?{Colors.RESET}"
        elif code == "M":
            return f"{Colors.MAGENTA}?{Colors.RESET}"
        elif code == "D":
            return f"{Colors.RED}?{Colors.RESET}"
        elif code == "R":
            return f"{Colors.CYAN}?{Colors.RESET}"
        elif code == "C":
            return f"{Colors.CYAN}?{Colors.RESET}"
        else:
            return f"{Colors.RED}{code}{Colors.RESET}"
    elif status[1] != " ":
        code = status[1]
        if code == "M":
            return f"{Colors.MAGENTA}?{Colors.RESET}"
        elif code == "D":
            return f"{Colors.RED}?{Colors.RESET}"
        else:
            return f"{Colors.RED}{code}{Colors.RESET}"
    return " "

def git_status_in_subfolders(root_folder="."):
    try:
        if not os.path.exists(root_folder):
            print(f"{Colors.RED}Error: Root folder '{root_folder}' does not exist.{Colors.RESET}")
            return

        # Iterate over each item in the root folder.
        for item in os.listdir(root_folder):
            item_path = os.path.join(root_folder, item)
            if os.path.isdir(item_path) and item != ".":
                git_dir = os.path.join(item_path, ".git")
                if os.path.exists(git_dir) and os.path.isdir(git_dir):
                    try:
                        process = subprocess.run(
                            ["git", "status", "-s"],
                            cwd=item_path,
                            capture_output=True,
                            text=True,
                            check=True,
                        )
                        output = process.stdout.strip()
                        if output == "":
                            # Clean repository: use a green tick as prefix.
                            prefix = f"{Colors.GREEN}\u2713{Colors.RESET}   "
                            print(f"{prefix}{Colors.BLUE}{item_path}:{Colors.RESET}")
                        else:
                            # Dirty repository: use a red cross as prefix.
                            prefix = f"{Colors.RED}\u2717{Colors.RESET}   "
                            print(f"{prefix}{Colors.BLUE}{item_path}:{Colors.RESET}")
                            for line in output.splitlines():
                                if len(line) >= 2:
                                    status_code = line[:2]
                                    file_info = line[3:]
                                    extra_symbol = symbol_for_status(status_code)
                                    print(f"    {extra_symbol} {file_info}")
                                else:
                                    print(f"    {line}")
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
