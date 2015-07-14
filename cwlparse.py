"""Rabix Parser

Usage:
  cwlparse.py <tool_help_call> [--stdin=<arg_name> --stdout=<file_name> --out=<file_name.extension>... ]

Options:
  -h, --help                print this message and exit
  -v, --version             print cwl parser version
  --stdout=<file>           reference the output file(s)
  --stdin=<file>            reference the input files(s)
  --out=<file_extension>    define output file and extension

Arguments:
  <tool_help_call>          call tool help inside '', e.g. 'python tool cmd --help'

Example:
  python cwlparse.py 'python tool.py -h'
  python cwlparse.py 'python tool.py -h' --out='bam.bam' --out='reports[].pdf'
  python cwlparse.py 'python tool.py -h' --stdout='out.bam' --stdin='<arg-some_file>' --out='bam.bam' --out='reports[].pdf'

"""

import json
import optdoc
from subprocess import check_output
from collections import OrderedDict
from docopt import docopt, printable_usage, parse_defaults, formal_usage


if __name__ == '__main__':
    args = docopt(__doc__, help=True, version=1.0)
    base_command = args.get('<tool_help_call>').split(' ')
    doc = check_output(base_command)

    # Load options and arguments
    doc_options, doc_args = optdoc.parse_defaults(doc)

    # Load list
    usage = printable_usage(doc)
    options = parse_defaults(doc)
    pattern, arg_list, cmd_list, ids = optdoc.parse_pattern(formal_usage(usage), options)

    # print pattern
    # Print args, options, cmds, and lists
    # print 'ARGS \n' + str(args) + '\n'
    # print 'OPTIONS \n' + str(doc_options) + '\n'
    # print 'ARGUMENTS \n' + str(doc_args) + '\n'
    # print 'LIST OPT/ARGS \n' + str(arg_list)
    # print 'CMD \n' + str(cmd_list)

    # remove -h/--help from base_command
    if '-h' in base_command:
        base_command.remove('-h')
    elif '--help' in base_command:
        base_command.remove('--help')

    # CWL shema
    rabix_schema = OrderedDict({
        'id': '',
        'class': 'CommandLineTool',
        '@context': 'https://github.com/common-workflow-language/common-workflow-language/blob/draft-1/specification/tool-description.md',
        'label': '',
        'description': '',
        'owner': [],
        'contributor': [],
        'requirements': [
            {'class': 'DockerRequirement', 'dockerImageId': '', 'dockerPull': ''},
            {'class': 'CPURequirement', 'value': 1},
            {'class': 'MemRequirement', 'value': 1000}
        ],
        'inputs': [],
        'outputs': [],
        'baseCommand': base_command,
        'stdin': '',
        'stdout': '',
        'successCodes': [],
        'temporaryFailCodes': [],
        'arguments': []
    })

    # Variable types
    str_type = ['STRING', 'STR', '<string>', '<str>', 'str']
    int_type = ['INTEGER', 'INT', '<integer>', '<int>', 'int']
    float_type = ['FLOAT', '<float>', 'float']
    file_type = ['FILE', '<file>', 'File']
    enum_type = ['ENUM', '<enum>', 'enum']

    # Append to rabix input
    def append_input(o, list=False):
        if not isinstance(o, str):
            name = o.get('name', None)
            prefix = get_prefix(o)
            label = prefix.lower().strip('-').replace('-', '_') if prefix else name
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
                    start, end, d = '[values:', ']', description
                    var_type = ["null", {"type": "enum", "name": prefix.lower().strip('-'),
                                         "symbols": d[d.find(start)+len(start):d.find(end, d.find(start))].strip().split(' ')}]

            inputs = rabix_schema.get('inputs')

            # In case o is option
            if o.get('short') or o.get('long'):
                inputs.append(OrderedDict(
                    {
                        "inputBinding": {"prefix": prefix, "separate": True},
                        "type": var_type if 'enum' in str(var_type) or 'array' in str(var_type) else ["null", var_type],
                        "id": ''.join(['#', prefix.lower().strip('-').replace('-', '_')]),
                        "description": description,
                        "label": label,
                        "sbg:category": "",
                    }
                    )
                )
            # In case o is argument
            elif name:
                inputs.append(OrderedDict(
                    {
                        "inputBinding": {},
                        "type": var_type if 'enum' in str(var_type) or 'array' in str(var_type) else ["null", var_type],
                        "id": ''.join(['#', name.replace('<', '').replace('>', '').replace('-', '_')]),
                        "description": description,
                        "label": ''.join(['#', name.replace('<', '').replace('>', '').replace('-', '_')]),
                        "sbg:category": "",
                    }
                    )
                )
        # In case o is command
        else:
            inputs = rabix_schema.get('inputs')
            inputs.append(OrderedDict(
                {
                    "inputBinding": {},
                    "type": ["null", 'string'],
                    "id": ''.join(['#', o]),
                    "description": "",
                    "label": "",
                    "sbg:category": "",
                }
                )
            )
        rabix_schema['inputs'] = inputs

    # Append to rabix output
    def append_output(output, list=False):
        outputs = rabix_schema.get('outputs')
        outputs.append(
            {
                "outputBinding": {"glob": ''.join(['*.', output[1]])},
                "type": ["null", {"type": "array", "items": {"type": "File"}}] if list else ["null", "File"],
                "id": ''.join(['#', output[0].lower().replace('-', '_').replace('[', '').replace(']', '')]),
            }
        )
        rabix_schema['outputs'] = outputs

    def get_prefix(o):
        return o.get('long') if o.get('long') is not None else o.get('short')

    # Iterate over doc_options and append optional inputs
    for x, option in enumerate(doc_options):
        for arg in arg_list:
            arg_long = arg.get('long')
            arg_short = arg.get('short')
            if arg_long and arg_long == option.get('long'):
                doc_options[x]['list'] = True
            elif arg_short and arg_short == option.get('short'):
                doc_options[x]['list'] = True
        if option.get('long') in ['--version', '--help']:
            continue
        elif option.get('list'):
            append_input(option, list=True)
        else:
            append_input(option)

    # Iterate over doc_args and append positional arguments on inputs
    for x, argument in enumerate(doc_args):
        for arg in arg_list:
            arg_name = arg.get('name')
            if arg_name and arg_name == argument.get('name'):
                doc_args[x]['list'] = True
        if argument.get('list'):
            append_input(argument, list=True)
        else:
            append_input(argument)

    # Iterate over cmd_list and append commands
    for x in cmd_list:
        append_input(x)

    # Iterate over out and append outputs
    for output in args.get('--out'):
        output = output.split('.')
        if '[]' in output[0]:
            append_output(output, list=True)
        else:
            append_output(output)

    # make stdin from argument
    if args.get('--stdin'):
        for x, inp in enumerate(rabix_schema.get('inputs')):
            if inp.get('id') == '#' + args.get('--stdin').replace('<', '').replace('>', '').replace('-', '_'):
                rabix_schema['inputs'][x]['inputBinding'] = {"stdin": True}

    # make std out
    if args.get('--stdout'):
        rabix_schema['stdout'] = args.get('--stdout')

    # position inputs
    for x, id in enumerate(ids):
        for y, inp in enumerate(rabix_schema.get('inputs')):
            if inp['id'] == id:
                rabix_schema['inputs'][y]['inputBinding'].update({'position': x})

    # Write cwl schema to output.json
    with open('output.json', 'w') as out_file:
        json.dump(rabix_schema, out_file, separators=(',', ':'))
