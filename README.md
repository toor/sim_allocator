This small library provides the functionality to create new directories per-simulation for use with the Snakemake workflow management tool. It creates new directories based on today's date, and generates a new directory in which to store generated data atomically. If the directory SIM_TODAY_0001 already exists and is not empty, then the directory SIM_TODAY_0002 is automatically generated and marked as the relevant directory. A small snippet to suggest how this may be used inside your Snakefile:

```python
BASE = "results"
META = "meta"
SIM  = select_sim(base=BASE, meta_dir=META, fname="sim_selected.txt")
SIMDIR = f"{BASE}/{SIM}"
LOGDIR = f"logs/{SIM}"

# Ensure roots exist (SIMDIR ensured by allocator)
os.makedirs("logs", exist_ok=True)
os.makedirs(LOGDIR, exist_ok=True)
os.makedirs("figs", exist_ok=True)

SIM_FILE = f"{META}/sim_selected.txt"
```
