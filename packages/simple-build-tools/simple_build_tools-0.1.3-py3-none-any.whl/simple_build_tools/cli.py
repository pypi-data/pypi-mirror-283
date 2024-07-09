import argparse

from simple_build_tools import configure_python_for_nexus
from simple_build_tools import configure_flake
from simple_build_tools import configure_gitignore


def set_options_nexus(parser):
    parser.add_argument(
        "--name",
        metavar="name",
        help="Name of the nexus server. default: nexus",
        default="nexus",
    )
    parser.add_argument("--nexus-url", metavar="url", help="URL of the Nexus server")
    parser.add_argument(
        "--repository",
        metavar="repository",
        help="Repository name in Nexus. default: /repository/pypi",
    )
    parser.add_argument(
        "--nexus-username", metavar="username", help="Username for Nexus server"
    )
    parser.add_argument(
        "--nexus-password", metavar="password", help="Password for Nexus server"
    )


def set_options_flake8(parser):
    pass


def set_options_gitignore(parser):
    pass


CHOICES = {
    "nexus": (
        "Setup project to use Nexus is PyPi source",
        set_options_nexus,
        configure_python_for_nexus,
    ),
    "flake8": (
        "Add a .flake8 config file to the project folder",
        set_options_flake8,
        configure_flake,
    ),
    "gitignore": (
        "Add a stndard gitignore to thep roject folder",
        set_options_gitignore,
        configure_gitignore,
    ),
}


# argparse.RawTextHelpFormatter
class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=24, width=None):
        super().__init__(prog, indent_increment, max_help_position, width)
        self.max_width = 0  # Track the maximum option width

    def add_argument(self, action):
        super().add_argument(action)
        # Calculate option string length and update max_width if necessary
        option_string_length = sum(len(opt) for opt in action.option_strings)
        self.max_width = max(self.max_width, option_string_length)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            # For positional arguments, just return the metavar or dest
            default = super()._format_action_invocation(action)
        else:
            # Adjust the formatting based on the calculated max width
            parts = []
            for option_string in action.option_strings:
                parts.append(option_string)
            default = ", ".join(parts).ljust(self.max_width + self._current_indent)
        return default


class CommandArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        kwargs["formatter_class"] = CustomHelpFormatter
        super().__init__(*args, **kwargs)


def main():
    parser = CommandArgumentParser(
        usage="%(prog)s [command] ...",
        description="Tools to setup environment for Python Nexus",
    )
    subparsers = parser.add_subparsers(
        title="Command Actions", dest="command", metavar="[command]"
    )
    for name, (desc, set_options, func) in CHOICES.items():
        subparser = subparsers.add_parser(name, help=desc)
        set_options(subparser)
        subparser.set_defaults(run=func)

    args = parser.parse_args()
    args.run(**vars(args))


if __name__ == "__main__":
    main()
