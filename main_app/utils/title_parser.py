import re
import requests
from typing import Optional

def get_page_title(url) -> Optional[str]:
    title_re=re.compile(r'<title>(.*?)</title>', re.UNICODE)
    try:
        r = requests.get(url)
    except:
        return

    if r.status_code == 200:
        match = title_re.search(r.text)
        if match:
            return match.group(1)
