#!/usr/bin/env python3

import argparse
import csv
import json
import sys


def parse_kraken_report(kraken_report_path):
    """
    """
    kraken_report = []
    input_fieldnames = [
        'percent_seqs_in_clade',
        'num_seqs_in_clade',
        'num_seqs_this_taxon',
        'rank_code',
        'ncbi_taxonomy_id',
        'taxon_name',
    ]
    with open(kraken_report_path, 'r') as f:
        reader = csv.DictReader(f, fieldnames=input_fieldnames, dialect='excel-tab')
        for row in reader:
            for k in input_fieldnames:
                row[k] = row[k].strip()
            try:
                row['percent_seqs_in_clade'] = float(row['percent_seqs_in_clade'])
            except ValueError as e:
                row['percent_seqs_in_clade'] = None
            kraken_report.append(row)

    return kraken_report


def main(args):
    kraken_report = parse_kraken_report(args.report)
    unclassified_rows = list(filter(lambda x: x['rank_code'] == 'U', kraken_report))
    unclassified_row = {
        'percent_seqs_in_clade': 0.0,
        'num_seqs_in_clade': "0",
        'num_seqs_this_taxon': "0",
        'rank_code': 'U',
        'ncbi_taxonomy_id': "0",
        'taxon_name': "unclassified",
    }
    if len(unclassified_rows) > 0:
        unclassified_row = unclassified_rows[0]

    kraken_report_without_unclassified = list(filter(lambda x: x['rank_code'] != 'U', kraken_report))
    if args.rank is not None:
        kraken_report_without_unclassified = list(filter(lambda x: x['rank_code'] == args.rank, kraken_report_without_unclassified))

    kraken_report_without_unclassified_sorted = list(sorted(kraken_report_without_unclassified, key=lambda x: x['percent_seqs_in_clade'], reverse=True))
    kraken_report_sorted = [unclassified_row] + kraken_report_without_unclassified_sorted

    output_fieldnames = [
        'percent_seqs_in_clade',
        'num_seqs_in_clade',
        'num_seqs_this_taxon',
        'rank_code',
        'ncbi_taxonomy_id',
        'taxon_name',
    ]
    if args.sample_id:
        output_fieldnames = ['sample_id'] + output_fieldnames
        for record in kraken_report_sorted:
            record['sample_id'] = args.sample_id.strip()

    writer = csv.DictWriter(sys.stdout, fieldnames=output_fieldnames, dialect='unix', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for row in kraken_report_sorted:
        
        writer.writerow(row)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('report')
    parser.add_argument('--rank')
    parser.add_argument('--sample-id')
    args = parser.parse_args()
    main(args)
