import os
import argparse


def install_requirements():
    """Install required python packages."""
    os.system("pip3 install -r requirements.txt")


def build_ui():
    """Convert UI file to equivalent python code."""
    os.system("PySide6-uic the_ant_farm.ui > ui_the_ant_farm.py")


def clean_ui():
    """Remove python file generated from UI file."""
    os.remove("ui_the_ant_farm.py")


def build_resources():
    """Convert QRC resource file to python code."""
    os.system("PySide6-rcc app_resources.qrc -o app_resources_rc.py")


def clean_resources():
    """Remove python file generated from QRC resource file."""
    os.remove("app_resources_rc.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build artifacts for The Ant Farm application.")
    parser.add_argument("operation", choices=["req", "REQ", "ui", "UI", "res", "RES", "clean", "CLEAN", "all", "ALL"])

    parsed_args = parser.parse_args()

    operation = parsed_args.operation.lower()
    if operation == "req":
        install_requirements()
    elif operation == "ui":
        build_ui()
    elif operation == "res":
        build_resources()
    elif operation == "all":
        install_requirements()
        build_ui()
        build_resources()
    elif operation == "clean":
        clean_ui()
        clean_resources()
