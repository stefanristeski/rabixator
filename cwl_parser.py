"""Rabix Parser

Usage:
  cwl_parser.py ship new [-b --longboolean --some-int INTEGER --some-float=<float> -s STR --some-array=<integer>... --enum=<enum> --other-enum=<enum>] --file=<file> <some-int> <out_file>...
  cwl_parser.py -h | -v

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
  <out_file>                        this is output FILE [type: file] [default: file.txt]
  <some-int>                        INTEGER [type: integer]
  <some_float> float                FLOAT [type: float]
  <some-enum> enum                  enum [type: enum]
  <some-str> STRING                 string [type: string]
                                    second line of string decription
  <some-array>                      this is array of ints [type: int]

"""

import json
import optdoc
from collections import OrderedDict
from docopt import docopt, printable_usage, parse_defaults, formal_usage


if __name__ == '__main__':
    doc = __doc__
    args = docopt(doc)

    # print 'ARGS \n' + str(args) + '\n'

    # Load options and arguments
    doc_options, doc_args = optdoc.parse_defaults(doc)
    print 'OPTIONS \n' + str(doc_options) + '\n'
    print 'ARGUMENTS \n' + str(doc_args) + '\n'

    # Load list
    usage = printable_usage(doc)
    options = parse_defaults(doc)
    pattern, arg_list, cmd_list = optdoc.parse_pattern(formal_usage(usage), options)
    print 'LIST OPT/ARGS \n' + str(arg_list)

    print 'CMD \n' + str(cmd_list)

    # CWL shema from sbg platform
    rabix_schema = {
        "id": "",
        "class": "CommandLineTool",
        "@context": "https://github.com/common-workflow-language/common-workflow-language/blob/draft-1/specification/tool-description.md",
        "label": "",
        "description": "",
        "owner": [],
        "contributor": [],
        "requirements": [
            {"class": "DockerRequirement", "dockerImageId": "", "dockerPull": ""},
            {"class": "CPURequirement", "value": 1},
            {"class": "MemRequirement", "value": 1000}
        ],
        "inputs": [],
        "outputs": [],
        "baseCommand": [""],
        "stdin": "",
        "stdout": "",
        "argAdapters": [],
        "sbg:category": [],
        "sbg:sbgMaintained": False,
    }

    # Variable types
    str_type = ['STRING', 'STR', '<string>', '<str>']
    int_type = ['INTEGER', 'INT', '<integer>', '<int>']
    float_type = ['FLOAT', '<float>']
    file_type = ['FILE', '<file>']
    enum_type = ['ENUM', '<enum>']

    # Append to rabix input
    def append_input(prefix, o, list=False):
        label = prefix.lower().strip('-').replace('-', '_')
        description = o.get('description')
        var_type = o.get('type')
        if var_type == 'boolean' and not prefix.startswith('--'):
            label = description.replace(' ', '_')

        if list:
            if var_type in str_type: var_type = ["null", {"type": "array", "items": {"type": "string"}}]
            elif var_type in int_type: var_type = ["null", {"type": "array", "items": {"type": "int"}}]
            elif var_type in float_type: var_type = ["null", {"type": "array", "items": {"type": "float"}}]
            elif var_type in file_type: var_type = ["null", {"type": "array", "items": {"type": "File"}}]
        else:
            if var_type in str_type: var_type = 'string'
            elif var_type in int_type: var_type = 'int'
            elif var_type in float_type: var_type = 'float'
            elif var_type in file_type: var_type = 'File'
            elif var_type in enum_type:
                start, end, d = '[values:', ']', o.get('description')
                var_type = ["null", {"type": "enum", "name": prefix.lower().strip('-'),
                                     "symbols": d[d.find(start)+len(start):d.find(end, d.find(start))].strip().split(' ')}]

        inputs = rabix_schema.get('inputs')
        inputs.append(OrderedDict(
            {
                "inputBinding": {"prefix": prefix, "separate": True},
                "type": var_type if 'enum' in str(var_type) or 'array' in str(var_type) else ["null", var_type],
                "id": ''.join(['#', prefix.lower().strip('-').replace('-', '_')]),
                "depth": 0,
                "description": description,
                "label": label,
                "sbg:category": "",
                "schema": var_type if 'enum' in str(var_type) or 'array' in str(var_type) else ["null", var_type],
                "adapter": {"prefix": prefix, "separate": True}
            }
            )
        )
        rabix_schema['inputs'] = inputs

    # Append to rabix output
    def append_output():
        rabix_schema_outputs = rabix_schema.get('outputs')

    def get_prefix(o):
        return o.get('long') if o.get('long') is not None else o.get('short')

    # Iterate over args and options, and call append_input with proper arguments
    for prefix, value in args.iteritems():
        if prefix in ['--version', '--help']:
            continue
        elif isinstance(value, list):
            for o in doc_options:
                if prefix == get_prefix(o):
                    append_input(prefix, o, list=True)
        else:
            for o in doc_options:
                if prefix == get_prefix(o):
                    append_input(prefix, o)

    # Write rabix schema to output.json
    with open('output.json', 'w') as out_file:
        json.dump(rabix_schema, out_file, separators=(',', ':'))
