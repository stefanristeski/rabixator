"""
Usage:
    third_class_tool.py command --q1=FILE... --w2=STR [options] [--param9=STR... --param10=INT... --param11=FLOAT...]

Description:
    This is description.

Options:
    -h, --help                      Show this help message and exit.

    --version                       Show version and exit.

    -q=FILE, --q1=FILE              This is array of input files which tool requires in order to work.

    -w=STR, --w2=STR                This is some string, which tool also requires in order to work. [Default: output_file_path]

    -p3=INT, --param3=INT           This is some int. This is third line of description.

    -p4=FLOAT, --param4=FLOAT       This is float with default value. [Default: 10.0]

    -p5=ENUM                        This is enum type with default value included. Possible values: {the one, two, three}.
                                    [Default: the one]

    -p6                             This is short boolean and also a boolean flag. In docopt boolean flag is False
                                    by default, but you need to specify default value. For third class of tools advice
                                    is to use boolean enum, and for first and second this value will be parsed.
                                    [Default: true]

    --param7                        This is long boolean and also a boolean flag. You need to specify default value.
                                    [Default: false]

    -p8 --param8=BOOL               This is boolean enum. Possible values: {true, false, null}. [Default: true]


    --param9=STR                    This is array of strings. You need to put ... in usage pattern. [Default: x y]

    --param10=INT                   This is some integers array. You need to put ... in usage pattern.
                                    Second description line. [Default: 1 2 3]

    --param11=FLOAT                 This is array of floats.

Examples:
    python tool.py command --param1=file --param2=string

"""

from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version=1.0)
    print(arguments)
