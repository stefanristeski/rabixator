"""Rabix Parser

Usage:
    rabixator.py (<tool_help_call> | --file=<file>) [--stdout=<file_name> --out=<file_name.extension>... --del_prefix=<dash>]

Arguments:
    <tool_help_call>                Tool help call inside single quotes, e.g. 'python tool.py [cmd] --help'.

Options:
    --file=<file>                   Path to the tool help file in txt format, e.g --file=/opt/tool/tool_help.txt.

    --out=<file_name.extension>     Define output file_name and extension, where file_name is used to generate input id
                                    and label, and extension is used to generate glob. This option could be called
                                    multiple times, if you need to define more than one output. Output could be defined
                                    either as single file output or array of files output. For array of files you only
                                    need to add "[]" to the file_name.
                                    e.g. --out='sorted_bam.bam' --out='reports[].pdf' will define two outputs.
                                    First: Single file output sorted_bam.bam is generated with:
                                    {id: 'sorted_bam', label: 'Sorted Bam', type: 'File', glob: '*.bam'},
                                    Second: Array of files output reports[].pdf is generated with:
                                    {id: 'reports', label: 'Reports', type: 'array', glob: '*.pdf'}.

    --stdout=<file_name.extension>  Redirect stdout of tool to the output file, where file_name is label and id in cwl,
                                    and extension is parsed in glob as *.extension. This option could not be called
                                    multiple times. e.g. --stdout=aligned_bam.bam.

    --del_prefix=<dash>             Delete single dash or double dash from every prefix.

    -h, --help                      Print this message and exit.

    -v, --version                   Print cwl parser version.

Examples:
    python rabixator.py --file=path_to_help_file
    python rabixator.py 'python tool.py -h' --del_prefix='--'
    python rabixator.py 'python tool.py -h' --stdout='aligned_bam.bam' --out='sorted_bam.bam' --out='reports[].pdf'
"""

import re
import json
import optdoc
from subprocess import check_output
from collections import OrderedDict
from docopt import docopt, printable_usage, parse_defaults, formal_usage


if __name__ == '__main__':
    args = docopt(__doc__, help=True, version=0.1)
    base_command = ''

    if args.get('<tool_help_call>'):
        base_command = args.get('<tool_help_call>').split(' ')
        doc = check_output(base_command)
    if args.get('--file'):
        with open(args.get('--file'), "r") as help_file:
            doc = help_file.read()

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
    if base_command:
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
    str_type = ['STRING', 'STR', '<string>', '<str>', 'Str', 'str']
    int_type = ['INTEGER', 'INT', '<integer>', '<int>', 'Int', 'int']
    float_type = ['FLOAT', '<float>', 'float', 'Float']
    file_type = ['FILE', '<file>', 'File', 'file']
    enum_type = ['ENUM', '<enum>', 'ENUMERATION', '<enumeration>', 'enum', 'Enum', 'Enumeration']
    bool_type = ['BOOLEAN', '<boolean>', 'BOOL', '<bool>', 'Bool']

    # Append to rabix input
    def append_input(o, list=False):
        if not isinstance(o, str):
            name = o.get('name', None)
            prefix = get_prefix(o)
            # label = prefix.lower().strip('-').replace('-', '_').title() if prefix else name
            label = o.get('description').split('.')[0] if (prefix and o.get('description')) else name
            description = o.get('description')
            var_type = o.get('type')
            if var_type == 'boolean' and not prefix.startswith('--'):
                label = description.split('.')[0]
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
                elif var_type in enum_type or var_type in bool_type:
                    start, end, d = 'values: {', '}', description
                    var_type = ["null", {"type": "enum", "name": prefix.lower().strip('-'),
                                         "symbols": [e.strip() for e in d[d.find(start)+len(start):d.find(end, d.find(start))].split(',')]}]

            if any(map(lambda x: x.upper() in description.upper(), ['default', 'category', 'altprefix'])):
                description = description.split('. ')[:-1]
                description = '. '.join(description) + '.'
            else:
                if not description.endswith('.'):
                    description += '.'

            # split_desc = '.'.join(split_desc)
            # print type(split_desc)
            # description = str('.'.join(description.split('.')[:-1]) + '.') if '.'.join(description.split('.')[:-1]) else str(description),
            # if not description.endswith('.'):
            #     description += '.'
            inputs = rabix_schema.get('inputs')
            del_prefix = args.get('--del_prefix') if args.get('--del_prefix') in ['-', '--'] else None
            # In case o is option
            if o.get('short') or o.get('long'):
                inputs.append(OrderedDict(
                    {
                        "inputBinding": {"prefix": prefix[len(del_prefix):] if del_prefix else prefix, "separate": True},
                        "type": var_type if 'enum' in str(var_type) or 'array' in str(var_type) else ["null", var_type],
                        "id": '#' + label.lower().replace(' ', '_') if not o.get('long') else
                        ''.join(['#', prefix.lower().strip('-').replace('-', '_')]),
                        "description": description,
                        "label": label,
                        "sbg:altPrefix": o.get('short') if (o.get('short') and o.get('long')) else o.get('altprefix'),
                        "sbg:toolDefaultValue": o.get('value'),
                        "sbg:category": o.get('category') if o.get('category') else ""
                    }
                    )
                )

            # In case o is argument
            elif name:
                name = replace(name, [('<', ''), ('>', ''), ('-', '_')])
                inputs.append(OrderedDict(
                    {
                        "inputBinding": {},
                        "type": var_type if 'enum' in str(var_type) or 'array' in str(var_type) else ["null", var_type],
                        "id": ''.join(['#', name]),
                        "description": description,
                        "label": ''.join(['#', name]),
                        "sbg:altPrefix": o.get('short') if (o.get('short') and o.get('long')) else "",
                        "sbg:toolDefaultValue": o.get('value'),
                        "sbg:category": ""
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
                    "description": ''.join(['This is ', o, ' command.', " Type it's name if you want to use it"]),
                    "label": o,
                    "sbg:altPrefix": "",
                    "sbg:toolDefaultValue": "",
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
                "id": ''.join(['#', replace(output[0].lower(), [('-', '_'), ('[', ''), (']', '')])]),
                "label": output[0].replace('_', ' ').replace('-', ' ').title()
            }
        )
        rabix_schema['outputs'] = outputs

    # Append std to rabix output
    def append_stdout(stdout):
        outputs = rabix_schema.get('outputs')
        outputs.append(
            {
                "outputBinding": {"glob": ''.join(['*.', stdout.split('.')[1]])},
                "type": ["null", {"type": "array", "items": {"type": "File"}}] if list else ["null", "File"],
                "id": ''.join(['#', replace(stdout.split('.')[0].lower(), [('-', '_'), ('[', ''), (']', '')])]),
                "label": stdout.split('.')[0].replace('_', ' ').replace('-', ' ').title()
            }
        )
        rabix_schema['outputs'] = outputs

    # get prefix
    def get_prefix(o):
        return o.get('long') if o.get('long') is not None else o.get('short')

    # string replace
    def replace(string, tupple_list):
        for t in tupple_list:
            string = string.replace(t[0], t[1])
        return string

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

    # make std out
    if args.get('--stdout'):
        rabix_schema['stdout'] = args.get('--stdout')
        append_stdout(args.get('--stdout'))

    # position inputs
    for x, id in enumerate(ids):
        for y, inp in enumerate(rabix_schema.get('inputs')):
            if inp['id'] == id:
                rabix_schema['inputs'][y]['inputBinding'].update({'position': x})
    for x, id in enumerate(ids):
        if len(id) == 2:
            for y, o in enumerate(doc_options):
                if id.replace('#', '-') == doc_options[y].get('short') and doc_options[y].get('long'):
                    for z, inp in enumerate(rabix_schema.get('inputs')):
                        if inp['id'] == doc_options[y].get('long').replace('--', '#'):
                            rabix_schema['inputs'][z]['inputBinding'].update({'position': x})

    # make inputs required
    req = re.sub(r'\[.*?\]', '', usage)
    req = re.sub(r'\(.*?\)', '', req)
    req = [x for x in req.split(' ') if x and (x.startswith('-') or x.startswith('<'))]
    req = [replace(x.split('=')[0], [('--', ''), ('...', ''), ('<', ''), ('>', ''), ('-', '_')]) for x in req]
    req = ['#'+x if not x.startswith('_') else '#'+x.split('_')[1] for x in req]
    for id in req:
        for y, inp in enumerate(rabix_schema.get('inputs')):
            if inp['id'] == id:
                rabix_schema['inputs'][y]['type'].remove('null')

    # Write cwl schema to output.json
    with open('output.json', 'w') as out_file:
        json.dump(rabix_schema, out_file, separators=(',', ':'))
