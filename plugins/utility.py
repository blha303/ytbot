from util import hook, text
import hashlib
import collections
import re

# variables

colors = collections.OrderedDict([
  ('red',     '\x0304'),
  ('ornage',  '\x0307'),
  ('yellow',  '\x0308'),
  ('green',   '\x0309'),
  ('cyan',    '\x0303'),
  ('ltblue',  '\x0310'),
  ('rylblue', '\x0312'),
  ('blue',    '\x0302'),
  ('magenta', '\x0306'),
  ('pink',    '\x0313'),
  ('maroon',  '\x0305')
])

# helper functions

strip_re = re.compile("(\x03|\x02|\x1f)(?:,?\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)


def strip(text):
    return strip_re.sub('', text)
