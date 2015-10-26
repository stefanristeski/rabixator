"""
Usage:
    snpEff [options] [--filterInterval <file>... --reg <string>...]

Description:
    Generate VCF, BCF or pileup for one or multiple BAM files. Alignment records are grouped by sample (SM) identifiers
    in @RG header lines. If sample identifiers are absent, each input file is regarded as one sample. In the pileup
    format (without -u or -g), each line represents a genomic position, consisting of chromosome name, 1-based
    coordinate, reference base, the number of reads covering the site, read bases, base qualities and alignment mapping
    qualities. Information on match, mismatch, indel, strand, mapping quality and start and end of a read are all
    encoded at the read base column. At this column, a dot stands for a match to the reference base on the forward
    strand, a comma for a match on the reverse strand, a '>' or '<' for a reference skip, `ACGTN' for a mismatch on the
    forward strand and `acgtn' for a mismatch on the reverse strand. A pattern `\\+[0-9]+[ACGTNacgtn]+' indicates there
    is an insertion between this reference position and the next reference position. The length of the insertion is
    given by the integer in the pattern, followed by the inserted sequence. Similarly, a pattern `-[0-9]+[ACGTNacgtn]+'
    represents a deletion from the reference. The deleted bases will be presented as `*' in the following lines. Also
    at the read base column, a symbol `^' marks the start of a read. The ASCII of the character following `^' minus 33
    gives the mapping quality. A symbol `$' marks the end of a read segment.

Options:
    variants_file                       Default is STDIN
    -a, --around <int>                  Show N codons and amino acids around change (only in coding regions). [Category: Options] [AltPrefix: altprefix] [Default: 0]
    --chr <string>                      Prepend 'string' to chromosome name (e.g. 'chr1' instead of '1'). Only on TXT output. [Category: Options]
    --download                          Download reference genome if not available. [Category: Advanced Options] [Default: false]
    -i <enum>                           Input format. Possible values: {vcf, txt, pileup, bed}. [Category: Advanced Options] [Default: vcf]
    --fileList                          Input actually contains a list of files to process. [Category: Options]
    -o <enum>                           Output format. Possible values: {txt, vcf, gatk, bed, bedAnn}. [Category: Options] [Default: vcf]
    --stats <str>                       Name of stats file (summary). [Category: Options] [Default: snpEff_summary.html]
    --noStats                           Do not create stats (summary) file. [Category: Advanced Options]
    --csvStats                          Create CSV summary file instead of HTML. [Category: Advanced Options]

    --del                               Analyze deletions only.
    --ins                               Analyze insertions only.
    --hom                               Analyze homozygous variants only.
    --het                               Analyze heterozygous variants only.
    --minQuality <int>                  Filter out variants with quality lower than X.
    --maxQuality <int>                  Filter out variants with quality higher than X.
    --minCoverage <int>                 Filter out variants with coverage lower than X.
    --maxCoverage <int>                 Filter out variants with coverage higher than X.
    --nmp                               Only MNPs (multiple nucleotide polymorphisms).
    --snp                               Only SNPs (single nucleotide polymorphisms).

    --filterInterval <file>             Only analyze changes that intersect with the intervals specified in this file (you may use this option many times)
    --no-downstream                     Do not show DOWNSTREAM changes
    --no-intergenic                     Do not show INTERGENIC changes
    --no-intron                         Do not show INTRON changes
    --no-upstream                       Do not show UPSTREAM changes
    --no-utr                            Do not show 5_PRIME_UTR or 3_PRIME_UTR changes
    --no EffectType                     Do not show 'EffectType'. This option can be used several times.

    --cancer                            Perform 'cancer' comparisons (Somatic vs Germline). [Default: false]
    --cancerSamples <file>              Two column TXT file defining 'oringinal \t derived' samples.
    --geneId                            Use gene ID instead of gene name (VCF output). [Default: false]
    --hgvs                              Use HGVS annotations for amino acid sub-field. [Default: false]
    --lof                               Add loss of function (LOF) and Nonsense mediated decay (NMD) tags.
    --oicr                              Add OICR tag in VCF file. [Default: false]
    --sequenceOntology                  Use Sequence Ontology terms. [Default: false]

    --config                            Specify config file
    --debug                             Debug mode (very verbose).
    --dataDir <string>                  Override data_dir parameter from config file.
    -h , --help                         Show this help and exit.
    --inOffset <int>                    Offset input by a number of bases. E.g. '-inOffset 1' for one-based TXT input files.
    --outOffset <int>                   Offset output by a number of bases. E.g. '-outOffset 1' for one-based TXT output files.
    --noLog                             Do not report usage statistics to server.
    -t <str>                            Use multiple threads (implies '-noStats'). [Default: off]
    --quiet                             Quiet mode (do not show any messages or errors).
    --verbose                           Verbose mode.

    --canon                             Only use canonical transcripts.
    --interval                          Use a custom intervals in TXT/BED/BigBed/VCF/GFF file (you may use this option many times).
    --motif                             Annotate using motifs (requires Motif database).
    --nextProt                          Annotate using NextProt (requires NextProt database).
    --reg <string>                      Regulation track to use (this option can be used add several times).
    --onlyReg                           Only use regulation tracks.
    --onlyTr <file>                     Only use the transcripts in this file. Format: One transcript ID per line.
    --spliceSiteSize <int>              Set size for splice sites (donor and acceptor) in bases. [Default: 2]
    --upDownStreamLen <int>             Set upstream downstream interval length (in bases).

"""

from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version=1.0)
    # print arguments

    around = arguments.get('--around')
    print around


    def fix_key(key):
        if key.startswith('--'):
            return key[1:]
        return key
    args = {fix_key(key): val for key, val in arguments.iteritems()}
