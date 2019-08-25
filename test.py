import sys
import subprocess

branch = subprocess.run(["git", "-C", sys.argv[1], "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE)
branch = branch.stdout.strip().decode("utf-8")
print(branch)