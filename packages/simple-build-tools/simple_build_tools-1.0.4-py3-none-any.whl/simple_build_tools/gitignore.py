""" Copy a standard gitignore to the project folder """
import os


def configure_gitignore(**kwargs):
    """ configure the project with a gitignore"""
    try:

        if os.path.exists(".gitignore"):
            print("gitignore already exists")
            result = input("Do you want to overwrite it? (y/N): ")
            if result.lower() != "y":
                return

        if not os.path.exists("pyproject.toml"):
            print("You need to run this command in the root path of the projett")
            return

        filename = os.path.join(os.path.dirname(__file__), "gitignore.txt")

        with open(filename, "r") as f:
            gitignore = f.read()

        with open(".gitignore", "w") as f:
            f.write(gitignore)

        print("Done.")

    except Exception as e:
        print(f"Error: {e}")
