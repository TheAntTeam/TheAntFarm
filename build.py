import os
import argparse


def install_requirements():
    os.system("pip3 install -r requirements.txt")


def build_ui():
    os.system("pyside2-uic the_ant_farm.ui > ui_the_ant_farm.py")


def build_resources():
    os.system("pyside2-rcc app_resources.qrc -o app_resources_rc.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build artifacts for The Ant Farm application.")
    parser.add_argument("operation", choices=["req", "REQ", "ui", "UI", "res", "RES"])

    parsed_args = parser.parse_args()

    operation = parsed_args.operation.lower()
    if operation == "req":
        install_requirements()
    elif operation == "ui":
        build_ui()
    elif operation == "res":
        build_resources()
