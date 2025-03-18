<!--
This document provides a comprehensive reference for the field definitions (schema)  
used in the UMLS RRF files (e.g., MRCONSO.RRF, MRREL.RRF, MRSTY.RRF).  
It helps clarify the meaning and usage of each field, supporting easier data extraction,  
filtering, and processing during the knowledge graph (KG) construction process  
for Parkinson's Disease research.
-->



### 1. Concept Names and Sources (File = MRCONSO.RRF)

| Col.     | Description                                                  |
| :------- | :----------------------------------------------------------- |
| CUI      | Unique identifier for concept                                |
| LAT      | Language of term                                             |
| TS       | Term status                                                  |
| LUI      | Unique identifier for term                                   |
| STT      | String type                                                  |
| SUI      | Unique identifier for string                                 |
| ISPREF   | Atom status - preferred (Y) or not (N) for this string within this concept |
| AUI      | Unique identifier for atom - variable length field, 8 or 9 characters |
| SAUI     | Source asserted atom identifier [optional]                   |
| SCUI     | Source asserted concept identifier [optional]                |
| SDUI     | Source asserted descriptor identifier [optional]             |
| SAB      | Abbreviated source name (SAB). Maximum field length is 20 alphanumeric characters. Two source abbreviations are assigned:Root Source Abbreviation (RSAB) — short form, no version information, for example, AI/RHEUM, 1993, has an RSAB of "AIR"Versioned Source Abbreviation (VSAB) — includes version information, for example, AI/RHEUM, 1993, has an VSAB of "AIR93"Official source names, RSABs, and VSABs are included on the [UMLS Source Vocabulary Documentation page](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html). |
| TTY      | Abbreviation for term type in source vocabulary, for example PN (Metathesaurus Preferred Name) or CD (Clinical Drug). Possible values are listed on the [Abbreviations Used in Data Elements page](http://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html). |
| CODE     | Most useful source asserted identifier (if the source vocabulary has more than one identifier), or a Metathesaurus-generated source entry identifier (if the source vocabulary has none) |
| STR      | String                                                       |
| SRL      | Source restriction level                                     |
| SUPPRESS | Suppressible flag. Values = O, E, Y, or N O: All obsolete content, whether they are obsolesced by the source or by NLM. These will include all atoms having obsolete TTYs, and other atoms becoming obsolete that have not acquired an obsolete TTY (e.g. RxNorm SCDs no longer associated with current drugs, LNC atoms derived from obsolete LNC concepts). E: Non-obsolete content marked suppressible by an editor. These do not have a suppressible SAB/TTY combination. Y: Non-obsolete content deemed suppressible during inversion. These can be determined by a specific SAB/TTY combination explicitly listed in MRRANK. N: None of the above Default suppressibility as determined by NLM (i.e., no changes at the Suppressibility tab in MetamorphoSys) should be used by most users, but may not be suitable in some specialized applications. See the [MetamorphoSys Help page](http://www.nlm.nih.gov/research/umls/implementation_resources/metamorphosys/help.html) for information on how to change the SAB/TTY suppressibility to suit your requirements. NLM strongly recommends that users not alter editor-assigned suppressibility, and MetamorphoSys cannot be used for this purpose. |
| CVF      | Content View Flag. Bit field used to flag rows included in Content View. This field is a varchar field to maximize the number of bits available for use. |





### 2. Related Concepts (File = MRREL.RRF)

| Col.     | Description                                                  |
| :------- | :----------------------------------------------------------- |
| CUI1     | Unique identifier of first concept                           |
| AUI1     | Unique identifier of first atom                              |
| STYPE1   | The name of the column in MRCONSO.RRF that contains the identifier used for the first element in the relationship, i.e. AUI, CODE, CUI, SCUI, SDUI. |
| REL      | Relationship of second concept or atom to first concept or atom |
| CUI2     | Unique identifier of second concept                          |
| AUI2     | Unique identifier of second atom                             |
| STYPE2   | The name of the column in MRCONSO.RRF that contains the identifier used for the second element in the relationship, i.e. AUI, CODE, CUI, SCUI, SDUI. |
| RELA     | Additional (more specific) relationship label (optional)     |
| RUI      | Unique identifier of relationship                            |
| SRUI     | Source asserted relationship identifier, if present          |
| SAB      | Abbreviated source name of the source of relationship. Maximum field length is 20 alphanumeric characters. Two source abbreviations are assigned:Root Source Abbreviation (RSAB) — short form, no version information, for example, AI/RHEUM, 1993, has an RSAB of "AIR"Versioned Source Abbreviation (VSAB) — includes version information, for example, AI/RHEUM, 1993, has an VSAB of "AIR93"Official source names, RSABs, and VSABs are included on the [UMLS Source Vocabulary Documentation page](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html). |
| SL       | Source of relationship labels                                |
| RG       | Relationship group. Used to indicate that a set of relationships should be looked at in conjunction. |
| DIR      | Source asserted directionality flag. Y indicates that this is the direction of the relationship in its source; N indicates that it is not; a blank indicates that it is not important or has not yet been determined. |
| SUPPRESS | Suppressible flag. Reflects the suppressible status of the relationship. See also SUPPRESS in MRCONSO.RRF, MRDEF.RRF, and MRSAT.RRF. |
| CVF      | Content View Flag. Bit field used to flag rows included in Content View. This field is a varchar field to maximize the number of bits available for use. |



### 3. Semantic Types (File = MRSTY.RRF)

| Col. | Description                                                  |
| :--- | :----------------------------------------------------------- |
| CUI  | Unique identifier of concept                                 |
| TUI  | Unique identifier of Semantic Type                           |
| STN  | Semantic Type tree number                                    |
| STY  | Semantic Type. The valid values are defined in the Semantic Network. |
| ATUI | Unique identifier for attribute                              |
| CVF  | Content View Flag. Bit field used to flag rows included in Content View. This field is a varchar field to maximize the number of bits available for use. |