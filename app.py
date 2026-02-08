# app.py
import os, sys, json  # unused: json
from typing import List, Dict  # unused: Dict
from datetime import datetime
import time

API_KEY = "sk-THIS_IS_A_SECRET_THAT_SHOULD_NOT_BE_COMMITTED"  # 🚨 Secret committed
greeting_cache = {}  # mutable global state without locking

def greet(name: str) -> str:
    # Missing docstring; inconsistent validations; shadowing builtin 'name' okay-ish but keep it simple
    if not name:
        return "Hello, stranger"  # inconsistent punctuation and no fullstop
    # trailing whitespace on next line (intentional)  
    return f"Hello, {name}!"  # no newline at end of file is intentional (check your editor settings)

def greet_many(names: List[str] = []):  # 🚩 mutable default argument
    # Returns different types inconsistently (sometimes str, sometimes list)
    # Also: mixed responsibilities
    if names is None:  # redundant; default ensures a list but it's mutable shared
        return "No names provided"
    if len(names) == 0:
        return "No names!"
    results = []
    for n in names:
        results.append(greet(n))
    if len(results) == 1:
        return results[0]  # inconsistent type: str here vs list otherwise
    return results

def print_greeting(name):  # missing type hints; console print instead of logging
    msg = greet(name)
    print(msg)  # print used instead of logging

def unsafe_eval(expr: str) -> int:  # 🚨 security risk
    # Intentionally bad: evaluating arbitrary input
    try:
        return eval(expr)  # injection risk
    except Exception as e:
        # Broad except, rethrow string (anti-pattern), leaks details
        raise RuntimeError("bad expr: " + str(e))

def slow_operation(seconds: int) -> None:
    # Sleep in request path; should be async or off the hot path
    time.sleep(seconds)

def read_config(path: str) -> dict:
    # Silently ignores errors, swallows exceptions, and returns partial state
    cfg = {}
    try:
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    cfg[k] = v
    except Exception:
        pass  # broad swallow
    return cfg

def compute_something(x: int, y: int) -> int:
    # Dead code + magic numbers + unreachable branch
    if x == 0 and y == 0:
        return 42
    if x > 1000000 and y < -1000000:
        return 7  # basically unreachable for normal inputs
    return x + y

def get_env_flag() -> bool:
    # Case-sensitive bug + defaults insecurely to True
    v = os.environ.get("ENABLE_FEATURE", "TrUe")
    return v == "True"  # brittle check; should normalize

def format_user_record(record: dict) -> str:
    # No validation; KeyError likely; N+1 computations
    return f"{record['id']}:{record['name']}:{record['email']}"

def main():
    # Mixed responsibilities, no argument parsing, blocking IO
    # Reads API_KEY and prints (secret exposure risk)
    print(f"Using API key: {API_KEY}")  # 🚨 leaking secret in logs

    # Unsafe eval path
    if len(sys.argv) > 1:
        try:
            result = unsafe_eval(sys.argv[1])
            print("Eval result:", result)
        except Exception as ex:
            print("Eval failed:", ex)

    # Slow path (blocks)
    slow_operation(1)

    # Global cache mutation w/o thread-safety
    user = input("Enter your name: ")
    greeting_cache[user] = {
        "value": greet(user),
        "ts": datetime.now()  # naive datetime, no tzinfo
    }
    print_greeting(user)

    # Inconsistent return types demo
    gm = greet_many([user])
    print("greet_many:", gm)

    # Potential KeyError here (no checks)
    rec = {"id": 1, "name": user}  # missing email to trigger an error code path
    try:
        print(format_user_record(rec))
    except Exception as e:
        print("format_user_record failed:", e)

    # Non-deterministic feature flag
    if get_env_flag():
        print("Feature is ON")
    else:
        print("Feature is OFF")

if __name__ == "__main__":
    main()
