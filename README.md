# CapCrack

A Python CapCut cracking tool by Germanized

## What is this?

This is a Python  CapCrack tool that lets you unlock premium features in CapCut video editor. The script modifies CapCut's DLL files to enable pro features and remove watermarks without paying.

## Requirements

- Python 3.6+
- psutil library
- Windows OS with CapCut installed

## How to use

1. Install the required library:
```
pip install psutil
```

2. Run the script:
```
python capcrack.py
```

3. Type "on" to enable premium features or "off" to disable them

4. The script will:
   - Find and close any running CapCut instances
   - Locate the VECreator.dll file
   - Create backup copies
   - Patch the DLL to enable/disable pro features
   - Remove watermark folders
   
5. Start CapCut after the script finishes

## How it works

The script simply finds specific byte patterns in the CapCut DLL and replaces "vip_entrance" with "pro_fortnite" to trick the software into enabling premium features. It also deletes the watermark folder to prevent export watermarks.

## Warning

Use at your own risk. This is for educational purposes only. I'm not responsible if you break something or violate CapCut's terms of service.

## Notes

- Rounded text boxes in the terminal
- Color-coded status messages
- Simplified interface

## Credits

Original concept by Germanized
