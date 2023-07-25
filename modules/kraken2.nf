process kraken2 {

    tag { sample_id }

    publishDir "${params.outdir}/${sample_id}", pattern: "${sample_id}_kraken2*", mode: 'copy'


    input:
      tuple val(sample_id), path(reads), path(kraken2_db)

    output:
      tuple val(sample_id), path("${sample_id}_kraken2.txt"), emit: report
      tuple val(sample_id), path("${sample_id}_kraken2_species.csv"), emit: parsed_report

    script:
    // After running kraken2, check if output file is empty. If it is, return exit code 1 to cause the process to error.
    """
    kraken2 --db ${kraken2_db} --threads ${task.cpus} --output "-" --report ${sample_id}_kraken2.txt ${reads}
    [ -s ${sample_id}_kraken2.txt ]

    parse_kraken_report.py --rank 'S' --sample-id ${sample_id} ${sample_id}_kraken2.txt > ${sample_id}_kraken2_species.csv
    """
}
