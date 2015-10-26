"""Foo bar tool

Usage:
  second_class_tool.py create (foo | bar) [-abcdf FLOAT] [--longboolean --some-int INTEGER --string STR --some-array=<integer>... --enum=<enum> --other-enum=<enum>] [--input-file=<file> -x STR <arg-some_file> <arg_some-array>...] [<arg-some-int> <arg-float-some> <arg-str-some>]

Arguments:
  <arg-some_file>                  	arg FILE output. [type: file] [default: file.txt]
  <arg-some-int>			        arg integer. [type: integer]
  <arg-float-some>                 	arg FLOAT. [type: float]
  <arg-str-some>			        arg string.
                                    second line of string decription. [type: string]
  <arg_some-array>		            arg this is array of ints. [type: int]

Options:
  -h --help                         show this help message and exit
  -v, --version                    	show version and exit
  --input-file=<file>               this is input file
  -s STR --string=STR           	this is string
  -i, --some-int INTEGER      	    this is int
                                    second line of description
  -f FLOAT, --float Float       	this is float. [default: 10.0]
  -b                                this is short boolean. [category: Booleans] [altprefix: --alt_prefix]
  --longboolean                     this is longboolean. [Category: Flags]
  -a, --longa                       this is short and long a bool. [category: Bool]
  -c                                this is short c bool
  -d                                this is short d bool
  --some-array=<integer>		    this is list of int. [Default: 1 2 3]
                                    second description line
  --enum=<enum>		                this is enum. Possible values: {10.1 11.1 12.1}. [default: 10.1]
  -x STR                            this is description
  --other-enum=<enum>       	    this is enum. Possible values: {values: 10 11 12}. [default: 10]

Examples:
  python second_class_tool.py create foo

"""


from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version=1.0)
    print args