#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.

from argparse import ArgumentParser
import random
from sys import stdin

from morph_seg.sequence_tagger.data import DataSet
from morph_seg.sequence_tagger.train import SequenceTagger, Config


def parse_args():
    p = ArgumentParser()
    p.add_argument('-N', type=int, default=1,
                   help="Number of experiments to run")
    p.add_argument('--dataframe-path', type=str, required=True,
                   help="Location of the dataframe for results")
    return p.parse_args()


def generate_config():
    from morph_seg.sequence_tagger import hyperparam_ranges
    hyperparam_ranges = reload(hyperparam_ranges)
    conf = {}
    for param, prange in hyperparam_ranges.ranges.items():
        conf[param] = random.choice(prange)
    return conf


def main():
    args = parse_args()
    dataset = DataSet(stdin)
    logging.info("Dataset loaded. Shape: {}".format(dataset.x.shape))
    for n in range(1, args.N+1):
        logging.info("Running experiment {}/{}".format(n, args.N))
        cfg = generate_config()
        logging.info(cfg)
        cfg['log_results'] = True
        cfg['dataframe_path'] = args.dataframe_path
        model = SequenceTagger(dataset, Config(cfg))
        model.run_train_test()
        logging.info("Test loss: {0}, test accuracy: {1}".format(
            model.result.test_loss, model.result.test_acc))

if __name__ == '__main__':
    import logging
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
