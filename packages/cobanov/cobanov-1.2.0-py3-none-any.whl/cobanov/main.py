import sys
import argparse
import psutil
import subprocess
import platform


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
                print(
                    f"Device: {device.device_node}, Manufacturer: {device.attributes.get('manufacturer')}, Product: {device.attributes.get('product')}"
                )
        except ImportError:
            print(
                "pyudev is not installed. Please install it using 'pip install pyudev'"
            )
    else:
        print("This functionality is only available on Linux.")


def show_temperature():
    if platform.system() == "Linux":
        try:
            sensors_output = subprocess.check_output(
                ["sensors"], universal_newlines=True
            )
            print(sensors_output)
        except FileNotFoundError:
            print(
                "sensors command is not found. Please install it using your package manager."
            )
    else:
        print("This functionality is only available on Linux.")


def show_disk_usage():
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        print(
            f"Partition: {partition.device}, Total: {usage.total / (1024 ** 3):.2f} GB, Used: {usage.used / (1024 ** 3):.2f} GB, Free: {usage.free / (1024 ** 3):.2f} GB, Percentage: {usage.percent}%"
        )


def main():
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
        print("Watching for changes...")
        # Add your watch functionality here

    if args.list_usb:
        list_usb_devices()

    if args.temperature:
        show_temperature()

    if args.disk_usage:
        show_disk_usage()


if __name__ == "__main__":
    main()
