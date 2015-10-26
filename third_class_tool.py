# coding=utf-8
"""
Usage:
    third_class_tool.py command --option_a FILE... --option_b STR [options] [--option_x STR... --option_y INT... --option_z FLOAT...]

Description:
    Main idea of CWL parser is to speed up the process of porting tools to Rabix as much as possible. Parser gets tool
    help/documentation on input either trough help.txt file, either trough call of help command, and makes CWL
    description out of it. Here is the usage of parser.
    For this to work, help file needs to be formatted in docopt manner.

    This parser could be used for all three class of tools. "

    Third class of tools(SBGTools) help file must be in a strict format, which includes the following:
    We only use long option, expect for help and version option where there is "-h, --help" and "-v, --version".
    All option must have two dashes '--' before option's name which is underscore separated between words.
    Option's file type is written in UPPERCASE and tab separated from option's description.

    Usage, Description, Options and Examples content are also tab separated. In Options section, between every option,
    there is a new line. Examples section is optional. There is no Arguments section in third class of tools, which is
    reserved only for positional arguments which we meet in first and second class of tools. Help file is
    surrounded with tipple double quotes. If some option have default value, it goes to the end of the option's description,
    in the following format: "[Default: value]" and "[Default: value1 value2] for arrays".
    Tool Description section must be present.

    Supported file types are: file, string, integer, float, enum, array, boolean flag and boolean enum. Enum is used
    when option supports mutually exclusive values. Those values needs to be placed in description for that option in
    the following format: "Possible values: {value1, value2, value3, value4}", where valueX is placeholder for some
    value. Description of every option is on the right side of the option, separated with a few tabs, and in line with
    other option's descriptions.

    Boolean enum is used when tool supports e.g "Possible values: {true, false, null}" for
    boolean file type, and boolean flag is used when tool supports only True and False. Docopt does not support True as
    default value for boolean flag, but this will be parsed in json as Default, so you need to write [Default: True] or
    [Default: False] at the end boolean flag description. So for third class of tools, if you need to set boolean flag
    to True by default, advice is to use boolean enum instead of boolean flag.

    Usage pattern is structured from only one line. Putting "[options]" in usage pattern instead of every option is
    convenient way to include all options, but you need to specify required options and arrays. Required options goes
    before [options] in usage pattern, and arrays of some file type goes after [options], followed by ellipsis "...".

    For second class of tools, tool help needs to be changed as minimal as possible. This small changes
    usually consist of adding '-' or '--' before option, and/or adding/modifying file type after option. If tool have
    any positional arguments, you need to put them on the right position in usage pattern and write it's file type in
    description under Arguments section, in the following format [type: file_type]. Usage pattern consisted from
    required options, [options], arrays, and positional arguments. On this link you could see docopt example of
    seccond class of tools.

    Here is example of Options for third class of tools.



Options:
    -h, --help          Show this help message and exit. (For third class of tools it's required to pu this option).

    -v, --version       Show version and exit. (For third class of tools it's required to put this option).

    --option_a FILE     This is array of input files which tool requires in order to work. So this param goes before
                        [option] is usage pattern, followed by ellipsis "....".

    --option_b STR      This is some string, which tool also requires in order to work. So
                        this param goes before [option] is usage pattern. Every option
                        except boolean flag which is False by default could have default
                        value. For example this option have "aligned.bam" set as default.
                        [Default: aligned.bam]

    --option_c INT      This is some int. It have long '--option_c' prefix. This option does
                        not have default value. In the next line there is third line of
                        description. This is the third line of description.

    --option_d FLOAT    This is float with default value. Default needs to be in the following
                        format: [Default: 10.0]

    --option_e ENUM     This is enum type with default value included. It’s necessary to put
                        possible values in the following format: “Possible values: {value1,
                        value2}”, e.g. Possible values: {the one, two, three}. [Default: the one]

    --option_f          This is boolean flag. In docopt boolean flag is False by default.  If
                        you need some boolean with True value set as default, use boolean
                        enum instead of boolean flag.

    --option_g BOOL		This is boolean enum. It’s necessary to put possible values in the
                        following format: “Possible values: {value1, value2}”. [Default: value1]

    --option_x STR      This is array of strings. You need to put ... in usage pattern. Default
                        for array needs to be set in the following format:
                        “[Default: value1 value2]”, e.g. [Default: X Y]

    --option_y INT      This is some integer array. You need to put ... in usage pattern.
                        [Default: 1 2 3]

    --option_z FLOAT    This is array of floats without default. You need to put ... in usage
                        pattern.

Examples:
    python third_class_tool.py command --option_a path_to_input_file1 --option_a path_to_input_file2 --option_b output_name

"""

from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version=1.0)
    print(arguments)
