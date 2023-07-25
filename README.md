# Routine Nanopore QC

A generic pipeline that can be run routinely on all Illumina sequence runs, regardless of the project or organism of interest.

* Sequence quality information
* Possible contamination

## Analyses

* [`nanoq`](https://github.com/esteinig/nanoq): Basic sequence stats including total reads, total bases, read N50 and read quality.
* [`kraken2`](https://github.com/DerrickWood/kraken2): Taxonomic classification of reads.

## Usage

```
nextflow run BCCDC-PHL/routine-nanopore-qc \
  --kraken2_db /path/to/kraken2_db \
  --fastq_input /path/to/reads \
  --outdir /path/to/output_directory
```

## Outputs

Nanoq report:

```
sample_id
reads
bases
n50
longest
shortest
mean_length
median_length
mean_quality
median_quality
```

Species-level Kraken Report:

```
sample_id
percent_seqs_in_clade
num_seqs_in_clade
num_seqs_this_taxon
rank_code
ncbi_taxonomy_id
taxon_name
```
