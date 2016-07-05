from nlp.tag_cleaner import TagCleaner
from optparse import OptionParser
import codecs
import sys


parser = OptionParser()
parser.set_usage('Usage: python -m nlp [options]')
parser.add_option('-e', '--encoding', help='Set the input encoding (Default to utf-8)', dest='encoding', default='utf-8')
parser.add_option("-t", "--tag", action='store_const', const='tag_cleaner', dest='module', help='Set module to tag_cleaner (default)', default='tag_cleaner')

(options, args) = parser.parse_args()

if (len(args) > 0):
    file_input = open(args[0], 'r')
else:
    file_input = sys.stdin

body_raw = codecs.getreader(options.encoding)(file_input).read()

file_input.close()

if (options.module == 'tag_cleaner'):
    tag_cleaner = TagCleaner()
    tag_cleaner.loadModel('tagger')
    result = tag_cleaner.cleanBody(body_raw)

print result
