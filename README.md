# CertWatcher

Real-time Certificate Transparency monitoring with push notifications.

## Description

This basic script uses the [Gungnir](https://github.com/g0ldencybersec/gungnir) command line tool to query Certificate Transparency Logs in real time. It then uses a free tier of [ntfy.sh](https://ntfy.sh/) to notify the user when a new certificate is spotted.

Simple deduplication is included so you are not spammed with repeat notifications. A `seen.txt` file is created automatically to track previously seen certificates across runs.

## Prerequisites

- **Python 3** with the `requests` library
- **Gungnir** — install from [github.com/g0ldencybersec/gungnir](https://github.com/g0ldencybersec/gungnir)
- **ntfy.sh account** — sign up at [ntfy.sh](https://ntfy.sh/) and note your topic name

## Installation

```bash
git clone https://github.com/hackerbartender/certwatcher.git
cd certwatcher
pip install -r requirements.txt
```

## Configuration

Open `CertWatcher.py` and edit the constants at the top of the file:

```python
# --- Configuration ---
NTFY_TOPIC = "your-ntfy-topic"   # Your ntfy.sh topic name
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"
DOMAINS_FILE = "domains.txt"     # Path to your list of domains to monitor
SEEN_FILE = "seen.txt"           # Deduplication cache (created automatically)
```

## Usage

1. Create a `domains.txt` file with one domain per line:
   ```
   example.com
   mycompany.io
   ```

2. Run the script:
   ```bash
   python3 CertWatcher.py
   ```

The script will run continuously, printing new certificate entries to stdout and sending a push notification to your ntfy.sh topic each time one is detected.

## How It Works

- On startup, `seen.txt` is loaded into memory to avoid re-alerting on known certificates.
- `gungnir` is launched as a subprocess and its output is read line by line.
- Each new (unseen) entry is printed, sent as a push notification, and recorded in `seen.txt`.

## License

MIT — see [LICENSE](LICENSE).
