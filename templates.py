from pprint import pprint

BASE_TEMPLATE = '''Mood: {{mood}}
Energy: {{energy}}
Mental performance: {{mind}}
Physical condition: {{phys}}
{specific}

Notes: {{notes}}'''

TEMPLATES = {'morning': BASE_TEMPLATE.format(specific="Sleep quality: {sleep}"),
             'midday':  BASE_TEMPLATE.format(specific=""),
             'night':   BASE_TEMPLATE.format(specific="Physical performance: {perf}")}

REGEX_TEMPLATES = {key: template.replace('{notes}', r'(?P<notes>.*)')
                                .replace('{',r'(?P<')
                                .replace('}',r'>\d+)')
                   for key, template in TEMPLATES.items()}
