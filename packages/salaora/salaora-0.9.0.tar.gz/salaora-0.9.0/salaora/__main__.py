import os
from pathlib import Path

MANAGE_PATH = Path(__file__).parent.joinpath("manage.py")

def runserver():
    os.system(f"python {MANAGE_PATH} makemigrations reservations")
    os.system(f"python {MANAGE_PATH} makemigrations vehicles")
    os.system(f"python {MANAGE_PATH} migrate")
    os.system(f"python {MANAGE_PATH} runserver 0.0.0.0:8000")

def create_admin():
    os.system(f"python {MANAGE_PATH} createsuperuser")
    exit()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--create-admin", action="store_true", help="create the admin user")
    args = parser.parse_args()

    if args.create_admin:
        create_admin()
    else:
        runserver()
