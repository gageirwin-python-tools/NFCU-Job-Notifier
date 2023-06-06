# 🌐 NFCU Job Notifier
A Python application to send Discord webhooks for new/removed jobs for Navy Federal Credit Union (NFCU)

# Usage
Install requirements
```bash
pip install -r requirements.txt
```
Run application
```bash
python nfcu_jobs.py [OPTIONS] --webhook "DISCORD_WEBHOOK"
```
## Options
 - `--webhook WEBHOOK` : Your Discord webhook. (Required)
 - `--categories CATEGORY [CATEGORY ...]` : Categories of the jobs you want to monitor. If no category is passed it will search all.
 - `--locations LOCATION [LOCATION ...]` : Locations of the jobs you want to monitor. If no location is passed it will search all.
 - `--continuous` : Continually check feed(s) based on --interval value. The default --interval is 6 hours.
 - `--interval 0d0h0m0s` : Specify the wait interval in days, hours, minutes, and seconds (e.g., 1d2h30m)
 - `--archive FILE` : Archive file to store previous jobs. Default is `nfcu_jobs.txt` located in the current working directory (cwd).
 - `--force-old` Send webhook notifications on first run when preloading `--archive` file.

### Categories
 - `analyst`
 - `branch-office`
 - `collections`
 - `compliance`
 - `comptroller-accounting`
 - `contact-center`
 - `facilities`
 - `human-resources`
 - `information-technology`
 - `internship`
 - `lending`
 - `marketing-social-media`
 - `mortgage`
 - `security`
 - `skillbridge`
 - `training`
### Locations
 - `pensacola-fl`
 - `vienna-va`
 - `winchester-va`
 - `remote`
### Notes
- Using `--force-old` will send previously existing job notifications on **initial run**.
- A separate `--archive FILE` is need for each separate instance if the files are in the same path.  

## Examples
```bash
python nfcu_jobs.py --categories "information-technology" --locations "remote" --continuous --interval "1d" --webhook "DISCORD_WEBHOOK"
```
Continually check the job postings for `remote` positions for `information-technology`  every 1 days.
```bash
python nfcu_jobs.py --categories "information-technology" "analyst" --locations "remote" "winchester-va" --continuous --interval "1h" --webhook "DISCORD_WEBHOOK"
```
Continually check the job postings for `remote` and `winchester-va` positions for `information-technology` and `analyst` every 1 days.