import os
import sys
import shutil
import time
import ctypes
import psutil
from pathlib import Path
import re

def find_program_processes(program_name):
    """Find all processes with the given name and return their PIDs."""
    pids = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == program_name.lower():
                pids.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return pids

def force_close_processes(pids):
    """Force close all processes with the given PIDs."""
    for pid in pids:
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=3)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            try:
                process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"Failed to terminate process with PID {pid}")

def get_exe_path_from_pid(pid):
    """Get the executable path for a given process ID."""
    try:
        process = psutil.Process(pid)
        return process.exe()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print(f"Failed to get process path for PID {pid}")
        return ""

def binary_replace(data, from_bytes, to_bytes):
    """Replace all occurrences of from_bytes with to_bytes in data."""
    result = data.replace(from_bytes, to_bytes)
    return result

def save_edited_file(output_path, content):
    """Save the content to the specified output path."""
    try:
        with open(output_path, 'wb') as file:
            file.write(content)
    except Exception as e:
        raise RuntimeError(f"Failed to open the output file for writing: {output_path}. Error: {str(e)}")

def create_toggled_dll_files(dll_path, original_content):
    """Create both on and off versions of the DLL file."""
    print("Editing files...")

    on_content = original_content
    off_content = original_content
    
    print("Making cracked...")
    on_content = binary_replace(on_content, 
                               b'\x00vip_entrance\x00', 
                               b'\x00pro_fortnite\x00')

    print("Making uncracked...")
    off_content = binary_replace(off_content, 
                                b'\x00pro_fortnite\x00', 
                                b'\x00vip_entrance\x00')

    save_edited_file(f"{dll_path}_On.dll", on_content)
    save_edited_file(f"{dll_path}_Off.dll", off_content)

    print("Files created successfully.")

def edit_dll_file(dll_path, toggle_pro_properties):
    """Edit the DLL file based on the toggle setting."""
    try:
        on_path = f"{dll_path}_On.dll"
        off_path = f"{dll_path}_Off.dll"

        if os.path.exists(on_path) and os.path.exists(off_path):
            selected_file = on_path if toggle_pro_properties == "on" else off_path
            shutil.copy2(selected_file, dll_path)
            print("Changes applied successfully.")
            return

        print("Cracked and uncracked files not found. Creating them...\nReading File...")

        with open(dll_path, 'rb') as file:
            dll_content = file.read()

        create_toggled_dll_files(dll_path, dll_content)
        
        os.remove(dll_path)
        
        selected_file = on_path if toggle_pro_properties == "on" else off_path
        shutil.copy2(selected_file, dll_path)

        print("Changes applied successfully.")
    except Exception as e:
        print(f"An error occurred while editing the DLL file: {str(e)}")

def draw_rounded_box(text, width=None, padding=1):
    """Draw a rounded box around the text."""
    lines = text.strip().split('\n')
    if width is None:
        width = max(len(line) for line in lines)
    
    padded_lines = [' ' * padding + line + ' ' * (width - len(line) + padding) for line in lines]
    
    top = '╭' + '─' * (width + padding * 2) + '╮'
    bottom = '╰' + '─' * (width + padding * 2) + '╯'
    middle = ['│' + line + '│' for line in padded_lines]
    
    return '\n'.join([top] + middle + [bottom])

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color=None):
    """Print colored text in Windows command prompt."""
    colors = {
        'reset': 7,
        'black': 0,
        'blue': 1,
        'green': 2,
        'cyan': 3,
        'red': 4,
        'purple': 5,
        'yellow': 6,
        'white': 7,
        'bright_black': 8,
        'bright_blue': 9,
        'bright_green': 10,
        'bright_cyan': 11,
        'bright_red': 12,
        'bright_purple': 13,
        'bright_yellow': 14,
        'bright_white': 15,
    }
    
    if os.name == 'nt':
        handle = ctypes.windll.kernel32.GetStdHandle(-11)  
        if color:
            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, colors.get(color, 7))
        print(text)
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, colors['reset'])
    else:
        ansi_colors = {
            'reset': '\033[0m',
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'bright_black': '\033[90m',
            'bright_red': '\033[91m',
            'bright_green': '\033[92m',
            'bright_yellow': '\033[93m',
            'bright_blue': '\033[94m',
            'bright_purple': '\033[95m',
            'bright_cyan': '\033[96m',
            'bright_white': '\033[97m',
        }
        if color:
            print(f"{ansi_colors.get(color, '')}{text}{ansi_colors['reset']}")
        else:
            print(text)

def main():
    program_name = "CapCut.exe"
    
    clear_screen()
    
    header = "CapCrack By Germanized"
    print_colored(draw_rounded_box(header, padding=2), "bright_cyan")
    print()
    
    options = "Type \"on\" or \"off\" (CASE SENSITIVE):"
    print_colored(draw_rounded_box(options, padding=1), "bright_green")
    print()
    
    toggle_pro_properties = input("➤ ")

    if toggle_pro_properties not in ["on", "off"]:
        print_colored(draw_rounded_box("Invalid option! Please use 'on' or 'off'.", padding=1), "bright_red")
        input("Press Enter to exit...")
        return

    print_colored(draw_rounded_box("Searching for CapCut processes...", padding=1), "bright_yellow")
    caput_pids = find_program_processes(program_name)
    dll_paths = set()

    if not caput_pids:
        print_colored(draw_rounded_box("No instances of CapCut.exe were found.", padding=1), "bright_red")
        input("Press Enter to exit...")
        return

    print_colored(draw_rounded_box(f"Found {len(caput_pids)} CapCut processes.", padding=1), "bright_green")
    
    for pid in caput_pids:
        exe_path = get_exe_path_from_pid(pid)
        if exe_path:
            exe_folder_path = os.path.dirname(exe_path)
            dll_path = os.path.join(exe_folder_path, "VECreator.dll")
            watermark_folder_path = os.path.join(exe_folder_path, "Resources", "watermark")

            if os.path.exists(dll_path):
                dll_paths.add(dll_path)
                
            if os.path.exists(watermark_folder_path) and os.path.isdir(watermark_folder_path):
                try:
                    shutil.rmtree(watermark_folder_path)
                    print_colored(draw_rounded_box("Deleted watermarks.", padding=1), "bright_green")
                except Exception as e:
                    print_colored(draw_rounded_box(f"Failed to delete watermark folder: {watermark_folder_path}. Error: {str(e)}", padding=1), "bright_red")

    print_colored(draw_rounded_box("Closing all CapCut processes...", padding=1), "bright_yellow")
    force_close_processes(caput_pids)

    print_colored(draw_rounded_box("Waiting for all instances to close completely...", padding=1), "bright_yellow")
    while find_program_processes(program_name):
        time.sleep(0.1)
    print_colored(draw_rounded_box("All instances of CapCut have been closed.", padding=1), "bright_green")

    for dll_path in dll_paths:
        print_colored(draw_rounded_box(f"Processing DLL: {dll_path}", padding=1), "bright_cyan")
        edit_dll_file(dll_path, toggle_pro_properties)

    print_colored(draw_rounded_box("Finished! CapCut has been successfully modified.", padding=1), "bright_green")
    input("Press Enter to close...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_colored(draw_rounded_box(f"An error occurred: {str(e)}", padding=1), "bright_red")
        input("Press Enter to exit...")