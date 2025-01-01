import argparse
from getpass import getpass
from pathlib import Path

from loguru import logger

from src.helpers import convert_2fas_to_raivo, get_2fas_files, get_file_to_process


def main():
    exec_dir = Path.cwd()
    logs_dir = Path.joinpath(exec_dir, "logs")

    logger.add(Path.joinpath(logs_dir, "conversion_{time}.log"), level="INFO")

    parser = argparse.ArgumentParser(
        prog="twofas2raivo",
        description="A CLI tool to convert 2FAS backups into Raivo-compatible ones.",
    )
    parser.add_argument(
        "-s",
        "--source_file",
        type=str,
        default=exec_dir,
        required=False,
        help="2FAS Auth backup file path.",
    )
    parser.add_argument(
        "-d",
        "--destination_file",
        type=str,
        default=exec_dir,
        required=False,
        help="Raivo backup file path.",
    )
    parser.add_argument(
        "--encrypted",
        action="store_true",
        required=False,
        help="Specify if 2FAS backup is encrypted.",
    )
    args = parser.parse_args()

    src_file = (
        Path(args.source_file)
        if args.source_file and args.source_file != exec_dir
        else None
    )
    dst_file = (
        Path(args.destination_file)
        if args.destination_file and args.destination_file != exec_dir
        else None
    )
    password = getpass("Enter password: ") if args.encrypted else None

    if (
        src_file is None
        or not src_file.is_file()
        or not src_file.name.endswith(".2fas")
    ):
        logger.warning(
            f"No valid source file passed in input, scanning [{exec_dir}] for .2fas files..."
        )
        try:
            twofas_files = get_2fas_files(exec_dir)
            if len(twofas_files) == 0:
                logger.error("No .2fas files found. Exiting!")
                return
            logger.info(f"Files found: {len(twofas_files)}")
            src_file = (
                get_file_to_process(twofas_files)
                if len(twofas_files) > 1
                else twofas_files[0]
            )
        except Exception as exc:
            logger.error(f"{exc}")
            return

    if dst_file is None:
        dst_file = Path.joinpath(exec_dir, f"raivo-otp-export.zip")
    if dst_file.is_dir():
        dst_file = Path.joinpath(dst_file, f"raivo-otp-export.zip")

    logger.info(f"Source file: [{src_file}]")
    logger.info(f"Destination file: [{dst_file}]")

    try:
        convert_2fas_to_raivo(src_file, dst_file, password)
    except Exception as exc:
        logger.error(f"An error is occurred while converting the file: {exc}")
        return

    logger.info("File converted successfully!")
    return


if __name__ == "__main__":
    main()
