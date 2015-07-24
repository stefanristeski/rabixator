import json
from path import path

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


sbdk_schema = json.load(open('./gatk2.json'))[0]
sbdk_schema_inputs = sbdk_schema.get('schema').get('inputs')
sbdk_schema_params = sbdk_schema.get('schema').get('params')
sbdk_schema_outputs = sbdk_schema.get('schema').get('outputs')
wrapper = path(sbdk_schema.get('wrapper_id')).ext[1:]

required = []

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

    # append '.' to description
    description = input.get('description')
    if description and not description.endswith('.'):
        description = ''.join([description, '.'])

    inputs = rabix_schema.get('inputs')
    inputs.append(
        {
            "inputBinding": {"prefix": prefix, "separate": True, "itemSeparator": " "},
            "type": [input_type] if input.get('id') in required else ["null", input_type],
            "id": ''.join(['#', input.get('id')]),
            "description": description.capitalize() if description else "",
            "label": input.get('name'),
            "sbg:category": "Inputs",
        }
    )
    rabix_schema['inputs'] = inputs


# Append output
def append_output(output):
    if output.get('list') is True:
        output_type = {"type": "array", "items": "File"}
    else:
        output_type = "File"

    # append '.' to description
    description = input.get('description')
    if description and not description.endswith('.'):
        description = ''.join([description, '.'])

    outputs = rabix_schema.get('outputs')
    outputs.append(
        {
            "type": [output_type] if output.get('id') in required else ["null", output_type],
            "id": ''.join(['#', output.get('id')]),
            "description": description.capitalize() if description else "",
            "label": input.get('name'),
        }
    )
    rabix_schema['outputs'] = outputs


# Append param
def append_param(param):
    if param.get('type') == 'string':
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

    # add '.' and 'default' to description
    description = param.get('description')
    if description and not description.endswith('.'):
        description = ''.join([description, '.'])
    if description and param.get('default'):
        description = ' '.join([description, ' [default: ', str(param.get('default')), ']'])

    inputs = rabix_schema.get('inputs')
    inputs.append(
        {
            "inputBinding": {"prefix": prefix, "separate": True, "itemSeparator": " ",  "sbg:cmdInclude": True},
            "type": [param_type] if param.get('id') in required else ["null", param_type],
            "id": ''.join(['#', param.get('id')]),
            "description": description.capitalize() if description else "",
            "label": param.get('name'),
            "sbg:category": param.get('category'),
        }
    )
    rabix_schema['inputs'] = inputs


# Iterate over sbdk schema inputs and call append_input
for order, input in enumerate(sbdk_schema_inputs):
    if input.get('_extra').get('arg') is None:
        prefix = raw_input('Enter prefix for Input ' + ''.join(
            ['{id: "', input['id'], '", name: "', input['name'], '", description: "', input['description'], '"}:']))
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
            ['{id: "', param['id'], '", name: ', param['name'], '", description: "', param['description'], '"}:']))
    else:
        prefix = param.get('_extra').get('arg')

    if param.get('required') is True:
        required.append(param.get('id'))

    append_param(param)

# Dump rabix_schema to output.json
with open('output.json', 'w') as out_file:
    json.dump(rabix_schema, out_file, separators=(',', ':'))