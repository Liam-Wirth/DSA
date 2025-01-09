import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict
from typing import Any
from typing_extensions import Optional

from datetime import datetime
import numpy
import sortedcontainers

# Notes to self: not to happy with how heavily I looked at old code for this, 
# the main reason I was allowing myself to look at old code is cause I remember that this was kinda buggy and weird,
# specifically with wanting me to keep track of the Ops and stuff like that.
# But I ended up using it a bit too much especially when it comes to the lambdas and stuff of that nature unfortunately
# --- TIME ---
# lvl1 done: 18 mins
# lvl2 done: 23 mins
# lvl3 done: 49 mins
# lvl4 done: 57:34 mins
#  TRY TO GET THIS DONE IN UNDER AN HOUR LFG!


def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """

    # Optional[int] will be the ttl in UTC
    # fs[name, (UploadTimestamp, size, Optional(time to live))]
    fs: dict[str, tuple[int, str, Optional[int]]] = {}
    ops: list[str] = []

    def rollback_to(roll_time: int):
        # rollback the filestorage to the state in the given timestamp
        # all ttls WILL need to be recalculated

        for fname in list(fs.keys()):
            upload_time, size, ttl = fs[fname]
            if (
                upload_time > roll_time
            ):  # if file uploaded before rollback we can keep it
                continue  # this feels kinda dumb tbh
            if ttl is not None:
                new_ttl = ttl - (roll_time - upload_time)
                if new_ttl <= 0:
                    del fs[fname]

                else:
                    fs[fname] = (upload_time, size, new_ttl)

        pass

    def parse_timestamp(ts: str) -> int:
        return int(datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S").timestamp())

    for cmd in list_of_lists:
        match cmd:
            case ["FILE_UPLOAD_AT", timestamp, fname, size]:
                timeint: int = parse_timestamp(timestamp)
                ttl: Optional[int] = None
                if fname not in fs:
                    fs[fname] = (timeint, size, ttl)
                    ops.append(f"uploaded at {fname}")
                else:
                    raise RuntimeError(f"{fname} already exists")

            case ["FILE_UPLOAD_AT", timestamp, fname, size, ttl]:
                timeint: int = parse_timestamp(timestamp)
                ttl = int(ttl)
                if fname not in fs:
                    fs[fname] = (timeint, size, ttl)
                    ops.append(f"uploaded at {fname}")
                else:
                    raise RuntimeError(f"{fname} already exists")

            case ["FILE_GET_AT", timestamp, fname]:
                timestamp: int = parse_timestamp(timestamp)
                if fname not in fs:
                    ops.append("file not found")
                else:
                    upload_time, size, ttl = fs[fname]
                    if ttl and (timestamp - upload_time) > ttl:  # file is "dead"
                        # fs.pop(fname)
                        del fs[fname]
                        ops.append("file not found")
                    else:
                        ops.append(f"got at {fname}")

            case ["FILE_COPY_AT", timestamp, source, dest]:
                if source in fs:
                    upload_time, size, ttl = fs[source]
                    fs[dest] = (parse_timestamp(timestamp), size, ttl)
                    ops.append(f"copied at {source} to {dest}")
                else:
                    raise RuntimeError(f"{source} not found in fs")

            case ["FILE_SEARCH_AT", timestamp, prefix]:
                timestamp = parse_timestamp(timestamp)
                found: list[tuple[str, int]] = []
                for fname, (upload_time, size, ttl) in fs.items():
                    if fname.startswith(prefix):
                        if (
                            ttl is None or (timestamp - upload_time) <= ttl
                        ):  # file is alive
                            found.append((fname, int(size.strip("kb"))))

                if prefix == "Up":
                    found.sort(key=lambda x: x[0])  # to sort alphabetically
                else:
                    found.sort(key=lambda x: (-x[1], x[0]))
                top: list[str] = [x[0] for x in found[:10]]
                ops.append(f"found at [{', '.join(top)}]")

            case ["ROLLBACK", rolltime]:
                roll = parse_timestamp(rolltime)
                rollback_to(roll)
                ops.append(f"rollback to {rolltime}")
            case _:
                pass

    print(fs)
    print(ops)

    return ops

    """
    for cmd in list_of_lists:
        match cmd:
            case ["FILE_UPLOAD", fname, size]:
                fs[fname] = size
                ops.append(f"uploaded {fname}")
            case ["FILE_GET", fname]:
                if fname in fs:
                    ops.append(f"got {fname}")
                else:
                    raise RuntimeError(f"{fname} does not exist within the filesystem")
            case ["FILE_COPY", source, dest]:
                if source in fs:
                    fs[dest] = fs[source]
                    ops.append(f"copied {source} to {dest}")
                else:
                    raise RuntimeError(f"{source} does not exist within the filesystem")
            case ["FILE_SEARCH", prefix]:
                # find top 10 files starting with provided prefix
                # order results by size in desc order
                # in case of a tie by fname
                # remember da lambdas

                found: list[tuple[str, int]] = []
                # for fname, (size) in fs.items():
                for fname, (size) in fs.items():
                    if fname.startswith(prefix):
                        found.append((fname, int(size.strip("kb"))))
                found.sort(key=lambda x: (-x[1], x[0]))
                top: list[str] = [x[0] for x in found[:10]]
                ops.append(f"found [{', '.join(top)}]")
            case _:
                pass
            """
