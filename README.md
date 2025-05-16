# fetch_ncbi_source_from_csv

A Python script to fetch source metadata from NCBI GenBank records using a list of accession IDs in a CSV file. The script extracts fields such as organism, isolation source, host, geographic location, collection date, and more, saving the results to a CSV output.

---

## Features

- Fetch GenBank source section metadata for given nucleotide IDs.
- Extract fields:  
  - organism  
  - isolation_source  
  - host  
  - geo_loc_name  
  - lat_lon  
  - collection_date  
  - collected_by
- Save results in a structured CSV file.
- Handles errors and missing fields gracefully.

---

## Requirements

- Python 3
- Biopython

Install Biopython with:

```bash
pip install biopython
