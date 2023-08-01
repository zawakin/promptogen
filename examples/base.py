import os

# get the root directory of the project
root_dir = os.path.dirname(os.path.abspath(__file__))

# define the output directory
output_dir = os.path.join(root_dir, "output")

# make sure the output directory is created if it does not exist
os.makedirs(output_dir, exist_ok=True)


def make_output_path(path: str):
    return os.path.join(output_dir, path)
