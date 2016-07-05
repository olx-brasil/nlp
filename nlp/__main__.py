from optparse import OptionParser

parser = OptionParser()
parser.set_usage('Usage: python -m nlp [options] # WORKING IN PROGRESS')
# parser.add_option("-f", "--file", dest="filename",
#                           help="write report to FILE", metavar="FILE")
# parser.add_option("-q", "--quiet",
#                           action="store_false", dest="verbose", default=True,
#                                             help="don't print status messages to stdout")

(options, args) = parser.parse_args()

import code;code.interact(local=dict(globals(),**locals()))

# print options
# print args
