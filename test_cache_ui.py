"""Test cache UI improvements."""
import subprocess
import time

commands = """1
2
0
0
0
"""

# Run the application
process = subprocess.Popen(
    ['python', '-m', 'src.main'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=commands)
print(stdout)

if stderr:
    print("STDERR:")
    print(stderr)