"""Rabix Parser

Usage:
  cwl_parser.py --file=<file> [-b --int=<integer> --float=<float> -s=<string> --int-array=<int>... --enum=<string>]

Options:
  -h --help                         show this help message and exit
  -v, --version                     show version and exit
  --file=<file>                     this is file
  -s --string=<string>              this is string
  --int=<integer>                   this is int
  --float=<float>                   this is float [default: 10.0] #DETAILED DESCRIPTION
  -b                                this is boolean
  --int-array=<int>...              this is list of int [default: 1 2 3] #ARRAY
  --enum=<enum>                     this is enum [values: x y c]

Try:
  python cwl_parser.py --file file.ext

"""

import json
from collections import OrderedDict
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version='V 1.0')
    print(args)

    # Load rabix schema
    rabix_schema = json.load(open('./input.json'), object_pairs_hook=OrderedDict)
    options = __doc__.splitlines()[__doc__.splitlines().index('Options:'):]

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
        description = ''
        label = ''

        for line in options:
            if prefix in line:
                label = line.split('  ')[-1].strip()

            if prefix in line and '#' in line:
                description = line.rsplit('#')[-1]
                label = line.rsplit('#')[0].split('  ')[-1].strip()

        inputs = rabix_schema.get('inputs')
        inputs.append(OrderedDict(
            {
                "inputBinding": {"prefix": prefix, "separate": True},
                "type": var_type if 'enum' in str(var_type) or 'array' in str(var_type) else ["null", var_type],
                "id": ''.join(['#', prefix.lower().strip('-')]),
                "depth": 0,
                "description": description,
                "label": label,
                "sbg:category": "OPTIONS",
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
    for key, value in args.iteritems():
        if isinstance(value, bool):
            append_input(key, 'boolean')
            print 'boolean'
        elif isinstance(value, list):
            for line in options:
                if key in line and map_any(line, str_type):
                    append_input(key, ["null", {"type": "array", "items": {"type": "string"}}])
                elif key in line and map_any(line, int_type):
                    append_input(key, ["null", {"type": "array", "items": {"type": "int"}}])
                elif key in line and map_any(line, float_type):
                    append_input(key, ["null", {"type": "array", "items": {"type": "float"}}])
                elif key in line and map_any(line, file_type):
                    append_input(key, ["null", {"type": "array", "items": {"type": "File"}}])
        else:
            for line in options:
                if key in line and map_any(line, str_type) and map_all(line, str_type):
                    append_input(key, 'string')
                elif key in line and map_any(line, int_type) and map_all(line, int_type):
                    append_input(key, 'int')
                elif key in line and map_any(line, float_type) and map_all(line, float_type):
                    append_input(key, 'float')
                elif key in line and map_any(line, file_type) and map_all(line, file_type):
                    append_input(key, 'File')
                elif key in line and map_any(line, enum_type):
                    value = ["null", {"type": "enum", "name": key.lower().strip('-'),
                                      "symbols": [v for v in line.rsplit('values: ')[-1].strip(']').split(' ')]}]
                    append_input(key, value)

    # Write rabix schema to output.json
    with open('output.json', 'w') as out_file:
        json.dump(rabix_schema, out_file, separators=(',', ':'))
