#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { nanoq }   from './modules/nanoq.nf'
include { kraken2 } from './modules/kraken2.nf'


workflow {
  ch_fastq = Channel.fromPath( params.fastq_search_path ).map{ it -> [it.baseName.split("_")[0], [it]] }
  ch_kraken2_db = Channel.fromPath(params.kraken2_db)
  ch_run_id = Channel.of(params.run_id)

  main:
    nanoq(ch_fastq)
    kraken2(ch_fastq.combine(ch_kraken2_db))

}
