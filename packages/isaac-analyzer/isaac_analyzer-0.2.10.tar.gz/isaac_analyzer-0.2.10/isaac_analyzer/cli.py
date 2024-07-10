from argparse import ArgumentParser
from os.path import join
from glob import glob
from logging import DEBUG, INFO
from typing import Sequence

from isaac_analyzer import __version__
from isaac_analyzer.items import print_items, get_by_id
from isaac_analyzer.run_loader import load_run_file
from isaac_analyzer.validator import validate_yaml
from isaac_analyzer.logging import init, getLogger
from isaac_analyzer.analysis.main import analyze_single_run, analyze_runs

logger = getLogger(__name__)


def parse_arguments():
    parser = ArgumentParser(
        description="isaac-analyzer: A CLI application to analyze isaac runs"
    )
    parser.add_argument(
        "--version", action="version", version=f"isaac-analyzer {__version__}"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    add_items_subparser(subparsers)
    add_validate_subparser(subparsers)
    add_analyze_subparser(subparsers)
    add_dry_run_subparser(subparsers)

    return parser.parse_args()


def add_items_subparser(subparsers: ArgumentParser):
    parser_items = subparsers.add_parser(
        "items", help="Operations related to items.yaml"
    )
    items_subparsers = parser_items.add_subparsers(
        dest="items_command", help="Items command help"
    )

    items_subparsers.add_parser("list", help="Print items from items.yaml")

    parser_get = items_subparsers.add_parser("get", help="Get an item by ID")
    parser_get.add_argument("id", help="The ID of the item to fetch")


def add_validate_subparser(subparsers: ArgumentParser):
    parser_validate = subparsers.add_parser(
        "validate", help="Validate a YAML file against the schema"
    )
    parser_validate.add_argument(
        "-f", "--file", type=str, help="Path to a single YAML file to validate"
    )
    parser_validate.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Path to a directory containing YAML files to validate",
    )


def add_dry_run_subparser(subparsers: ArgumentParser):
    parser_dry_run = subparsers.add_parser(
        "load",
        help="Load a directory of run files to see if the run loader throws any issues",
    )
    parser_dry_run.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Path to a directory containing YAML files to dry load",
    )


def add_analyze_subparser(subparsers: ArgumentParser):
    parser_analyze = subparsers.add_parser(
        "analyze", help="Analyze a given file or directory of runs"
    )
    parser_analyze.add_argument(
        "-f", "--file", type=str, help="Path to a single YAML file to analyze"
    )
    parser_analyze.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Path to a directory containing YAML files to analyze",
    )
    parser_analyze.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to a directory where images shall be saved",
    )


def setup_logging(verbose: bool):
    log_level = DEBUG if verbose else INFO
    init(log_level)
    if verbose:
        logger.debug("Verbose logging enabled.")


def handle_items_command(args: Sequence[str]):
    if args.items_command == "list":
        print_items()
    elif args.items_command == "get":
        item = get_by_id(args.id)
        if item:
            logger.info(item)
        else:
            logger.error(f"Item with ID {args.id} not found.")


def handle_validate_command(args: Sequence[str]):
    if args.file:
        validate_single_file(args.file)
    elif args.directory:
        validate_directory(args.directory)


def handle_analyze_command(args: Sequence[str]):
    if args.file:
        analyze_single_file(args.file, args.output)
    elif args.directory:
        analyze_directory(args.directory, args.output)


def handle_load_command(args: Sequence[str]):
    logger.info(
        f"Loading runs inside ({args.directory}) with the run_loader to see potential issues."
    )
    yaml_files = glob(join(args.directory, "*.y*ml"))
    all_good = True

    for file in yaml_files:
        try:
            load_run_file(file)
            logger.debug(f"Successfully loaded file: {file}")
        except Exception as e:
            all_good = False
            logger.error(f"Failed loading file: {file} with error: {e}")

    if all_good:
        logger.info(f"All files inside directory ({args.directory}) loadable.")
        exit(0)
    else:
        exit(1)


def validate_single_file(file_path):
    schema_path = join("resources", "run_file_schema.json")
    try:
        validate_yaml(file_path, schema_path)
        logger.info(f"Validation successful for file: {file_path}")
    except Exception as e:
        logger.error(f"Validation failed for file: {file_path} with error: {e}")
        exit(1)


def validate_directory(directory_path: str):
    schema_path = join("resources", "run_file_schema.json")
    yaml_files = glob(join(directory_path, "*.y*ml"))
    all_valid = True

    for yaml_file in yaml_files:
        try:
            validate_yaml(yaml_file, schema_path)
            logger.info(f"Validation successful for file: {yaml_file}")
        except Exception as e:
            all_valid = False
            logger.error(f"Validation failed for file: {yaml_file} with error: {e}")

    if all_valid:
        logger.info("All YAML files are valid.")
    else:
        logger.error("Some YAML files failed validation. See error messages above.")
        exit(1)


def analyze_single_file(file_path, output_path):
    logger.info(f"Analyzing run file: {file_path}")
    analyze_single_run(file_path, output_path)


def analyze_directory(directory_path, output_path):
    logger.info(f"Analyzing all runs in directory: {directory_path}")
    analyze_runs(directory_path, output_path)


def main():
    args = parse_arguments()
    setup_logging(args.verbose)

    if args.command == "items":
        handle_items_command(args)
    elif args.command == "validate":
        handle_validate_command(args)
    elif args.command == "analyze":
        handle_analyze_command(args)
    elif args.command == "load":
        handle_load_command(args)
    else:
        logger.error("Invalid command. Use --help for more information.")


if __name__ == "__main__":
    main()
