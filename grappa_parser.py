import itertools
from log2sqlite import Parser, cli
from parameters import JSONParamsParser, PARAMS_TAG

__author__ = 'brandon'


class GrappaLogParser(Parser):
    def __init__(self, includes_params=True):
        self.includes_params = includes_params

    def recorditer(self, inputstr):
        jparams = JSONParamsParser(PARAMS_TAG)
        sparams = JSONParamsParser('STATS')

        if self.includes_params:
            # concurrently search for adjacent pairs of PARAMS and STATS
            for pdict, sdict in itertools.izip(
                jparams.idict_from_json(inputstr),
                    sparams.idict_from_json(inputstr)):

                result = {}
                result.update(pdict)
                result.update(sdict)
                yield result
        else:
            for sdict in itertools.izip(
                    jparams.idict_from_json(inputstr)):

                result = {}
                result.update(sdict)
                yield result


if __name__ == '__main__':
    cli(GrappaLogParser())
