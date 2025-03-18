import csv
import os
import pandas as pd

# Set the block size, depending on the memory can be adjusted to large/small
CHUNKSIZE = 100_000

# CUI of Parkinson's disease
PD_CUI = "C0030567"


# Column name definition: Refer to the UMLS Reference Manual
COL_CONSO = [
    "CUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "AUI", "SAUI", "SCUI", "SDUI",
    "SAB", "TTY", "CODE", "STR", "SRL", "SUPPRESS", "CVF"
]

COL_REL = [
    "CUI1", "AUI1", "STYPE1", "REL", "CUI2", "AUI2", "STYPE2", "RELA", "RUI", "SRUI",
    "SAB", "SL", "RG", "DIR", "SUPPRESS", "CVF"
]

COL_STY = [
    "CUI", "TUI", "STN", "STY", "ATUI", "CVF"
]

def filter_mrrel_for_pd(rrf_path, output_path):
    """
    Read in chunks from MRREL, keeping only the lines directly related to PD_CUI, written to output_path.
    """
    #
    print(f"\n[filter_mrrel_for_pd] Reading {rrf_path} in chunks...")
    # Detection tag
    has_data = False
    with open(output_path, "w", encoding="utf-8", newline="") as fout:
        fout.write("|".join(COL_REL) + "\n")
        for i, chunk in enumerate(
                pd.read_csv(rrf_path, sep="|",
                            names=COL_REL,
                            dtype=str,
                            chunksize=CHUNKSIZE,
                            engine='python',
                            quoting=csv.QUOTE_NONE,
                            usecols=range(len(COL_REL)))):
            filtered = chunk[(chunk['CUI1'].str.upper() == PD_CUI) | (chunk['CUI2'].str.upper() == PD_CUI)]
            if not filtered.empty:
                filtered.to_csv(fout, header=False, index=False,sep="|")
                has_data = True
                print(f"Data found in chunk {i}, total rows: {len(filtered)}")
    if not has_data:
        print("No matching data found in the entire file.")
    print(f"\n[filter_mrrel_for_pd]Done. Output -> {output_path}")

def get_related_cuis_from_rel(rel_csv_path):
    """
    All CUI sets related to PD are extracted from the filtered REL CSV
    """
    print(f"\n[get_related_cuis_from_rel] Reading filtered REL CSV: {rel_csv_path}")
    df_rel = pd.read_csv(rel_csv_path, sep="|",names=COL_REL,dtype=str)
    # Collect relevant CUI
    cuis_cui1 = df_rel['CUI1'].dropna().str.strip().tolist()
    cuis_cui2 = df_rel['CUI2'].dropna().str.strip().tolist()

    cui_set = set(cuis_cui1 + cuis_cui2)

    print(f"\n[get_related_cuis_from_rel] Found {len(cui_set)} CUIs related to PD.")
    print(f"\n[get_related_cuis_from_rel] CUIs sample: {list(cui_set)[:10]}")
    return cui_set

def filter_mrconso(rrf_path, related_cuis, output_path):
    """
    Block read MRCONSO, keeping only:
    1) English (LAT=ENG)
    2) CUI is in related_cuis
    """
    print(f"\n[filter_mrconso] Reading {rrf_path} in chunks...")
    # Record the total number of matches
    total_matched = 0
    with open(output_path, mode='w',encoding='utf-8',newline="") as fout:
        fout.write("|".join(COL_CONSO) + "\n")

        for idx,chunk in enumerate  ( pd.read_csv(rrf_path,
                                 sep="|",
                                 names=COL_CONSO,
                                 dtype=str,
                                 engine="python",
                                 quoting=csv.QUOTE_NONE,
                                 chunksize=CHUNKSIZE,
                                 usecols=range(len(COL_CONSO)))):
            print("Related CUIs:", list(related_cuis)[:10])

            df_english = chunk[chunk["LAT"].str.upper() == "ENG"]
            df_filtered = df_english[df_english["CUI"].isin(related_cuis)]

            # Output debugging information on each chunk processing
            matched_count = len(df_filtered)
            total_matched += matched_count
            print(f"[filter_mrconso] chunk {idx} : English rows = {len(df_english)} , Matched rows={matched_count} ]")

            if not df_filtered.empty:
                df_filtered.to_csv(fout, sep="|",header=False,index=False)

    print(f"\n[filter_mrconso] Done. Output -> {output_path}")

def filter_mrsty(rrf_path, related_cuis, output_path):
    """
    Block read MRSTY, leaving CUI only in related_cuis
    """
    print(f"\n[filter_mrstr] Reading {rrf_path} in chunks...")
    # Records the total number of matches
    total_matched = 0
    with open(output_path, mode='w',encoding='utf-8',newline="") as fout:
        fout.write("|".join(COL_STY) + "\n")

        for idx, chunk in enumerate(pd.read_csv(rrf_path,
                                                sep="|",
                                                names=COL_STY,
                                                dtype=str,
                                                engine='python',
                                                quoting=csv.QUOTE_NONE,
                                                chunksize=CHUNKSIZE,
                                                usecols=range(len(COL_STY)))):

            df_filtered = chunk[chunk["CUI"].isin(related_cuis)]

            #  Output debugging information on each chunk processing
            matched_count = len(df_filtered)
            total_matched += matched_count
            print(f"[filter_mrsty] Chunk {idx}: Matched rows={matched_count}")
            if not df_filtered.empty:
                df_filtered.to_csv(fout, sep="|",header=False,index=False)

    print(f"{filter_mrsty} Done. Output -> {output_path}")

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))
    rrf_dir = os.path.join(base_dir,"data","umls")
    out_dir = os.path.join(base_dir,"data","umls_output")
    os.makedirs(out_dir, exist_ok=True)

    # Relative path
    # mrrel_path = os.path.join(rrf_dir,"MRREL.RRF")
    # mrconso_path = os.path.join(rrf_dir,"MRCONSO.RRF")
    # mrsty_path = os.path.join(rrf_dir,"MRSTY.RRF")

    # Absolute path
    mrrel_path ="E:\\Data\\2024AB\\META\\MRREL.RRF"
    mrconso_path = "E:\\Data\\2024AB\\META\\MRCONSO.RRF"
    mrsty_path ="E:\\Data\\2024AB\\META\\MRSTY.RRF"

    rel_filtered = os.path.join(out_dir,"pd_rel.csv")
    conso_filtered = os.path.join(out_dir,"pd_conso.csv")
    sty_filtered = os.path.join(out_dir,"pd_sty.csv")

    # 1) Block filter MRREL, and only PD-related rows are retained
    filter_mrrel_for_pd(mrrel_path,rel_filtered)

    # 2) Get the CUI collection according to the CUI in pd_rel.csv
    cui_set = get_related_cuis_from_rel(rel_filtered)
    print("Sample extracted CUIs:", list(cui_set)[:10])

    # 3) Block filter MRCONSO, retain (English + CUI in cui_set)
    filter_mrconso(mrconso_path,cui_set,conso_filtered)

    # 4) Block screening MRSTY, reserved (CUI in cui_set)
    filter_mrsty(mrsty_path,cui_set,sty_filtered)

    print("\nAll done! Final outputs:")
    print(f"  REL -> {rel_filtered}")
    print(f"  CONSO -> {conso_filtered}")
    print(f"  STY -> {sty_filtered}")

if __name__ == "__main__":
    main()
