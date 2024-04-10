import hashlib
import os
import json
import logging
import time



def hash_file(filepath):
  """
  Calculates the SHA-256 hash of a file.

  Args:
      filepath: Path to the file.

  Returns:
      SHA-256 hash of the file as a string.
  """
  with open(filepath, 'rb') as f:
    hasher = hashlib.sha256()
    for chunk in iter(lambda: f.read(4096), b''):
      hasher.update(chunk)
  return hasher.hexdigest()


def create_baseline(directory):
  """
  Creates a baseline dictionary of file paths and their SHA-256 hashes.

  Args:
      directory: Path to the directory to monitor.

  Returns:
      Dictionary with file paths as keys and SHA-256 hashes as values.
  """
  baseline = {}
  for root, _, files in os.walk(directory):
    for filename in files:
      filepath = os.path.join(root, filename)
      baseline[filepath] = hash_file(filepath)
  return baseline


def save_baseline(baseline, filepath):
  """
  Saves the baseline dictionary to a JSON file.

  Args:
      baseline: Dictionary containing file paths and their baseline hashes.
      filepath: Path to the JSON file for storing the baseline.
  """
  with open(filepath, 'w') as f:
    json.dump(baseline, f, indent=4)


def load_baseline(filepath):
  """
  Loads the baseline dictionary from a JSON file.

  Args:
      filepath: Path to the JSON file containing the baseline.

  Returns:
      Dictionary with file paths and their baseline hashes, or an empty dictionary if file not found.
  """
  if not os.path.exists(filepath):
    return {}
  with open(filepath, 'r') as f:
    try:
      return json.load(f)
    except json.JSONDecodeError:
      logging.warning("Error loading baseline from %s", filepath)
      return {}


def monitor_integrity(baseline, monitor_dir):
  """
  Monitors the integrity of files based on the baseline dictionary.

  Args:
      baseline: Dictionary containing file paths and their baseline hashes.

  Logs information about modified, added, or deleted files.
  """
  for filepath, baseline_hash in baseline.items():
    if not os.path.exists(filepath):
      logging.info(f"File deleted: {filepath}")
      continue
    current_hash = hash_file(filepath)
    if current_hash != baseline_hash:
      logging.warning(f"File modified: {filepath}")
    else:
      logging.debug(f"File unchanged: {filepath}")  # Optional debug log
  # Handle new files
  for root, _, files in os.walk(monitor_dir):
    for filename in files:
      filepath = os.path.join(root, filename)
      if filepath not in baseline:
        logging.info(f"New file added: {filepath}")
        # You can decide to add the new file to the baseline here


def main():
  # Configure logging
  logging.basicConfig(filename='fim.log', level=logging.INFO,
                      format='%(asctime)s - %(levelname)s - %(message)s')

  # Define directory to monitor and baseline file path
  monitor_dir = "/path/to/your/directory"
  baseline_file = os.path.join(monitor_dir, 'baseline.json')

  # Load baseline or create a new one
  baseline = load_baseline(baseline_file)
  if not baseline:
    baseline = create_baseline(monitor_dir)
    save_baseline(baseline, baseline_file)

  # Continuously monitor the directory
  while True:
    monitor_integrity(baseline, monitor_dir)
    time.sleep(60)  # Optional: Sleep for 60 seconds between checks


if __name__ == "__main__":
  main()
