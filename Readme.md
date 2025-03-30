# Git Status in Subfolders

This Python script (`git-status.py`) provides a convenient way to check the `git status -s` of all Git repositories located in the immediate subfolders of a specified directory. It enhances the output with color-coding for better readability and minimizes unnecessary whitespace.

## Demo

![Image](Resources/Unitled.png)

## Features

* **Iterates through Subfolders:** Recursively checks only the first level subdirectories.
* **Git Status Display:** Executes `git status -s` in each subfolder that is a Git repository.
* **Color-Coded Output:** Uses ANSI escape codes to colorize output for improved clarity (e.g., errors in red, clean status in green).
* **Clean Status Indication:** Explicitly indicates when a repository is clean.
* **Error Handling:** Includes error handling for non-existent directories, Git command failures, and the absence of the Git command.
* **Clear Messages:** Provides informative messages for Git repositories, non-Git directories, and errors.
* **Whitespace Optimization:** Reduces vertical whitespace in the output for a more compact display.

## Requirements

* Python 3.x
* Git (must be installed and accessible in your system's PATH)

## Usage

1.  **Save the script:** Save the Python code as `git-status.py`.
2.  **Run the script:**
    * Navigate to the directory containing the script in your terminal.
    * Execute the script using Python 3:

        ```bash
        python3 git-status.py
        ```
3.  **Optional: Make it executable (Linux/macOS):**
    * Add the shebang line to the beginning of the script: `#!/usr/bin/env python3`
    * Make the script executable: `chmod +x git-status.py`
    * Run it directly: `./git-status.py`

4.  **Specify a different root folder (Optional):**
    * To check Git status in subfolders of a directory other than the current one, provide the directory path as an argument:

        ```bash
        python3 git-status.py /path/to/your/root/directory
        ```

## License

MIT License
