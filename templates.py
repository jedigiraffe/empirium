INPUT_TEMPLATE = '''Mood: {mood}
Physical performance: {phys}'''

REGEX_TEMPLATE = INPUT_TEMPLATE.format(mood=r'(?P<mood>\d+)',
                                       phys=r'(?P<phys>\d+)')
