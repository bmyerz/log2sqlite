import re
from parser import Parser
from log2sqlite import cli


class ImpalaLogParser(Parser):
    def recorditer(self, inputstr):
        querypat = re.compile(r'Running query: (?P<query>q\d+)[_a-z]+, no_codegen: (?P<ncodegen>\d+), scale: (?P<scale>\d+)\nTime:(?P<preptime>\d+[.]\d+)\nTime:(?P<runtime1>\d+[.]\d+)\nTime:(?P<runtime2>\d+[.]\d+)\n(?P<failmsg>(ABOVE QUERY FAILED:1)?)')

        for m in re.finditer(querypat, inputstr):
            # params
            r = {'machine': 'bigdata',
                 'system': 'impala',
                 'nnode': 16,
                 'codegen': 1-int(m.group('ncodegen')),
                 'scale': m.group('scale') 
            }

            # measures
            for k in ['query', 'runtime1', 'runtime2', 'preptime']:
                r[k] = m.group(k)

            if m.group('failmsg') != '':
                print "failed query {0}; not saving".format(r['query'])
                continue

            yield r


if __name__ == '__main__':
    cli(ImpalaLogParser())
