#!/usr/bin/env python3

import sys
import subprocess
import requests

# --- Configuration ---
ntfyTopic = "your-ntfy-topic"
ntfyURL = f"https://ntfy.sh/{ntfyTopic}"
domainsFile = "domains.txt"
seenFile = "seen.txt"

def load_seen():
    try:
        with open(seenFile, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def mark_seen(entry):
    with open(seenFile, "a") as f:
        f.write(entry + "\n")

def notify(domain):
    try:
        response = requests.post(ntfyURL,
            data=domain,
            headers={
                "Title": "New Cert Detected",
                "Priority": "default",
                "Tags": "lock"
            },
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[warn] Notification failed for {domain!r}: {e}", file=sys.stderr)

seen = load_seen()

with subprocess.Popen(
    ["gungnir", "-r", domainsFile],
    stdout=subprocess.PIPE,
    text=True
) as process:
    for line in process.stdout:
        line = line.strip()
        if line and line not in seen:
            print(line)
            notify(line)
            seen.add(line)
            mark_seen(line)
