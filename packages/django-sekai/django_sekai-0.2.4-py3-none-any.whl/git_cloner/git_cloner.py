import subprocess
import os
import shutil
import tempfile


def clone_repo():
    repo_url = "https://github.com/JahongirHakimjonov/DjangoDefault.git"
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            subprocess.run(["git", "clone", repo_url, tmp_dir], check=True)

            git_dir_path = os.path.join(tmp_dir, '.git')
            if os.path.exists(git_dir_path):
                shutil.rmtree(git_dir_path)

            for item in os.listdir(tmp_dir):
                s_path = os.path.join(tmp_dir, item)
                d_path = os.path.join(os.getcwd(), item)

                if os.path.isdir(s_path) and os.path.exists(d_path):
                    shutil.rmtree(d_path)
                elif os.path.exists(d_path):
                    os.remove(d_path)

                shutil.move(s_path, d_path)

            print(f"Django Structure successfully moved to {os.getcwd()}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while cloning the repository: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
