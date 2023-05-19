import sys

from .geoserver import *

import argparse


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(1)


def main():
    parser = ArgParser()

    subparser = parser.add_subparsers(dest="command")
    ls_cmd = subparser.add_parser("ls")
    delete_cmd = subparser.add_parser("delete")

    ls_cmd.add_argument("-w", "--workspace", type=str, dest="workspace")

    delete_cmd.add_argument("-w", "--workspace", type=str, dest="workspace")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "ls":
        if args.workspace == None:
            workspaces = get_all_workspaces()
            print("Listing all the workspaces....")
            print(workspaces)
        else:
            stores = get_datastores(args.workspace)
            print(f"Listing all the datastores in workspace {args.workspace}")
            print(stores)
    elif args.command == "delete":
        print(f"delete {args.workspace}")


if __name__ == "__main__":
    main()
