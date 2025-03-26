# This method is used to generate pd_nhop_conso.csv and pd_nhop_sty.csv files

import os
from scripts.umls.chunk_extract_example import filter_mrconso,filter_mrsty

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))
    rrf_dir = os.path.join(base_dir,"data","umls")
    out_dir = os.path.join(base_dir,"data","umls_output")
    cui_txt = os.path.join(out_dir,"pd_nhop_cuis.txt")
    os.makedirs(out_dir, exist_ok=True)

    mrconso_path = "E:\\Data\\2024AB\\META\\MRCONSO.RRF"
    mrsty_path = "E:\\Data\\2024AB\\META\\MRSTY.RRF"

    conso_filtered = os.path.join(out_dir,"pd_nhop_conso.csv")
    sty_filtered = os.path.join(out_dir,"pd_nhop_sty.csv")

    # 1) load final_cuis
    final_cuis = set()
    with open(cui_txt, 'r', encoding='utf-8') as fin:
        for line in fin:
            final_cuis.add(line.strip())

    # 2) filter mrconso
    filter_mrconso(mrconso_path, final_cuis, conso_filtered)
    # 3) filter mrsty
    filter_mrsty(mrsty_path, final_cuis, sty_filtered)

if __name__ == "__main__":
    main()