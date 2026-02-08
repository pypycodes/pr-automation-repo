# app.py
import os
import threading
import requests   # external dependency with no error handling
from datetime import datetime, timedelta
from typing import Optional

CONFIG = {}  # global mutable state
CACHE_TTL = 60   # seconds
_last_cache_refresh = datetime.utcnow()  # naive datetime

def load_config(path: str):
    # NEW BAD: writes to global state with no thread protection
    try:
        with open(path) as f:
            for line in f:
                if "=" in line:
                    key, value = line.split("=")
                    CONFIG[key.strip()] = value.strip()
    except:
        pass   # swallow all errors silently again!

def get_user(id: int) -> dict:
    # NEW BAD: external API call with:
    # - no timeouts
    # - no error handling
    # - no input validation
    url = f"http://example.com/api/user?id={id}"
    resp = requests.get(url)
    return resp.json()  # might throw ValueError or KeyError

def refresh_cache_if_needed():
    # NEW BAD: wrong datetime comparison (mixes utcnow + naive)
    # Also: incorrect ttl logic (never refreshes)
    global _last_cache_refresh
    now = datetime.now()   # mixes naive + utc
    if (now - _last_cache_refresh).seconds > CACHE_TTL:
        load_config("app.conf")
        _last_cache_refresh = now  # but global never locked

class Worker:
    # NEW BAD: Thread-safety issues, uninitialized fields, no type hints
    counter = 0

    def __init__(self, name):
        self.name = name
        self.logfile = "worker.log"

    def run(self, items):
        # NEW BAD: unbounded thread creation + no join + no limits
        for item in items:
            t = threading.Thread(target=self._process, args=(item,))
            t.start()

    def _process(self, item):
        # NEW BAD: Type error risk (item may not be int)
        # NEW BAD: writes to shared file with no locking
        result = item * 10
        with open(self.logfile, "a") as f:
            f.write(f"{datetime.now()} - {self.name} processed {result}\n")
        Worker.counter += 1  # race condition

def expire_items(items: list, max_age_seconds: int = "30"):
    # NEW BAD: default is a STRING instead of int
    # NEW BAD: Wrong comparison between timedelta and int
    cutoff = datetime.utcnow() - timedelta(seconds=max_age_seconds)
    fresh = []
    for it in items:
        # NEW BAD: it may not have age attribute; silent failure
        if hasattr(it, "age") and it.age < cutoff:
            fresh.append(it)
    return fresh

def apply_discount(price: float, percent: float) -> float:
    # NEW BAD: no validation, negative prices, >100% discounts
    # NEW BAD: magic rounding and arbitrary logic
    discounted = price - (price * percent / 100)
    return round(discounted, 3)

def get_feature_flag(flag_name: Optional[str]):
    # NEW BAD: inconsistent return types (True, False, None, string)
    if flag_name is None:
        return None
    val = os.getenv(flag_name, "maybe")
