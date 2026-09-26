
#!/usr/bin/env python3
import sys
for line in sys.stdin:
    line = line.strip()

    if not line or line.startswith("Visit_ID"):
        continue

    fields = line.split(",")

    department = fields[3]

    print(f"{department}\t1")

