# CapCrackV2

A Python-based tool for modifying the CapCut video editor to enable PRO features. This is achieved by patching the `VECreator.dll` file.

## Features

- **Automatic Process Handling**: Detects and terminates any running instances of `CapCut.exe` before applying modifications.
- **DLL Patching**: Modifies the `VECreator.dll` to unlock features.
- **Backup Management**: Automatically creates backups of the original and the modified DLL (`_Off.dll` and `_On.dll` respectively), allowing users to easily toggle the changes.
- **Watermark Removal**: Deletes the watermark resource folder to prevent watermarks from being applied to exported videos.
- **Interactive UI**: Uses a command-line interface to guide the user through the process.

## Version History

### Version 2.5 (Latest) (BETA)

This version focuses on improving the robustness, maintainability, and user experience of the tool.

**Changes:**
- **Code Refactoring**: The script has been refactored to be more organized and easier to read.
- **Configuration Section**: Hardcoded values such as byte patterns and filenames have been moved to a global configuration section at the top of the file. This makes it significantly easier to update the patch for future versions of CapCut.
- **Improved Error Handling**: Added more specific error messages to help diagnose issues if the patching process fails.
- **Enhanced User Feedback**: The console output is clearer and provides better status updates throughout the process.

### Version 2.0

The initial release of CapCrackV2.

**Features:**
- Provided the core functionality for patching `VECreator.dll`.
- Included process termination and backup creation.
- Patch values were hardcoded directly within the script's functions.

## Requirements

- Python 3.x
- The following Python libraries are required:
  - `rich`
  - `psutil`

You can install them using pip:
```sh
pip install rich psutil
```

## Usage

1.  Ensure all requirements are installed.
2.  Run the script from your terminal:
    ```sh
    python capcrack.py
    ```
3.  Follow the on-screen prompts to select whether to enable or disable the PRO features.

## Disclaimer

This tool is intended for educational purposes only. Modifying software can be against the terms of service of the software provider. Use at your own risk.
