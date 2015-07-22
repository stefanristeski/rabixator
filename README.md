# rabixator

"""Rabix Parser
Usage:
  cwlparse.py <tool_help_call> [--stdout=<file_name> --out=<file_name.extension>...]
Options:
  -h, --help                print this message and exit
  -v, --version             print cwl parser version
  --stdout=<file>           reference the output file(s)
  --out=<file_extension>    define output file and extension
Arguments:
  <tool_help_call>          call tool help inside '', e.g. 'python tool_path cmd --help'
Example:
  python cwlparse.py 'python tool.py -h'
  python cwlparse.py 'python tool.py -h' --stdout='out.bam' --out='bam.bam' --out='reports[].pdf'

"""
