import subprocess

def install_dependencies():
    dependencies = ["numpy", "scikit-image", "pillow", "blend-modes", "tqdm", "nml"]
    for dependency in dependencies:
        subprocess.check_call(["pip", "install", dependency])

if __name__ == "__main__":
    install_dependencies()
