BASE_TEMPLATE = '''Physical condition: {{phys}}
Mental performance: {{mind}}
Energy: {{energy}}
Mood: {{mood}}
{specific}

Notes: {{notes}}'''

TEMPLATES = {'morning': BASE_TEMPLATE.format(specific="Sleep quality: {sleep}"),
             'midday':  BASE_TEMPLATE.format(specific=""),
             'evening': BASE_TEMPLATE.format(specific="Physical perf.: {perf}")}

REGEX_TEMPLATES = {key: template.replace('{notes}', r'(?P<notes>.*)$')
                                .replace('{',r'(?P<')
                                .replace('}',r'>\d+)')
                   for key, template in TEMPLATES.items()}
