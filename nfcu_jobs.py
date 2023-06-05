import os
import time

import requests
from bs4 import BeautifulSoup
from discord import Embed, SyncWebhook

from args import parse_arguments

WEBHOOK_USERNAME = "🌐 NFCU Job Notifier"
WEBHOOK_ICON = ""
NFCU_LOGO = "https://nfcucareers.ttcportals.com/system/production/assets/331061/original/social-image.png"

RED = 0xFF0000
GREEN = 0x00FF00


def set_category_params(category: str, params: dict) -> None:
    params["ns_category"] = category
    if category == "analyst":
        params["cfm4[]"] = ["ANALYS", "DATA"]
    elif category == "branch-office":
        params["cfm3[]"] = ["NFC12"]
    elif category == "collections":
        params["cfm4[]"] = ["CREDIT"]
    elif category == "compliance":
        params["cfm4[]"] = ["COMPLI"]
    elif category == "comptroller-accounting":
        params["cfm4[]"] = ["NFC02"]
    elif category == "contact-center":
        params["cfm3[]"] = ["NFC18"]
        params["cfm4[]"] = ["CUSTOM"]
    elif category == "facilities":
        params["cfm4[]"] = ["FACILI"]
    elif category == "human-resources":
        params["cfm3[]"] = ["NFC04"]
    elif category == "information-technology":
        params["cfm4[]"] = ["INFORM", "SOFTWA"]
    elif category == "internship":
        params["cfm4[]"] = ["INTERN"]
    elif category == "lending":
        params["cfm3[]"] = ["NFC09"]
    elif category == "marketing-social-media":
        params["cfm4[]"] = ["MARKET"]
    elif category == "mortgage":
        params["cfm4[]"] = ["MORTGE"]
    elif category == "security":
        params["cfm3[]"] = ["NFC14"]
    elif category == "skillbridge":
        params["cfm4[]"] = ["CONTRA"]
        params["cfm5[]"] = ["T"]
    elif category == "training":
        params["cfm4[]"] = ["EDUCAT"]
    return


def set_location_params(location: str, params: dict) -> None:
    params["ns_location"] = location
    if location == "pensacola-fl":
        params["cfm8[]"] = ["NFCU1-PCC", "NFCU1-PML"]
    elif location == "vienna-va":
        params["cfm8[]"] = ["NFCU1-HDQ", "NFCU1-HERN"]
    elif location == "winchester-va":
        params["cfm8[]"] = ["NFCU1-WCC"]
    elif location == "remote":
        params["cfm8[]"] = ["NFCU1-RMT"]
    return


def get_job_info(job: BeautifulSoup):
    position = job.find("td", class_="jobs_table_item_title")
    title = position.text
    link = position.find("a")["href"]
    location = job.find("td", class_="jobs_table_item_location job_location").text
    date_posted = job.find("td", class_="job_table_item_date").text
    return title.strip(), link.strip(), location.strip(), date_posted.strip()


def main():
    args = parse_arguments()
    webhook = SyncWebhook.from_url(args.webhook)
    skip_initial_run = not args.force_old
    interval = args.interval
    archive_file = args.archive

    while True:
        old_jobs = []
        if os.path.exists(archive_file):
            with open(archive_file, "r") as f:
                old_jobs = [line.strip() for line in f.readlines()]

        active_jobs = []

        url = "https://nfcucareers.ttcportals.com/search/jobs"

        for location in args.locations:
            for category in args.categories:
                print(
                    f"Checking NFCU jobs with category='{category}' and location='{location}'"
                )

                params = {}
                set_category_params(category=category, params=params)
                set_location_params(location=location, params=params)

                page = 1
                while True:
                    response = requests.get(url, params=params)
                    print(f"Checking page {page}: {response.url}")
                    soup = BeautifulSoup(response.text, "html.parser")

                    jobs = soup.find_all("tr", class_="jobs_table_item")

                    print(f"Found {len(jobs)} jobs on page {page}.")

                    if jobs == []:
                        break

                    for job in jobs:
                        title, link, j_location, date_posted = get_job_info(job)
                        job_info = f"{title}\t{link}\t{j_location}\t{date_posted}"
                        active_jobs.append(job_info)

                        if job_info in old_jobs:
                            continue

                        if not os.path.exists(archive_file) and skip_initial_run:
                            continue

                        embed = {
                            "author": {
                                "name": WEBHOOK_USERNAME,
                                "url": url,
                            },
                            "title": title,
                            "url": link,
                            "description": "**NEW POSITION**",
                            "color": GREEN,
                            "fields": [
                                {
                                    "name": "Location:",
                                    "value": j_location,
                                    "inline": True,
                                },
                                {
                                    "name": "Date Added:",
                                    "value": date_posted,
                                    "inline": True,
                                },
                            ],
                            "thumbnail": {"url": NFCU_LOGO},
                        }
                        webhook.send(
                            username=WEBHOOK_USERNAME,
                            avatar_url=WEBHOOK_ICON,
                            embed=Embed.from_dict(embed),
                        )

                    page += 1
                    params["page"] = page

            for old_job in old_jobs:
                if not old_job in active_jobs:
                    title, link, j_location, date_posted = old_job.split("\t")
                    embed = {
                        "author": {
                            "name": WEBHOOK_USERNAME,
                        },
                        "title": title,
                        "url": link,
                        "description": "**REMOVED POSITION**",
                        "color": RED,
                        "fields": [
                            {
                                "name": "Location:",
                                "value": j_location,
                                "inline": True,
                            },
                            {
                                "name": "Date Added:",
                                "value": date_posted,
                                "inline": True,
                            },
                        ],
                        "thumbnail": {"url": NFCU_LOGO},
                    }
                    webhook.send(
                        username=WEBHOOK_USERNAME,
                        avatar_url=WEBHOOK_ICON,
                        embed=Embed.from_dict(embed),
                    )

        with open(archive_file, "w") as f:
            for job in active_jobs:
                f.write(job + "\n")

        if not args.continuous:
            break

        print(f"Sleeping for {interval} seconds.")
        time.sleep(interval)


if __name__ == "__main__":
    main()
