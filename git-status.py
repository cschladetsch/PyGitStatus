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

def symbol_for_status(status_code):
    """
    Given a two-character git status code (e.g. '??', 'M ', ' M'), return an extra symbol.
    The first character is index status, the second is working tree status.
    """
    code = status_code.replace(' ', '')  # Remove any spaces, leaving only letters or '?'.
    if code == "??":
        return f"{Colors.YELLOW}+{Colors.RESET}"  # untracked
    if "A" in code:
        return f"{Colors.GREEN}?{Colors.RESET}"   # added
    if "M" in code:
        return f"{Colors.MAGENTA}?{Colors.RESET}" # modified
    if "D" in code:
        return f"{Colors.RED}?{Colors.RESET}"     # deleted
    if "R" in code:
        return f"{Colors.CYAN}?{Colors.RESET}"    # renamed
    if "C" in code:
        return f"{Colors.CYAN}?{Colors.RESET}"    # copied
    # Fallback symbol for anything else:
    return f"{Colors.RED}{code}{Colors.RESET}"

def parse_short_status(line):
    """
    Parse a 'git status -s' line (e.g. '?? .venv/', ' M main.cpp').
    Returns a tuple (status_code, file_path).
    """
    # The first 2 characters are the status code; the remainder is the file path.
    status_code = line[:2]
    file_path = line[2:].strip()  # remove leading/trailing spaces from the remainder
    return status_code, file_path

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
                    # Run 'git status -s' in this subfolder.
                    try:
                        process = subprocess.run(
                            ["git", "status", "-s"],
                            cwd=item_path,
                            capture_output=True,
                            text=True,
                            check=True,
                        )
                        output = process.stdout.strip()

                        if not output:
                            # Clean repo: print with a green tick.
                            prefix = f"{Colors.GREEN}\u2713{Colors.RESET}  "
                            print(f"{prefix}{Colors.BLUE}{item_path}:{Colors.RESET}")
                        else:
                            # Dirty repo: print with a red cross.
                            prefix = f"{Colors.RED}\u2717{Colors.RESET}  "
                            print(f"{prefix}{Colors.BLUE}{item_path}:{Colors.RESET}")

                            # List changed files with extra symbols.
                            for line in output.splitlines():
                                if len(line) >= 2:
                                    status_code, file_info = parse_short_status(line)
                                    extra_symbol = symbol_for_status(status_code)
                                    print(f"   {extra_symbol} {file_info}")
                                else:
                                    # If for some reason we get a weird line, just print it indented.
                                    print(f"   {line}")

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
