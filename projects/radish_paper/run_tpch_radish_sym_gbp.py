from grappa import GrappaExperiment, MPIRunGrappaExperiment

tpch_bigdatann = MPIRunGrappaExperiment({
                                'trial': range(1, 3 + 1),
                                #'qn': [x for x in range(8, 20 + 1) if x!=7 and x!=9 and x!=8 and x!=10 and x!=11],  # exclude 7 that runs forever
                                #'qn': [x for x in range(1, 20 + 1) if x!=7 and x!=10 and x!=11 and x!=20],  # exclude 7 that runs forever
                                'qn': [x for x in range(1, 20 + 1) if x!=7],  # exclude 7 that runs forever
                                'exe': lambda qn: "grappa_tpc_q{0}_sym_gbp.exe".format(qn),
                                'sf': 10,
                                'ppn': 16,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'query': lambda qn: 'q{0}'.format(qn),
                                'vtag': 'v99-noalign',
                                'machine': 'bigdata',
                                'system': 'radish-sym-gbp-noalign'
                            },
                            {
                                'shared_pool_memory_fraction': 0.5
                            })

tpch_sampa = GrappaExperiment({
                                'trial': range(1, 3 + 1),
                                #'qn': [x for x in range(8, 20 + 1) if x!=7 and x!=9 and x!=8 and x!=10 and x!=11],  # exclude 7 that runs forever
                                'qn': [x for x in range(1, 20)], #if x!=7 and x!=10 and x!=11 and x!=20],  # exclude 7 that runs forever
                                'exe': lambda qn: "grappa_tpc_q{0}_sym_gbp.exe".format(qn),
                                'sf': 10,
                                'ppn': 12,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'query': lambda qn: 'q{0}'.format(qn),
                                'vtag': 'align-fix',
                                'machine': 'sampa',
                                'system': 'radish-sym-gbp'
                            },
                            {
                                'shared_pool_memory_fraction': 0.5
                            })


#tpch_bigdatann.run()
tpch_sampa.run()
