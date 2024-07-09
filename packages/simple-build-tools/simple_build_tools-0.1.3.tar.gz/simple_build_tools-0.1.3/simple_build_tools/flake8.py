""" manage a default flake8 configuration """

import os


def configure_flake(**kwargs):
    try:

        if os.path.exists(".flake8"):
            print("flake8 already exists")
            result = input("Do you want to overwrite it? (y/N): ")
            if result.lower() != "y":
                return

        if not os.path.exists("pyproject.toml"):
            print("You need to run this command in the root path of the projett")
            return

        filename = os.path.join(os.path.dirname(__file__), "flake8.txt")

        with open(filename, "r") as f:
            flake8 = f.read()

        with open(".flake8", "w") as f:
            f.write(flake8)

        print("Done.")

    except Exception as e:
        print(e)
