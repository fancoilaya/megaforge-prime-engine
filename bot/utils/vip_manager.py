import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "vip_users.json")


def load_vip_users():
    """Return the set of VIP user IDs."""
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("vip_users", []))
    except FileNotFoundError:
        return set()


def save_vip_users(vip_set):
    """Save the VIP user set back to JSON."""
    data = {"vip_users": sorted(list(vip_set))}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_vip(user_id: int):
    vip = load_vip_users()
    vip.add(user_id)
    save_vip_users(vip)
    return vip


def remove_vip(user_id: int):
    vip = load_vip_users()
    if user_id in vip:
        vip.remove(user_id)
        save_vip_users(vip)
    return vip
