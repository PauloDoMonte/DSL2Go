def parse_model(line):
    parts = line.split('{')
    model_name = parts[0].split()[1]
    fields = parts[1].replace('}', '').strip().split()
    fields = [{'name': fields[i], 'type': fields[i+1]} for i in range(0, len(fields), 2)]
    return {'type': 'model', 'name': model_name, 'fields': fields}