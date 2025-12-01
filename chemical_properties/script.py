import json
import pandas as pd
from multiprocessing import Pool, cpu_count
"""
This script augments a Mapper JSON file by computing the average value of a
user-specified numerical field (“ValueField”) for every node in the graph.
This file was used for toxicity/solubility results added in the figure.
"""
# ============================
#  Input file paths (anonymized)
# ============================
json_file = "PATH_TO_MAPPER_JSON.json"
processed_data_file = "PATH_TO_PROCESSED_DATA.csv"
value_file = "PATH_TO_VALUE_FILE.csv"   # generic field source file


# ======================================================
#  1. Load value file into dict: Structure → Value(float)
# ======================================================
print("Loading value file...")

df_val = pd.read_csv(value_file)

# Example cleaning: remove first character and convert to float
# Adjust based on your real file format
df_val["ValueField"] = df_val["ValueField"].astype(str).str[1:].astype(float)

# Dictionary lookup: Structure → Value
value_dict = dict(zip(df_val["Structure"], df_val["ValueField"]))


# ======================================================
#  2. Load processed_data and map vertex → structure
# ======================================================
print("Loading processed_data...")

df_proc = pd.read_csv(processed_data_file)
vertex_structures = df_proc["Structure"].tolist()


# ======================================================
#  3. Load mapper JSON
# ======================================================
print("Loading mapper JSON...")

with open(json_file) as f:
    mapper = json.load(f)

nodes = mapper["mapper"]["nodes"]


# ======================================================
#  Worker function (parallel)
# ======================================================
def compute_avg(node):
    total = 0.0
    count = 0

    for v in node["vertices"]:
        struct = vertex_structures[v]   # O(1)
        val = value_dict[struct]        # O(1 lookup)
        total += val
        count += 1

    node["avgs"]["ValueField"] = total / count
    return node


# ======================================================
#  4. Parallel computation
# ======================================================
print(f"Running in parallel on {cpu_count()} cores...")

with Pool() as pool:
    mapper["mapper"]["nodes"] = pool.map(compute_avg, nodes)


# Add metadata keys
mapper["col_keys"].append("ValueField")

# Save updated JSON
with open(json_file, "w") as f:
    json.dump(mapper, f)

print("Done!")
