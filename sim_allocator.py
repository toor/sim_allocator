# lib/sim_allocator.py
import os
import datetime as dt


def select_sim(base="results", meta_dir="meta", fname="sim_selected.txt", envvar="SIM_NAME"):
    os.makedirs(base, exist_ok=True)
    os.makedirs(meta_dir, exist_ok=True)
    sim_file = os.path.join(meta_dir, fname)

    # Optional manual override
    if envvar and envvar in os.environ and os.environ[envvar].strip():
        sim = os.environ[envvar].strip()
        print(f"[SIM-RESOLVE] Using SIM from env {envvar}='{sim}'")
        _write_atomic(sim_file, sim + "\n")
        _ensure_dir(os.path.join(base, sim))
        return sim

    # Reuse previously selected SIM if present (prevents worker re-allocation)
    if os.path.exists(sim_file):
        sim = open(sim_file).read().strip()
        print(f"[SIM-RESOLVE] Reusing SIM from {sim_file}: '{sim}'")
        _ensure_dir(os.path.join(base, sim))
        return sim

    # Allocate next SIM for today, reusing empty dirs
    date = dt.datetime.now().strftime("%Y_%m_%d")
    print(f"[SIM-RESOLVE] Selecting simulation directory for date {date}")
    i = 1
    while True:
        sim = f"SIM_{date}_{i:04d}"
        path = os.path.join(base, sim)
        if os.path.exists(path):
            print(f"[SIM-RESOLVE] '{sim}' exists; checking emptiness...")
            if not os.listdir(path):  # empty → reuse
                print(f"[SIM-RESOLVE] '{sim}' is empty; reusing it.")
                break
            print(f"[SIM-RESOLVE] '{sim}' not empty; trying next.")
            i += 1
        else:
            print(f"[SIM-RESOLVE] Creating '{sim}'")
            os.mkdir(path)
            break

    _write_atomic(sim_file, sim + "\n")
    return sim

def _write_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(data)
    os.replace(tmp, path)

def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)
