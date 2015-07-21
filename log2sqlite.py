import re
import sys
import json
import itertools
import argparse
import dataset
import json
from abc import abstractmethod

logging = False
def LOG(s):
  if logging:
    if type(s).__name__ == "str":
      print s
    else:
      print str(s)

class Parser(object):

    @abstractmethod
    def recorditer(self, inputstr):
        pass


class GrappaLogParser(Parser):
    _paramjsonpat = re.compile(r'PARAMS{[^}]+}PARAMS')
    _statjsonpat = re.compile(r'STATS{[^}]+}STATS')
    _frontpat = re.compile(r'0+:')
    _statspat = re.compile(r'STATS')
    _paramspat = re.compile(r'PARAMS')
    _lastcomma = re.compile(r',[^",}]+}') # if one exists

    def __init__(self, includes_params=True):
        self.includes_params = includes_params

    @classmethod
    def _raw_to_dict(cls, raw, tagpattern):
        # find the next experimental result
        found = raw.group(0)

        # remove STATS tags
        notags = re.sub(tagpattern, '', found)

        # remove mpi logging node ids
        noids = re.sub(cls._frontpat, '', notags)

        # json doesn't allow trailing comma
        notrailing = re.sub(cls._lastcomma, '}', noids)

        LOG(notrailing)
        asdict = json.loads(notrailing)
        return asdict

    def recorditer(self, inputstr):
        if self.includes_params:
            # concurrently search for adjacent pairs of PARAMS and STATS
            for praw, sraw in itertools.izip(
                    re.finditer(self._paramjsonpat, inputstr),
                    re.finditer(self._statjsonpat, inputstr)):

                result = {}
                result.update(self._raw_to_dict(praw, self._paramspat))
                result.update(self._raw_to_dict(sraw, self._statspat))
                yield result
        else:
            for sraw in itertools.izip(
                    re.finditer(self._statjsonpat, inputstr)):

                result = {}
                result.update(self._raw_to_dict(sraw, self._statspat))
                yield result


class Processor(object):

    @abstractmethod
    def processrecord(self, record):
        pass

    @abstractmethod
    def close(self):
        pass


class SQLiteProcessor(Processor):

    def __init__(self, dbname, tablename):
        self.db = dataset.connect('sqlite:///{0}'.format(dbname))
        self.table = self.db[tablename]
        self.rows_to_insert = []

    def processrecord(self, record):
        for k in self.table.columns:
          if not k in record:
            record[k] = None   # for missing columns put None

        self.rows_to_insert.append(record)

    def close(self):
        self.table.insert_many(self.rows_to_insert)


def run(inputstr, parser, processor):
    count = 0
    for r in parser.recorditer(inputstr):
        processor.processrecord(r)
        count += 1

    processor.close()
    print "processed {0} records".format(count)

if __name__ == '__main__':
    p = argparse.ArgumentParser(prog=sys.argv[0])
    p.add_argument("-d", dest="dbname", required=True, help="database name")
    p.add_argument("-t", dest="tablename", required=True, help="table name")
    p.add_argument("-i", dest="inputf", required=True,
                   help="input log file; may contain multiple records")
    p.add_argument("-v", dest="verbose", action="store_true", help="turn on verbose logging")

    args = p.parse_args(sys.argv[1:])
    logging = args.verbose 

    with open(args.inputf, 'r') as inf:
        run(inf.read(),
            GrappaLogParser(),
            SQLiteProcessor(args.dbname, args.tablename))
