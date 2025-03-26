# This is a script for building triples

import pandas as pd
from pathlib import Path

def build_triples(rel_csv_path):
    rel_df = pd.read_csv(rel_csv_path,sep="|",dtype=str)

    def extract_relation(row):
        relation = row['RELA'] if pd.notnull(row['RELA']) else row['REL']
        return (row['CUI1'], relation, row['CUI2'])

    triples = rel_df.apply(extract_relation, axis=1).tolist()
    return triples

if __name__ == "__main__":
    data_dir = Path("../../data/umls_output")
    triples = build_triples(data_dir /"pd_rel.csv")
    print(f"Extracted {len(triples)} triples.")
    print(triples[:10])
