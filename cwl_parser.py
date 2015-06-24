"""Rabix Parser

Usage:
  cwl_parser.py --file=<file> [-b --longboolean --some-int INTEGER --some-float=<float> -s=<string> --some-array=<integer>... --enum=<string>]
  cwl_parser.py -h | -v

Options:
  -h --help                         show this help message and exit
  -v, --version                     show version and exit
  --file=<file>                     this is file
  -s --string=<string>              this is string
  -i, --some-int INTEGER            this is int
  --some-float=<float>              this is float [default: 10.0]
  -b                                this is boolean
  --longboolean                     this is long boolean
  --some-array=<integer>...         this is list of int [default: 1 2 3]
  --enum=<enum>                     this is enum [values: x y c]

Try:
  python cwl_parser.py --file file.ext

"""

import json
from collections import OrderedDict
from docopt import docopt, printable_usage, parse_defaults, parse_pattern, formal_usage


if __name__ == '__main__':
    args = docopt(__doc__, version='v1.0.0')

    # print(args)
    # print formal_usage(__doc__)
    doc = __doc__
    usage = printable_usage(doc)
    options = parse_defaults(doc)
    pattern = parse_pattern(formal_usage(usage), options)
    # print usage
    print pattern
    # print pattern

    rabix_schema = {
        "id": "",
        "class": "CommandLineTool",
        "@context": "https://github.com/common-workflow-language/common-workflow-language/blob/draft-1/specification/tool-description.md",
        "label": "",
        "description": "",
        "owner": ["null"],
        "contributor": [],
        "requirements": [
            {"class": "DockerRequirement", "imgRepo": "", "imgTag": "", "imgId": ""},
            {"class": "CpuRequirement", "value": 500},
            {"class": "MemRequirement", "value": 1000}
        ],
        "inputs": [],
        "outputs": [],
        "baseCommand": [""],
        "stdin": "",
        "stdout": "",
        "argAdapters": [],
        "sbg:category": []
    }

    # Load rabix options
    options = __doc__.splitlines()[__doc__.splitlines().index('Options:'):]
    # Load rabix arguments
    # options = __doc__.splitlines()[__doc__.splitlines().index('Arguments:'):]

    # Variable types
    str_type = ['STRING', 'STR', '<string>', '<str>']
    int_type = ['INTEGER', 'INT', '<integer>', '<int>']
    float_type = ['FLOAT', '<float>']
    file_type = ['FILE', '<file>']
    enum_type = ['ENUM', '<enum>']

    # Map any
    def map_any(line, type):
        return any(map(lambda t: t in line, type))

    # Map all
    def map_all(line, type):
        return all(map(lambda t: t + '...' not in line, type))

    # Append to rabix input
    def append_input(prefix, var_type):
        label = ""
        description = ""

        for line in options:
            if prefix in line:
                label = prefix.lower().strip('-').replace('-', '_')
                description = line.split('  ')[-1].strip()
                if var_type == 'boolean' and not prefix.startswith('--'):
                    label = description

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
        pass

    # Iterate over args and options, and call append_input with proper arguments
    for prefix, value in args.iteritems():
        if isinstance(value, bool):
            if prefix in ['--version', '--help']:
                continue
            else:
                append_input(prefix, 'boolean')
        elif isinstance(value, list):
            for line in options:
                if prefix in line and map_any(line, str_type):
                    append_input(prefix, ["null", {"type": "array", "items": {"type": "string"}}])
                elif prefix in line and map_any(line, int_type):
                    append_input(prefix, ["null", {"type": "array", "items": {"type": "int"}}])
                elif prefix in line and map_any(line, float_type):
                    append_input(prefix, ["null", {"type": "array", "items": {"type": "float"}}])
                elif prefix in line and map_any(line, file_type):
                    append_input(prefix, ["null", {"type": "array", "items": {"type": "File"}}])
        else:
            for line in options:
                if prefix in line and map_any(line, str_type) and map_all(line, str_type):
                    append_input(prefix, 'string')
                elif prefix in line and map_any(line, int_type) and map_all(line, int_type):
                    append_input(prefix, 'int')
                elif prefix in line and map_any(line, float_type) and map_all(line, float_type):
                    append_input(prefix, 'float')
                elif prefix in line and map_any(line, file_type) and map_all(line, file_type):
                    append_input(prefix, 'File')
                elif prefix in line and map_any(line, enum_type):
                    value = ["null", {"type": "enum", "name": prefix.lower().strip('-'),
                                      "symbols": [v for v in line.rsplit('values: ')[-1].strip(']').split(' ')]}]
                    append_input(prefix, value)

    # Write rabix schema to output.json
    with open('output.json', 'w') as out_file:
        json.dump(rabix_schema, out_file, separators=(',', ':'))


