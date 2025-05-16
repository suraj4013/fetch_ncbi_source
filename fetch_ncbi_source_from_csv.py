#!/usr/bin/env python3

from Bio import Entrez
import argparse
import re
import csv

# Set your NCBI email (required for Entrez API)
Entrez.email = "your_email@example.com"  # Replace with your email

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Fetch NCBI GenBank source section from CSV file and save to another CSV.")
parser.add_argument("input_csv", help="Input CSV file containing GenBank IDs (column name: 'id')")
parser.add_argument("-o", "--output", help="Output CSV file", default="ncbi_source_data.csv")
args = parser.parse_args()

# CSV fieldnames
fieldnames = [
    "id",
    "organism",
    "isolation_source",
    "host",
    "geo_loc_name",
    "lat_lon",
    "collection_date",
    "collected_by"
]

def extract_field(text, field):
    """Extracts the value of a specific field from the source section."""
    match = re.search(rf'/{field}="(.*?)"', text)
    return match.group(1) if match else "N/A"

def fetch_source_section(plasmid_id):
    """Fetch and parse the source section from GenBank record."""
    try:
        # Fetch GenBank record
        handle = Entrez.efetch(db="nucleotide", id=plasmid_id.strip(), rettype="gb", retmode="text")
        record = handle.read()
        handle.close()

        # Refined regex to extract only the source section
        source_match = re.search(r"FEATURES.*?source\s+.*?(?=\n\s{5}\w)", record, re.S)

        if source_match:
            source_section = source_match.group(0).strip()

            # Remove FEATURES header and unnecessary content
            source_section = re.sub(r"FEATURES\s+.*?\n", "", source_section, flags=re.S).strip()

            # Extract relevant fields
            data = {
                "id": plasmid_id,
                "organism": extract_field(source_section, "organism"),
                "isolation_source": extract_field(source_section, "isolation_source"),
                "host": extract_field(source_section, "host"),
                "geo_loc_name": extract_field(source_section, "geo_loc_name"),
                "lat_lon": extract_field(source_section, "lat_lon"),
                "collection_date": extract_field(source_section, "collection_date"),
                "collected_by": extract_field(source_section, "collected_by")
            }
        else:
            data = {field: "N/A" for field in fieldnames}
            data["id"] = plasmid_id

        print(f"\n✅ Extracted data for {plasmid_id}:")
        print(data)

        return data

    except Exception as e:
        print(f"Failed to fetch {plasmid_id.strip()}: {e}")
        return {field: "Error" for field in fieldnames}

# Read IDs from input CSV
input_file = args.input_csv
output_file = args.output

# Read IDs from the input CSV file
with open(input_file, mode="r") as infile:
    reader = csv.DictReader(infile)
    ids = [row["id"] for row in reader]

# Prepare the output CSV
with open(output_file, mode="w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Fetch and append data for each ID
    for plasmid_id in ids:
        data = fetch_source_section(plasmid_id.strip())
        writer.writerow(data)

print(f"\n✅ All source data saved to {output_file}")
