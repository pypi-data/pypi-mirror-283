import subprocess
import sys


def clone_repo():
    default_repo_url = "https://github.com/default/repository.git"  # Step 1: Define a default URL

    # Step 2: Check if the user provided a URL
    repo_url = sys.argv[1] if len(sys.argv) > 1 else default_repo_url  # Step 3: Use provided URL or default

    try:
        subprocess.run(["git", "clone", repo_url], check=True)  # Step 4: Clone the determined URL
    except subprocess.CalledProcessError as e:
        print(f"Error installing default django structure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    clone_repo()
