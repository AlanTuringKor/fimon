import hashlib
import os
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


def monitor_integrity(baseline):
  """
  Monitors the integrity of files based on the baseline dictionary.

  Args:
      baseline: Dictionary containing file paths and their baseline hashes.

  Prints information about modified, added, or deleted files.
  """
  for filepath, baseline_hash in baseline.items():
    if not os.path.exists(filepath):
      print(f"File deleted: {filepath}")
      continue
    current_hash = hash_file(filepath)
    if current_hash != baseline_hash:
      print(f"File modified: {filepath}")
  # You can add logic to handle new files here.


# Define the directory to monitor
monitor_dir = "/path/to/your/directory"

# Create the baseline on first run (or load a saved baseline)
baseline = create_baseline(monitor_dir)

# Continuously monitor the directory (loop)
while True:
  monitor_integrity(baseline)
  # You can define a delay between checks here
  time.sleep(60)  # Optional: Sleep for 60 seconds between checks
