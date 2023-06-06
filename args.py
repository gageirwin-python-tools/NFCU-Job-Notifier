import argparse
import os
import re
from datetime import timedelta


def validate_archive(path):
    if not os.path.exists(os.path.dirname(path)):
        raise argparse.ArgumentTypeError(
            f"Invalid path: Directory {os.path.dirname(path)} does not exist."
        )
    return path


def parse_time_interval(value):
    pattern = (
        r"^((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?$"
    )
    match = re.match(pattern, value)
    if not match:
        raise argparse.ArgumentTypeError(
            "Invalid time interval format. Please provide a valid interval (e.g., 1d2h30m)"
        )

    groups = match.groupdict()
    time_dict = {key: int(value) for key, value in groups.items() if value is not None}

    return timedelta(**time_dict)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A Python application to send Discord webhooks for new/removed jobs for NFCU."
    )
    parser.add_argument(
        "--webhook",
        type=str,
        required=True,
        metavar="DISCORD_WEBHOOK",
        help="Your Discord webhook. (Required)",
    )
    parser.add_argument(
        "--categories",
        type=str,
        metavar="CATEGORY",
        choices=[
            "analyst",
            "branch-office",
            "collections",
            "compliance",
            "comptroller-accounting",
            "contact-center",
            "facilities",
            "human-resources",
            "information-technology",
            "internship",
            "lending",
            "marketing-social-media",
            "mortgage",
            "security",
            "skillbridge",
            "training",
        ],
        nargs="+",
        help="Categories of the jobs you want to monitor. If no category is passed it will search all.",
        default=[],
    )
    parser.add_argument(
        "--locations",
        type=str,
        metavar="LOCATION",
        choices=["pensacola-fl", "vienna-va", "winchester-va", "remote"],
        nargs="+",
        help="Locations of the jobs you want to monitor. If no location is passed it will search all.",
        default=[],
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Continually check for jobs based on --interval value. The default --interval is 6 hours.",
    )
    parser.add_argument(
        "--interval",
        type=parse_time_interval,
        metavar="0d0h0m0s",
        help="Specify the wait interval in days, hours, minutes, and seconds (e.g., 1d2h30m)",
        default=timedelta(hours=6),
    )
    parser.add_argument(
        "--archive",
        metavar="FILE",
        type=validate_archive,
        help="Archive file to store previous jobs. Default is nfcu_jobs.txt located in the current working directory (cwd).",
        default=os.path.join(os.getcwd(), "nfcu_jobs.txt"),
    )
    parser.add_argument(
        "--force-old",
        action="store_true",
        help="Send webhook notifications on first run when preloading --archive file.",
    )
    args = parser.parse_args()
    return args
