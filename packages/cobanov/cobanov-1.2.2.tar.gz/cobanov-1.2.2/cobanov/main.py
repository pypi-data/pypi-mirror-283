import sys
import argparse
import psutil
import subprocess
import platform
import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()


def list_usb_devices():
    if platform.system() == "Linux":
        try:
            import pyudev

            context = pyudev.Context()
            usb_devices = [
                device
                for device in context.list_devices(subsystem="usb")
                if device.device_type == "usb_device"
            ]
            for device in usb_devices:
                console.print(
                    f"[bold green]Device:[/bold green] {device.device_node}, "
                    f"[bold blue]Manufacturer:[/bold blue] {device.attributes.get('manufacturer')}, "
                    f"[bold magenta]Product:[/bold magenta] {device.attributes.get('product')}"
                )
        except ImportError:
            console.print(
                "[bold red]pyudev is not installed. Please install it using 'pip install pyudev'"
            )
    else:
        console.print("[bold red]This functionality is only available on Linux.")


def show_temperature():
    if platform.system() == "Linux":
        try:
            sensors_output = subprocess.check_output(
                ["sensors"], universal_newlines=True
            )
            console.print(sensors_output)
        except FileNotFoundError:
            console.print(
                "[bold red]sensors command is not found. Please install it using your package manager."
            )
    else:
        console.print("[bold red]This functionality is only available on Linux.")


def show_disk_usage():
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        console.print(
            f"[bold green]Partition:[/bold green] {partition.device}, "
            f"[bold blue]Total:[/bold blue] {usage.total / (1024 ** 3):.2f} GB, "
            f"[bold magenta]Used:[/bold magenta] {usage.used / (1024 ** 3):.2f} GB, "
            f"[bold cyan]Free:[/bold cyan] {usage.free / (1024 ** 3):.2f} GB, "
            f"[bold yellow]Percentage:[/bold yellow] {usage.percent}%"
        )


def main():
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console)],
    )
    log = logging.getLogger("rich")

    parser = argparse.ArgumentParser(description="Cobanov command line tool")
    parser.add_argument("--watch", action="store_true", help="Watch for changes")
    parser.add_argument(
        "--list-usb", action="store_true", help="List connected USB devices"
    )
    parser.add_argument(
        "--temperature", action="store_true", help="Show system temperature"
    )
    parser.add_argument(
        "--disk-usage", action="store_true", help="Show available disk sizes"
    )
    args = parser.parse_args()

    if args.watch:
        log.info("Watching for changes...")
        # Add your watch functionality here

    if args.list_usb:
        list_usb_devices()

    if args.temperature:
        show_temperature()

    if args.disk_usage:
        show_disk_usage()


if __name__ == "__main__":
    main()
