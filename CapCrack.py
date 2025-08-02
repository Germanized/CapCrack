import ctypes
import os
import shutil
import sys
import time

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.spinner import Spinner
    from rich.text import Text
except ImportError:
    print("Required libraries are not installed. Please run: pip install rich psutil")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("psutil is not installed. Please run: pip install psutil")
    sys.exit(1)

console = Console()


def get_process_by_name(process_name):
    """Find all processes with a given name."""
    pids = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            pids.append(proc.info['pid'])
    return pids


def terminate_process(pid):
    """Forcefully terminate a process by its PID."""
    try:
        p = psutil.Process(pid)
        p.terminate()
        p.wait()
    except psutil.NoSuchProcess:
        pass  # Process already terminated


def get_exe_path_from_pid(pid):
    """Get the full path of the executable for a given PID."""
    try:
        return psutil.Process(pid).exe()
    except psutil.NoSuchProcess:
        return None


def binary_replace(data, old_bytes, new_bytes):
    """Replace all occurrences of old_bytes with new_bytes in a byte string."""
    return data.replace(old_bytes, new_bytes)


def patch_dll(dll_path, toggle):
    """
    Patches the VECreator.dll file using rich for output.
    """
    try:
        on_path = dll_path + "_On.dll"
        off_path = dll_path + "_Off.dll"

        if not (os.path.exists(on_path) and os.path.exists(off_path)):
            console.print("[yellow]Cracked and uncracked backups not found. Creating them...[/yellow]")
            if not os.path.exists(dll_path):
                console.print(f"[red]Error: {dll_path} not found![/red]")
                return

            with open(dll_path, 'rb') as f:
                original_content = f.read()

            console.print("[cyan]Creating cracked version (_On.dll)...[/cyan]")
            on_content = binary_replace(original_content, b'\x00vip_entrance\x00', b'\x00pro_fortnite\x00')
            with open(on_path, 'wb') as f:
                f.write(on_content)

            console.print("[cyan]Creating uncracked version (_Off.dll)...[/cyan]")
            off_content = binary_replace(original_content, b'\x00pro_fortnite\x00', b'\x00vip_entrance\x00')
            with open(off_path, 'wb') as f:
                f.write(off_content)

            console.print("[bold green]Backup files created.[/bold green]")

        selected_file = on_path if toggle == "on" else off_path
        shutil.copyfile(selected_file, dll_path)
        console.print("[bold green]Changes applied successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]An error occurred while patching the DLL: {e}[bold red]")


def main():
    """Main function for the CapCrack tool, enhanced with rich."""
    ctypes.windll.kernel32.SetConsoleTitleW("CapCrackV2 by Germanized")

    logo = r"""
_________               _________                       __     ____   ____________  
\_   ___ \_____  ______ \_   ___ \____________    ____ |  | __ \   \ /   /\_____  \ 
/    \  \/\__  \ \____ \/    \  \/\_  __ \__  \ _/ ___\|  |/ /  \   Y   /  /  ____/ 
\     \____/ __ \|  |_> >     \____|  | \// __ \\  \___|    <    \     /  /       \ 
 \______  (____  /   __/ \______  /|__|  (____  /\___  >__|_ \    \___/   \_______ \
        \/     \/|__|           \/            \/     \/     \/                    \/
"""
    logo_text = Text(logo, style="bold magenta", justify="center")
    subtitle = Text("By Germanized", style="cyan", justify="center")
    
    console.print(Panel(Text.assemble(logo_text, "\n", subtitle), title="CapCrackV2", border_style="green"))

    program_name = "CapCut.exe"
    
    with console.status("[bold yellow]Searching for CapCut.exe...[/bold yellow]", spinner="dots") as status:
        capcut_pids = get_process_by_name(program_name)
        time.sleep(1) # For effect

    if not capcut_pids:
        console.print("[yellow]No instances of CapCut.exe were found.[/yellow]")
    else:
        console.print(f"[yellow]Found {len(capcut_pids)} instance(s) of CapCut.exe. Closing them...[/yellow]")
        dll_paths = set()
        for pid in capcut_pids:
            exe_path = get_exe_path_from_pid(pid)
            if exe_path:
                exe_dir = os.path.dirname(exe_path)
                dll_path = os.path.join(exe_dir, "VECreator.dll")
                watermark_dir = os.path.join(exe_dir, "Resources", "watermark")

                if os.path.exists(dll_path):
                    dll_paths.add(dll_path)

                if os.path.isdir(watermark_dir):
                    try:
                        shutil.rmtree(watermark_dir)
                        console.print("[green]Deleted watermark folder.[/green]")
                    except Exception as e:
                        console.print(f"[red]Failed to delete watermark folder: {e}[/red]")

            terminate_process(pid)

        with console.status("[bold cyan]Waiting for all instances to close completely...[/bold cyan]", spinner="aesthetic"):
            while get_process_by_name(program_name):
                time.sleep(0.1)
        console.print("[bold green]All instances of CapCut have been closed.[/bold green]")

        if not dll_paths:
            console.print("[bold red]Could not find VECreator.dll in any CapCut installation path.[/bold red]")
        else:
            toggle = Prompt.ask("Enable PRO features?", choices=["on", "off"], default="on")

            for dll_path in dll_paths:
                console.print(Panel(f"[yellow]Patching: {dll_path}[/yellow]", border_style="blue"))
                patch_dll(dll_path, toggle)

    console.print("\n[bold green]Finished. Press Enter to close.[/bold green]")
    input()


if __name__ == "__main__":
    main()
