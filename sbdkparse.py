"""Parse sbdk1 wrappers to sbdk2

Usage:
    sbdkparse.py [-j FILE | --json FILE]
    sbdkparse.py [-h | -v]

Options:
    -j, --json FILE             Parse this json file [default: in_schema.json]
    -h, --help                  Print this message and exit
    -v, --version               Print version and exit

Example:
    python sbdkparse.py --json in_schema.json

"""

import json
from docopt import docopt

# def name_to_id(name):
#     input_id = [
#         c.replace(',', '_').replace(' ', '_').replace('-', '_').replace('.', '').replace('\'', '').replace('"', '')
#         for c in name.lower()]
#     return ''.join(input_id)


# Append input
def append_input(input):
    if input.get('list') is True:
        input_type = {"type": "array", "items": "File"}
    else:
        input_type = "File"

    # capitalize and append '.'  to description
    description = input.get('description')
    if description:
        description = ''.join([description[0].upper(), description[1:]])
        if not description.endswith('.'):
            description = ''.join([description, '.'])

    item_separator = None if input.get('list') else " "

    inputs = rabix_schema.get('inputs')
    inputs.append(
        {
            "inputBinding": {"prefix": prefix, "separate": True, "itemSeparator": item_separator,  "sbg:cmdInclude": True},
            "type": [input_type] if input.get('id') in required else ["null", input_type],
            "id": ''.join(['#', input.get('id')]),
            "description": description if description else "",
            "label": ''.join([input.get('name')[0].upper(),  input.get('name')[1:]]) if input.get('name') else "",
            "sbg:category": "Input Files",
            "sbg:altPrefix": input.get('_extra').get('alt')
        }
    )
    rabix_schema['inputs'] = inputs


# Append output
def append_output(output):
    if output.get('list') is True:
        output_type = {"type": "array", "items": "File"}
    else:
        output_type = "File"

    # capitalize description and append '.' to description
    description = output.get('description')
    if description:
        description = ''.join([description[0].upper(), description[1:]])
        if not description.endswith('.'):
            description = ''.join([description, '.'])

    outputs = rabix_schema.get('outputs')
    outputs.append(
        {
            "type": [output_type] if output.get('id') in required else ["null", output_type],
            "id": ''.join(['#', output.get('id')]),
            "description": description if description else "",
            "label": ''.join([output.get('name')[0].upper(),  output.get('name')[1:]]) if output.get('name') else "",
        }
    )
    rabix_schema['outputs'] = outputs


# Append param
def append_param(param):
    if param.get('type') == 'struct':
        print ''.join(['\n', 'PARAM IS STRUCT. PLEASE ADD IT MANUALLY!',
                       ' - {id: "', param['id'], '", name: "', param['name'], '"}', '\n'])
        return
    elif param.get('type') == 'string':
        param_type = 'string'
    elif param.get('type') == 'enum':
        param_type = {"type": "enum", "name": param.get('id'), "symbols": [v[0] for v in param.get('values')]}
    elif param.get('type') == 'integer':
        param_type = 'int'
    elif param.get('type') == 'float':
        param_type = 'float'
    elif param.get('type') == 'boolean':
        param_type = 'boolean'

    if param.get('list') is True:
        param_type = {"type": "array", "items": param_type}

    if param.get('type') == 'enum' and param.get('list') is True:
        print ''.join(['\n', 'PARAM IS ENUM LIST. PLEASE ADD IT MANUALLY!',
                       ' - {id: "', param['id'], '", name: "', param['name'], '"}', '\n'])
        param_type = {"type": "array", "items": {"type": "enum", "name": param.get('id'), "symbols": [v[0] for v in param.get('values')]}}

    item_separator = None if input.get('list') else " "
    category = param.get('category') if param.get('category') else ""
    default = str(param.get('default')) if param.get('default') is not None else ""

    # capitalize and append '.', 'default', 'category' to description
    description = param.get('description')

    if description:
        description = ''.join([description[0].upper(), description[1:]])
        if not description.endswith('.'):
            description = ''.join([description, '.'])
        # if param.get('default'):
            # description = ''.join([description, ' [Default: ', ''.join(['"', param.get('default'), '"'])
            # if isinstance(param.get('default'), str) else str(param.get('default')), ']'])
        # if param.get('category'):
            # description = ''.join([description, ' [Category: ', '"', param.get('category'), '"', ']'])

    inputs = rabix_schema.get('inputs')
    inputs.append(
        {
            "inputBinding": {"prefix": prefix, "separate": True, "itemSeparator": item_separator, "sbg:cmdInclude": True},
            "type": [param_type] if param.get('id') in required else ["null", param_type],
            "id": ''.join(['#', param.get('id')]),
            "description": description if description else "",
            "label": param.get('name'),
            "sbg:category": category,
            "sbg:toolDefaultValue": default,
            "sbg:altPrefix": param.get('_extra').get('alt')
        }
    )
    rabix_schema['inputs'] = inputs

if __name__ == '__main__':
    args = docopt(__doc__, version=1.0)
    schema = args.get('--json')

    for schema in json.load(open(schema)):

        # CWL shema
        rabix_schema = {
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
            'baseCommand': '',
            'stdin': '',
            'stdout': '',
            'successCodes': [],
            'temporaryFailCodes': [],
            'arguments': []
        }

        required = []
        sbdk_schema = schema
        sbdk_schema_inputs = sbdk_schema.get('schema').get('inputs')
        sbdk_schema_params = sbdk_schema.get('schema').get('params')
        sbdk_schema_outputs = sbdk_schema.get('schema').get('outputs')
        wrapper = sbdk_schema.get('wrapper_id').split('.')

        print '.'.join(wrapper).upper()

        # Iterate over sbdk schema inputs and call append_input
        for order, input in enumerate(sbdk_schema_inputs):
            if input.get('_extra').get('arg') is None:
                prefix = raw_input('Enter prefix for Input ' + ''.join(
                    ['{id: "', input['id'], '", name: "', input['name'], '"}:']))
            else:
                prefix = input.get('_extra').get('arg')
            if input.get('required') is True:
                required.append(input.get('id'))
            append_input(input)

        # Iterate over sbdk schema outputs and call append_output
        for order, output in enumerate(sbdk_schema_outputs):
            if output.get('required') is True:
                required.append(output.get('id'))
            append_output(output)

        # Iterate over sbdk schema params and call append_input
        for order, param in enumerate(sbdk_schema_params):
            if param.get('_extra').get('arg') is None:
                prefix = raw_input('Enter prefix for Param ' + ''.join(
                    ['{id: "', param['id'], '", name: "', param['name'], '"}:']))
            else:
                prefix = param.get('_extra').get('arg')
            if param.get('required') is True:
                required.append(param.get('id'))
            append_param(param)

        # Dump rabix_schema to output.json
        with open('.'.join([wrapper[0], wrapper[-1], 'cwl.json']), 'w') as out_file:
            json.dump(rabix_schema, out_file, separators=(',', ':'))
