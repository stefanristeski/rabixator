"""Foo bar tool

Usage:
  tool.py create new [-b --longboolean --some-int INTEGER --some-float=<float> -s STR --some-array=<integer>... --enum=<enum> --other-enum=<enum>] --file=<file> <some-arg-int> <some-arg-file>...
  tool.py -h | -v

Options:
  -h --help                         show this help message and exit
  -v, --version                     show version and exit
  --file=<file>                     this is file
  -s STR --string=STR               this is string
  -i, --some-int INTEGER            this is int
                                    second line of description
  -f --some-float=<float>           this is float [default: 10.0]
  -b                                this is boolean
  --longboolean                     this is long boolean
  --some-array=<integer>            this is list of int [default: 1 2 3]
                                    second description line
  --enum=<enum>                     this is enum [values: 10.1 11.1 12.1] [default: 10.1]
  --other-enum=<enum>               this is enum [default: 10] [values: 10 11 12]

Arguments:
  <arg-some_file>                   arg FILE output [type: file] [default: file.txt]
  <arg-some-int>                    arg integer [type: integer]
  <arg-float-some>                  arg FLOAT [type: float]
  <arg-str-some>                    arg string [type: string]
                                    second line of string decription
  <arg_some-array>                  arg this is array of ints [type: int]

"""
from docopt import docopt

if __name__ == '__main__':
    doc = docopt(__doc__)