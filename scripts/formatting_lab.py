import argparse
import csv


# input file - hla-type.csv
def main(input_path, output_path):
    input_open = open(input_path, "r", newline="")
    input_reader = csv.DictReader(input_open, delimiter=",")

    header_full = [
        "sample_name",
        "HLA-A",
        "HLA-A (2)",
        "HLA-B",
        "HLA-B (2)",
        "HLA-C",
        "HLA-C (2)",
        "HLA-DRB1",
        "HLA-DRB1 (2)",
        "HLA-DRB3",
        "HLA-DRB3 (2)",
        "HLA-DRB4",
        "HLA-DRB4 (2)",
        "HLA-DRB5",
        "HLA-DRB5 (2)",
        "HLA-DQA1",
        "HLA-DQA1 (2)",
        "HLA-DQB1",
        "HLA-DQB1 (2)",
        "HLA-DPB1",
        "HLA-DPB1 (2)",
    ]

    output_open = open(output_path, "w", newline="")
    output_writer = csv.DictWriter(output_open, fieldnames=header_full, dialect="unix")
    output_writer.writeheader()

    def format_options(input_row, allele):
        # create an empty string for the formatted genotype
        genotype = ""
        # determine the hla gene so it can be included in all options for
        # correct nomenclature
        hla_gene = input_row[allele].split("*")[0]
        i = 0
        # split multiple genotype options
        for option in input_row[allele].split("/"):
            # the first option already includes the hla gene
            if i == 0:
                genotype += f"HLA-{option}"
            # add the hla gene to all other options
            else:
                genotype += f"/HLA-{hla_gene}*{option}"
            i += 1

        return genotype

    for input_row in input_reader:
        # create empty output row
        output_row = {column: "" for column in header_full}
        output_row["sample_name"] = input_row["sample_name"]
        for allele in [
            "HLA-A",
            "HLA-B",
            "HLA-C",
            "HLA-DRB1",
            "HLA-DRB3",
            "HLA-DRB4",
            "HLA-DRB5",
            "HLA-DQA1",
            "HLA-DQB1",
            "HLA-DPB1",
        ]:
            allele2 = f"{allele} (2)"
            # no genotype > put ''
            if input_row[allele] == "0":
                output_row[allele] = ""
            else:
                output_row[allele] = format_options(input_row, allele)
            # homozygous > same as allele 1
            if input_row[allele2] == "0":
                output_row[allele2] = output_row[allele]
            else:
                output_row[allele2] = format_options(input_row, allele2)

        output_writer.writerow(output_row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
    Use this script to parse the lab output into the correct format
    """
    )

    parser.add_argument("input")
    parser.add_argument("output")

    args = parser.parse_args()
    main(args.input, args.output)
