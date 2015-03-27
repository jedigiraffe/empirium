#!/usr/bin/env python
import re
import os
import sys
import datetime
import optparse
import subprocess

from collections import defaultdict

from email.mime.text import MIMEText

from tempfile import NamedTemporaryFile

INPUT_TEMPLATE = '''Mood: {mood}
Physical performance: {phys}'''

REGEX_TEMPLATE = INPUT_TEMPLATE.format(mood=r'(?P<mood>\d+)',
                                       phys=r'(?P<phys>\d+)')

def get_input(editor, initial=''):
    with NamedTemporaryFile(delete=False) as tf:
        tfName = tf.name
        tf.write(initial)

    if subprocess.call([editor, tfName, '-w']) != 0: # Wait for file to close
        raise Exception("Sorry my friendo, the editor est muerte!")

    with open(tfName) as tf:
        contents = tf.read()
        os.remove(tfName)
        return contents

def verify_input(contents):
    if not re.match(REGEX_TEMPLATE, contents):
        print("Please follow the correct template!")
        sys.exit(1)

if __name__ == '__main__':
    contents = get_input('sublime', INPUT_TEMPLATE.format(mood='',
                                                          phys=''))
    parse_input(contents)