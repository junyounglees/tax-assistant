"""Test the app with caching."""
import subprocess
import time

# First run - should fetch from API
print("First run - fetching from API:")
process = subprocess.Popen(
    ['python', '-m', 'src.main'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Send commands
commands = "1\n1\n0\n0\n0\n"
stdout, stderr = process.communicate(input=commands)
print(stdout)

print("\n" + "="*50 + "\n")

# Second run - should use cache
print("Second run - using cache:")
process = subprocess.Popen(
    ['python', '-m', 'src.main'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Same commands
stdout, stderr = process.communicate(input=commands)
print(stdout)