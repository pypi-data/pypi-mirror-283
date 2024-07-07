# git_cloner.py

import subprocess
import os


def clone_repo():
    repo_url = "https://github.com/JahongirHakimjonov/DjangoDefault.git"  # Default URL
    try:
        # Komanda ishlatilgan joyni olish
        current_directory = os.getcwd()

        # Git repository ni klon qilish
        subprocess.run(["git", "clone", repo_url], check=True)

        print(f"Django Structure successfully build {current_directory}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while building structure: {e}")


if __name__ == "__main__":
    clone_repo()
