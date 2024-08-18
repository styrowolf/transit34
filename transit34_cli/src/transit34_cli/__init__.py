import argparse
import transit34_cli.subcommands as subcommands


def main() -> int:
    parser = argparse.ArgumentParser(
        description="work with Istanbul public transit data",
        usage="%(prog)s [subcommand]",
    )

    subparsers = parser.add_subparsers(required=True, title="subcommands")

    iett_download_parser = subparsers.add_parser(
        "iett-download",
        description="download IETT (bus) data from Otobüsüm Nerede? API",
    )

    subcommands.IETTDownloadArgs.configure_parser(iett_download_parser)

    args = parser.parse_args()
    args.func(args)

    return 0
