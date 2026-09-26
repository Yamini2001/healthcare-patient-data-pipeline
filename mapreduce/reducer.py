#!/usr/bin/env python3

import sys

current_department = None
current_count = 0

for line in sys.stdin:
    line = line.strip()

    department, count = line.split("\t")

    count = int(count)

    if current_department == department:
        current_count += count
    else:
        if current_department is not None:
            print(f"{current_department}\t{current_count}")

        current_department = department
        current_count = count

if current_department is not None:
    print(f"{current_department}\t{current_count}")
