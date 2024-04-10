## File Integrity Monitor (FIM)

This Python script monitors the integrity of files within a specified directory, detecting modifications, additions, and deletions. It also leverages VirusTotal's public API to check the reputation of suspicious files (optional, requires API key).

**Features:**

* Calculates SHA-256 hashes of files.
* Creates a baseline dictionary of file paths and their initial hashes.
* Monitors a directory for changes and logs information about:
    * Modified files.
    * Deleted files.
    * Added files.
    * Suspicious file size changes.
* Optionally checks the reputation of suspicious files using VirusTotal (requires API key).
* Creates decoy files (honeyfiles) to detect unauthorized file additions (configurable).

**Requirements:**

* Python 3
* `hashlib` library
* `os` library
* `json` library
* `logging` library
* `collections` library (for `defaultdict`)
* `requests` library (for VirusTotal API)

**Installation:**

1. Ensure you have Python 3 and the required libraries installed. You can install them using `pip`:

   ```bash
   pip install hashlib os json logging collections requests
   ```

2. Save the script as `fim.py`.

**Configuration:**

* Edit the `monitor_dir` variable in the `main` function to point to the directory you want to monitor.
* (Optional) Edit the `baseline_file` variable in the `main` function to change the filename for the baseline dictionary (defaults to `baseline.json` within the monitored directory).
* (Optional) Edit the `create_honeyfiles` function call in the `main` function to adjust the number of honeyfiles created (defaults to 1).
* (Optional) To use VirusTotal integration, obtain an API key from [https://docs.virustotal.com/reference/overview](https://docs.virustotal.com/reference/overview) and set the `api_key` variable in the `check_virus_total_report` function.
