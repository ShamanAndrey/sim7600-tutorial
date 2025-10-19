import re
from typing import Optional, Tuple, Dict

# Example incoming lines for +CMT mode:
# +CMT: "+4915140142720","","25/10/18,14:25:44+08"
# Hello there!
#
# We parse the header and expect the next line to be the SMS body.

CMT_HEADER_RE = re.compile(
    r'^\+CMT:\s*"(?P<number>[^"]+)"\s*,\s*"(?P<alpha>[^"]*)"\s*,\s*"(?P<timestamp>[^"]*)"\s*$'
)

def parse_cmt_header(line: str) -> Optional[Dict[str, str]]:
    m = CMT_HEADER_RE.match(line.strip())
    if not m:
        return None
    return {
        "number": m.group("number"),
        "alpha": m.group("alpha"),
        "timestamp": m.group("timestamp"),
        "raw_header": line.strip(),
    }