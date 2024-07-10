#!/usr/bin/env python3
"""
This module provides a command-line interface (CLI) for the byte-formatter
package, allowing users to convert file sizes to a human-readable format using
various options.
"""

import argparse
from byte_formatter.formatter import format_size


# noinspection PyProtectedMember
class ExplicitDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """
    A custom formatter class that displays the default values for all arguments
    in the help message.
    """

    def _get_help_string(self, action):
        if action.default is None or action.default is False:
            return action.help
        return super()._get_help_string(action)


def _parse_args():
    """
    Parses the command-line arguments provided by the user.

    Returns:
        argparse.ArgumentParser: The parser instance.
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=ExplicitDefaultsHelpFormatter,
        description="Convert a file size to a human-readable format.",
    )

    # Define arguments and options for the CLI
    parser.add_argument("size", type=int, help="The file size in bytes.")
    unit_group = parser.add_argument_group("Unit options")
    unit_group.add_argument(
        "-b",
        "--binary",
        action="store_true",
        help="Use binary (base-1024) units (KiB, MiB, etc.).",
    )
    unit_group.add_argument(
        "-S",
        "--si-units",
        action="store_true",
        help=
        "Use SI units (kB, MB, etc.) which are base-1000 but with different "
        "symbols.",
    )
    unit_group.add_argument(
        "-u",
        "--unit-case",
        choices=["upper", "lower"],
        default="upper",
        help=
        "Use uppercase (KB, MB) or lowercase (kb, mb) unit symbols. Default "
        "is uppercase.",
    )
    unit_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Use verbose unit names (Bytes, Kilobytes, etc.).",
    )
    unit_group.add_argument(
        "-x",
        "--unix-style",
        action="store_true",
        help="Use single-letter Unix-style unit names (B, K, M, G, T, P).",
    )
    parser.add_argument(
        "-p",
        "--precision",
        type=int,
        default=1,
        help="The number of decimal places to include in the formatted size.",
    )
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        default="",
        help="A suffix to append to the formatted size string.",
    )
    parser.add_argument(
        "-t",
        "--strip-trailing-zeros",
        action="store_true",
        help="Strip trailing zeros from the formatted size.",
    )

    return parser, parser.parse_args()


def main():
    """
    The main function of the CLI. It parses arguments, validates them, and then
    formats the provided file size according to the specified options.
    """
    parser, args = _parse_args()

    # Validate the provided file size to ensure it's non-negative
    if args.size < 0:
        parser.error("The file size must be a non-negative integer.")

    # Format the size based on the provided arguments and options
    formatted_size = format_size(
        size=args.size,
        binary=args.binary,
        precision=args.precision,
        suffix=args.suffix,
        strip_trailing_zeros=args.strip_trailing_zeros,
        si_units=args.si_units,
        uppercase_units=args.unit_case == "upper",
        verbose=args.verbose,
        unix_style=args.unix_style,
    )

    print(formatted_size)


if __name__ == "__main__":
    main()
