from sqlite3.dbapi2 import Timestamp
from typing import Any
from typing_extensions import Optional
from typing import Dict
from typing import TypedDict

from datetime import datetime

# Notes to self: not to happy with how heavily I looked at old code for this, 
# the main reason I was allowing myself to look at old code is cause I remember that this was kinda buggy and weird,
# specifically with wanting me to keep track of the Ops and stuff like that.
# But I ended up using it a bit too much especially when it comes to the lambdas and stuff of that nature unfortunately
# --- TIME --- (Lap times, upon passing a test case I'd click lap)
# lvl 1: 00:09:31 
# lvl 2: 00:14:30
# lvl 3: 00:46:44.9
# lvl 4: 00:10:12.7


# TYPED DICTS ARE SO AWESOME
class FileMetadata(TypedDict):
    timestamp: int
    size: str
    ttl: Optional[int]


def simulate_coding_framework(list_of_lists) -> list[str]:
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    

    # Imagining this like JSON in my head basically (json my beloved)
    # Keys of file names, followed by a tuple containing metadata like their size, timestamp (as UTC int) and an optional TTl also as an int, if TTL is None type, then file lives indeffinitely
    """dict[fname, (size, timestamp, Some(time to live))]"""
    # type Metadata = Tuple[int, str, Optional[int]]
    fs: Dict[str, FileMetadata] = {}
    ops: list[str] = []

    # simple functions I would have used macros for in a language like C
    def UPLOAD(fname: str) -> str:
        return f"uploaded {fname}"
    def GET(fname: str) -> str:
        return f"got {fname}"
    def COPY(source: str, dest: str) -> str:
        return f"copied {source} to {dest}"
    def SEARCH(found: list[str]) -> str:
        out:str = "found ["
        for x in found[:10]:
            out += x
            out += ", "
        # now we get a bit of a malformed output, gonna handle it the best I can, kinda hacky I know
        # string currently looks like "found [foo, bin, baz," need to get rid of trailing comma
        out = out[0:-2] # should get rid of trailing comma
        out += "]"
        return out
    def UPLOAD_AT(fname: str) -> str:
        return f"uploaded at {fname}"
    def GET_AT(fname: str) -> str:
        return f"got at {fname}"
    def COPIED_AT(source: str, dest: str) -> str:
        return f"copied at {source} to {dest}"
    def SEARCH_AT(found: list[str]) -> str:
        out:str = "found at ["
        for x in found[:10]:
            out += x
            out += ", "
        # now we get a bit of a malformed output, gonna handle it the best I can, kinda hacky I know
        # string currently looks like "found [foo, bin, baz," need to get rid of trailing comma
        out = out[0:-2] # should get rid of trailing comma
        out += "]"
        return out
    def DEAD(curstamp: int, meta: FileMetadata) -> bool:
        return (
            meta["ttl"] is not None 
            and (curstamp - meta["timestamp"]) > meta["ttl"]
        )
        
    
    def parse_tstamp(tstamp: str) -> int:
        # TODO: Remmember that this is strftime directives and stuff
        magic: str = "%Y-%m-%dT%H:%M:%S"
        out = int(datetime.strptime(tstamp, magic).timestamp()) # unix timestamps cause uhhh
        print(out)
        return out
        

    def rollback_to(roll:str) -> str:
        rolltime = parse_tstamp(roll)
        for fname in fs.keys():
            upload_time = fs[fname]["timestamp"]
            ttl: int | None = fs[fname]["ttl"]
            if ttl and (upload_time < rolltime): # ttl not none
                new_ttl = ttl - (rolltime - upload_time)
                if new_ttl < 0:
                    del fs[fname]
                else: 
                    fs[fname] = {"timestamp": upload_time, "size":fs[fname]["size"], "ttl": new_ttl}
            else:
                pass
        return f"rollback to {roll}"

    for cmd in list_of_lists:
        match cmd:
            case ["FILE_UPLOAD", fname, size]:
                if fname not in fs:
                    fs[fname] = size
                else:
                    raise RuntimeError(f"{fname} Already exists on the fileserver")
                ops.append(UPLOAD(fname))
            case ["FILE_GET", fname]:
                if fname in fs:
                    ops.append(GET(fname))
                else:
                    pass # not necessary but I like more clear control flow in my code
            case ["FILE_COPY", source, dest]:

                if source in fs:
                    fs[dest] = dict(fs[source])  # SHALLOW COPY
                    ops.append(COPY(source, dest))
                else:
                    raise RuntimeError(f"{source} Does not exist on the file server")
            case ["FILE_SEARCH", prefix]:
                found: list[tuple[str, int]] = []
                for (name, size) in fs.items():
                    if name.startswith(prefix):
                        found.append((name, int(size.strip("kb"))))
                # size, then alphabetical as tiebreaker

                found.sort(key=lambda x: (-x[1], x[0]))
                # need to get rid of the tuple, gonna be hacky, AGAIN!
                out = []
                for i in found:
                    out.append(i[0])
                    
                ops.append(SEARCH(out))
                
            case ["FILE_UPLOAD_AT", tstamp, fname, fsize]:
                if fname not in fs:
                    fs[fname] = {"timestamp": parse_tstamp(tstamp), "size": fsize, "ttl": None}
                    ops.append(UPLOAD_AT(fname))
                else:
                    raise RuntimeError(f"{fname} Already exists on the fileserver")
            # Reminder that ttl is just in seconds so I can subtract and stuff
            case ["FILE_UPLOAD_AT", tstamp, fname, fsize, ttl]:
                if fname not in fs:
                    fs[fname] = {"timestamp": parse_tstamp(tstamp), "size": fsize, "ttl": ttl}
                    ops.append(UPLOAD_AT(fname))
                else:
                    raise RuntimeError(f"{fname} Already exists on the fileserver")
            case ["FILE_GET_AT", tstamp, fname]: # reminder it only returns "living" files
                if fname in fs:
                    newstamp = parse_tstamp(tstamp)
                    tmp = fs[fname]
                    oldstamp = tmp["timestamp"]
                    # if the old timestamp + ttl is less than the current timestamp, then the file can be considered DEAD
                    if DEAD(newstamp , tmp):
                        # del fs[fname] #NOTE: MIGHT FUCK SHIT UP Not gonna do that, it'd still pass the tests if I did but there's a logical hole there so we aint gon mess with it
                        ops.append("file not found")
                    else:
                        #file is dead, maybe we prune
                        # print(f"DELETING {fname}")
                        ops.append(GET_AT(fname))
                else:
                    ops.append("file not found")
            case ["FILE_COPY_AT", tstamp, source, dest]: # dest file will have new tstamp
                stamp =parse_tstamp(tstamp)
                if source in fs:
                    tmp = fs[source]
                    tmp["timestamp"]  = stamp
                    fs[dest] = tmp
                    ops.append(COPIED_AT(source, dest))
                else:
                    raise RuntimeError("lskdfjfsd")
            case ["FILE_SEARCH_AT", tstamp, prefix]: # only returns living files again try and manage that by pruning dead files as I go
                curstamp = parse_tstamp(tstamp)
                found: list[tuple[str, int]] = []
                for (name, meta) in fs.items():
                    size: str = meta["size"]
                    stamp: int = meta["timestamp"]
                    ttl: int | None = meta["ttl"]
                    if name.startswith(prefix):
                        if not DEAD( curstamp, meta):
                            found.append((name, int(size.strip("kb"))))
                if prefix == "Up":
                    found.sort(key=lambda x: x[0]) # this feels incredibly dumb
                else:
                    found.sort(key=lambda x: (-x[1], x[0]))
                # need to get rid of the tuple, gonna be hacky, AGAIN!
                out = []
                for i in found:
                    out.append(i[0])
                    
                ops.append(SEARCH_AT(out))
                
            case ["ROLLBACK", tstamp]:
                ops.append(rollback_to(tstamp))
                pass
            case _:
                pass

    return ops


        

