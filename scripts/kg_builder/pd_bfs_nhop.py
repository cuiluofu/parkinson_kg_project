"""
This is a method to build an n-hop subgraph from the original UMLS file, currently using a hop count of 7, and the resulting file is pd_nhop_rel.csv
"""

import os
import csv
import pandas as pd
import time

CHUNKSIZE = 100_000

# UMLS Column name of MRREL
COL_REL = [
    "CUI1", "AUI1", "STYPE1", "REL", "CUI2", "AUI2", "STYPE2", "RELA", "RUI", "SRUI",
    "SAB", "SL", "RG", "DIR", "SUPPRESS", "CVF"
]

PD_CUI = "C0030567"  # Parkinson's disease


def find_direct_neighbors(mrrel_path, output_path):
    """
    Step 1:
        - Find the line directly connected to PD_CUI from the complete MRREL.RRF file (CUI1=PD_CUI or CUI2=PD_CUI)
        - Collect these rows and get neighbor_set (all nodes connected to PD)
        - Write to output_path
        Return: neighbor_set, and lines_pd_direct
    """
    neighbor_set = set()
    lines_pd_direct = []  # Store all lines related to PD

    chunk_idx = 0
    with open(mrrel_path, "r", encoding="utf-8") as fin:
        reader = pd.read_csv(fin,
                             sep="|",
                             names=COL_REL,
                             dtype=str,
                             chunksize=CHUNKSIZE,
                             engine="python",
                             quoting=csv.QUOTE_NONE,
                             usecols=range(len(COL_REL))
                             )
        for chunk in reader:
            chunk_idx += 1
            chunk["CUI1"] = chunk["CUI1"].str.upper().fillna("")
            chunk["CUI2"] = chunk["CUI2"].str.upper().fillna("")
            # Keep only PD_CUI lines
            mask = (chunk["CUI1"] == PD_CUI) | (chunk["CUI2"] == PD_CUI)
            filtered = chunk[mask]
            if not filtered.empty:
                # Collect rows
                lines_pd_direct.extend(filtered.values.tolist())
                # Collect neighbor
                for _, row in filtered.iterrows():
                    c1 = row["CUI1"]
                    c2 = row["CUI2"]
                    # If PD is in CUI1, the neighbor is CUI2; If PD is in CUI2, the neighbor is CUI1
                    if c1 == PD_CUI and c2 != PD_CUI:
                        neighbor_set.add(c2)
                    if c2 == PD_CUI and c1 != PD_CUI:
                        neighbor_set.add(c1)

    # Write out lines_pd_direct
    with open(output_path, "w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout, delimiter="|")
        writer.writerow(COL_REL)
        for row in lines_pd_direct:
            writer.writerow(row)

    print(f"[find_direct_neighbors] Found {len(neighbor_set)} neighbors of PD.")
    print(f"[find_direct_neighbors] Wrote {len(lines_pd_direct)} lines tp {output_path}.")
    return neighbor_set, lines_pd_direct

# This method is deprecated because of its high time and space complexity
def bfs_nhop_from_node(mrrel_path, start_cui, n_hops=3):
    """
    Do n hops (BFS) in MRREL for a single start_cui
    Return: lines_found(all rows matched when this node BFS), cui_found(all nodes CUI)
    """
    frontier = {start_cui}
    all_found_cuis = set([start_cui])
    lines_found = []

    for hop in range(1, n_hops + 1):
        if not frontier:
            break
        new_cuis = set()

        with open(mrrel_path, "r", encoding="utf-8") as fin:
            reader = pd.read_csv(fin,
                                 sep="|",
                                 names=COL_REL,
                                 dtype=str,
                                 chunksize=CHUNKSIZE,
                                 engine="python",
                                 quoting=csv.QUOTE_NONE,
                                 usecols=range(len(COL_REL))
                                 )
            for chunk in reader:
                chunk["CUI1"] = chunk["CUI1"].str.upper().fillna("")
                chunk["CUI2"] = chunk["CUI2"].str.upper().fillna("")

                mask = (chunk["CUI1"].isin(frontier)) | (chunk["CUI2"].isin(frontier))
                filtered = chunk[mask]
                if not filtered.empty:
                    # Collect rows
                    lines_found.extend(filtered.values.tolist())
                    # Collect emerging CUI
                    cuiset = set(filtered["CUI1"].tolist()) | set(filtered["CUI2"].tolist())
                    new_cuis.update(cuiset)
        newly_found = new_cuis - all_found_cuis
        frontier = newly_found
        all_found_cuis.update(new_cuis)

    return lines_found, all_found_cuis


#############################
# 1. BFS function core
#############################
def bfs_n_hop(mrrel_path, start_cui, max_hops=5):
    """
    From mrrel_path, do max_hops to jump BFS centered on start_cui.
    Each hop reads MRREL in blocks, finding rows connected to any node in frontier.

    :return:
    all_lines: [ [CUI1, AUI1, ..., CVF], ... ] # Do not go to the weight, then go to the weight
    all_cuis: set(...)   # All CUI that appear in BFS
    """

    frontier = {start_cui}  # Nodes that the current layer wants to extend
    all_cuis = set([start_cui])
    all_lines = []

    for hop in range(1, max_hops + 1):
        if not frontier:
            print(f"[bfs_n_hop] hop={hop}: frontier空, 提前结束 BFS.")
            break
        print(f"[bfs_n_hop] hop={hop}, frontier_size={len(frontier)}")

        new_cuis = set()
        start_t = time.time()

        # Block scan MRREL
        chunk_idx = 0
        with open(mrrel_path, "r", encoding="utf-8") as fin:
            reader = pd.read_csv(
                fin,
                sep="|",
                names=COL_REL,
                dtype=str,
                chunksize=CHUNKSIZE,
                engine="python",
                quoting=csv.QUOTE_NONE,
                usecols=range(len(COL_REL))
            )
            for chunk in reader:
                chunk_idx += 1
                chunk["CUI1"] = chunk["CUI1"].str.upper().fillna("")
                chunk["CUI2"] = chunk["CUI2"].str.upper().fillna("")

                # Find the row for (CUI1 in frontier) OR (CUI2 in frontier)
                mask = chunk["CUI1"].isin(frontier) | chunk["CUI2"].isin(frontier)
                filtered = chunk[mask]
                if not filtered.empty:
                    # Add these lines to all_lines
                    all_lines.extend(filtered.values.tolist())

                    # Extract new node
                    c1s = filtered["CUI1"].tolist()
                    c2s = filtered["CUI2"].tolist()
                    candidate_cuis = set(c1s) | set(c2s)
                    new_cuis.update(candidate_cuis)

        end_t = time.time()
        print(
            f"     hop={hop} done scanning, chunk_count={chunk_idx}, new_cuis={len(new_cuis)}, cost={end_t - start_t:.2f}s")

        # Remove CUIs that have been discovered and keep only the truly new ones
        newly_found = new_cuis - all_cuis
        frontier = newly_found
        all_cuis.update(new_cuis)

    return all_lines, all_cuis


#############################
# 2. De-duplication function (optional)
#############################
def deduplicate_lines(all_lines):
    """
    De-weight all_lines(nested lists).
    If the amount of data is very large, this step will consume a lot of memory.
    """
    # Convert each row to tuple, put in a set
    lines_set = set(tuple(row) for row in all_lines)
    # Convert back to list of list
    final_list = [list(x) for x in lines_set]
    return final_list

def bfs_node_only(mrrel_path, start_cui, max_hops=5):
    """
    Stage 1: Store only the multi-hop BFS of the "node collection".
    Logic:
        - frontier = {start_cui}
        - all_cuis = {start_cui}
        - hop in 1... max_hops:
            Stop if frontier is empty
            Each read MRREL:
                Find the row for (CUI1 in frontier or CUI2 in frontier)
                Extract CUI1, CUI2 → new_cuis from these rows
        frontier = new_cuis - all_cuis
        all_cuis |= new_cuis
    Return: all_cuis (≤ n All nodes that can be jumped to)
    Do not return all rows to avoid memory explosion.
    """

    frontier = {start_cui}
    all_cuis = set([start_cui])

    for hop in range(1, max_hops + 1):
        if not frontier:
            print(f"[bfs_node_only] hop={hop}, frontier空，提前结束")
            break
        start_t = time.time()
        new_cuis = set()
        print(f"[bfs_node_only] hop={hop}, frontier_size={len(frontier)}")

        # Block traversal MRREL
        with open(mrrel_path, "r", encoding="utf-8") as fin:
            reader = pd.read_csv(fin,
                                 sep="|",
                                 names=COL_REL,
                                 dtype=str,
                                 chunksize=CHUNKSIZE,
                                 engine="python",
                                 quoting=csv.QUOTE_NONE,
                                 usecols=range(len(COL_REL)))
            for chunk in reader:
                chunk["CUI1"] = chunk["CUI1"].str.upper().fillna("")
                chunk["CUI2"] = chunk["CUI2"].str.upper().fillna("")

                mask = chunk["CUI1"].isin(frontier) | chunk["CUI2"].isin(frontier)
                filtered = chunk[mask]
                if not filtered.empty:
                    c1s = filtered["CUI1"].tolist()
                    c2s = filtered["CUI2"].tolist()
                    new_cuis.update(c1s)
                    new_cuis.update(c2s)

        newly_found = new_cuis - all_cuis
        frontier = newly_found
        all_cuis.update(new_cuis)
        end_t = time.time()
        print(f"   hop={hop} done, newly_found={len(newly_found)}, all_cuis={len(all_cuis)}, cost={end_t - start_t:.2f}s")

    return all_cuis

def filter_rel_by_cuis(mrrel_path, node_set, output_rel_path):
    """
    Stage 2: After getting the node set node_set,
    Read MRREL once again, keeping only the lines (CUI1 in node_set & CUI2 in node_set)
    Write to output_rel_path
    """

    with open(output_rel_path, "w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout, delimiter="|")
        writer.writerow(COL_REL)

        chunk_idx = 0
        lines_kept = 0

        with open(mrrel_path, "r", encoding="utf-8") as fin:
            reader = pd.read_csv(fin,
                                 sep="|",
                                 names=COL_REL,
                                 dtype=str,
                                 chunksize=CHUNKSIZE,
                                 engine="python",
                                 quoting=csv.QUOTE_NONE,
                                 usecols=range(len(COL_REL)))
            for chunk in reader:
                chunk_idx += 1
                chunk["CUI1"] = chunk["CUI1"].str.upper().fillna("")
                chunk["CUI2"] = chunk["CUI2"].str.upper().fillna("")

                mask = (chunk["CUI1"].isin(node_set)) & (chunk["CUI2"].isin(node_set))
                filtered = chunk[mask]
                if not filtered.empty:
                    lines_kept += len(filtered)
                    filtered.to_csv(fout, sep="|", header=False, index=False)

    print(f"[filter_rel_by_cuis] lines_kept={lines_kept}, output -> {output_rel_path}")

def main():
    """
    1) Find the direct neighbor of PD
    2) Do n-hop BFS for each neighbor and collect all rows
    3) Merge results
    4) Write the final merged CSV + to generate the final CUI collection
    5) Subsequently use finalCUI to filter MRCONSO/MRSTY
    """

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, "data", "umls_output")
    os.makedirs(out_dir, exist_ok=True)

    # Relative path
    # rrf_dir = os.path.join(base_dir, "data", "umls")
    # mrrel_path = os.path.join(rrf_dir,"MRREL.RRF")

    # Absolute path
    mrrel_path = "E:\\Data\\2024AB\\META\\MRREL.RRF"
    out_rel_csv = os.path.join(out_dir, "pd_nhop_rel.csv")
    out_cui_txt = os.path.join(out_dir, "pd_nhop_cuis.txt")

    MAX_HOPS = 7  # The maximum number of hops of a subgraph

    # 第1阶段：只存节点 BFS
    start_time = time.time()
    final_nodes = bfs_node_only(
        mrrel_path=str(mrrel_path),
        start_cui=PD_CUI,
        max_hops=MAX_HOPS
    )
    end_time = time.time()
    print(f"[main] BFS node-only done, total nodes={len(final_nodes)}, cost={end_time - start_time:.2f}s")

    # Write node list
    with open(out_cui_txt, "w", encoding="utf-8") as fout:
        for c in sorted(final_nodes):
            fout.write(c + "\n")
    print(f"[main] node list -> {out_cui_txt}")

    # Stage 2: One-time MRREL filtering
    start_time = time.time()
    filter_rel_by_cuis(str(mrrel_path), final_nodes, str(out_rel_csv))
    end_time = time.time()
    print(f"[main] filter_rel_by_cuis done, cost={end_time - start_time:.2f}s")

    print("[main] Done. See results in:")
    print(f"   * {out_rel_csv}")
    print(f"   * {out_cui_txt}")


if __name__ == "__main__":
    main()
