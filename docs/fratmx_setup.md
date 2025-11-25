# FRATMX asset ingestion setup

This host was provisioned with a system user, directories, and supporting files for the FRATMX asset ingestion cron job. Steps performed:

1. Created a dedicated system account `fratuser` with home `/home/fratuser` for running the cron tasks.
2. Provisioned asset directories `/srv/fratmx-assets/incoming` and `/srv/fratmx-assets/archive` owned by `fratuser:fratuser` with `770` permissions to allow read/write access to the cron user.
3. Attempted to install required packages (`rclone`, `ImageMagick`, and `curl`) via `apt-get`. Package installation was blocked by repository access errors (HTTP 403). `curl` is already available at `/usr/bin/curl`; `rclone` and ImageMagick binaries are not present yet.
4. Added `/usr/local/bin/frat_ingest.py` (executable) using the system Python interpreter (`/usr/bin/python3`).
5. Created `/etc/frat_secrets.json` with placeholders for `telegram_token`, `telegram_chat_id`, and `rclone_remote`, owned by `root:fratuser` with `640` permissions so the cron job can read the file (verify with `sudo -u fratuser cat /etc/frat_secrets.json`). When recreating the file, use `install -m 640 -o root -g fratuser -T /dev/null /etc/frat_secrets.json` so the parent directory is confirmed and the file lands with the expected ownership in a single step.
6. Confirmed `/srv/fratmx-assets` hierarchy retains read/write access for the cron user through ownership and permissions.

Follow-up actions (execute after restoring apt access):

- Install dependencies: `apt-get update && apt-get install -y rclone imagemagick curl` (verify paths with `which rclone`, `which magick`/`convert`, and `which curl`).
- Populate `/etc/frat_secrets.json` with production values for `telegram_token`, `telegram_chat_id`, and `rclone_remote` and re-apply `chmod 640 && chown root:fratuser /etc/frat_secrets.json` (or recreate it with `install -m 640 -o root -g fratuser -T /dev/null /etc/frat_secrets.json`) to keep it readable by the cron user while still restricting write access. Validate readability by the cron user with `sudo -u fratuser cat /etc/frat_secrets.json`.
- Confirm `/usr/local/bin/frat_ingest.py` remains executable (`chmod +x /usr/local/bin/frat_ingest.py`) and uses `/usr/bin/python3`.
- Validate directory permissions: `ls -ld /srv/fratmx-assets /srv/fratmx-assets/incoming /srv/fratmx-assets/archive` to ensure `fratuser` retains write access.
- Configure cron for `fratuser`, e.g. `crontab -u fratuser -e` with an entry similar to: `*/5 * * * * /usr/local/bin/frat_ingest.py >>/var/log/frat_ingest.log 2>&1`.
