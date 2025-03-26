# This is a script for creating a concept mapping

import pandas as pd
from pathlib import Path

def build_mappings(conso_csv_path, sty_csv_path):
    conso_df = pd.read_csv(conso_csv_path, sep="|", dtype=str)
    preferred_names = conso_df[conso_df['TS'] == 'P'][['CUI','STR']].drop_duplicates().set_index('CUI')['STR'].to_dict()

    sty_df = pd.read_csv(sty_csv_path, sep="|", dtype=str)
    semantic_types = sty_df[['CUI','STY']].drop_duplicates().set_index('CUI')['STY'].to_dict()

    return preferred_names, semantic_types

if __name__ == "__main__":
    data_dir = Path("../../data/umls_output")
    preferred_names, semantic_types = build_mappings(data_dir / "pd_conso.csv", data_dir / "pd_sty.csv")

    pd_cui = 'C0030567'
    print("PD Preferred Name:", preferred_names.get(pd_cui))
    print("PD Semantic Type:", semantic_types.get(pd_cui))