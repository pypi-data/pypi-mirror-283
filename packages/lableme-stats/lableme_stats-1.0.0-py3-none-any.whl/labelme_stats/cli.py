#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""comment here"""
import collections
import json
import os
import os.path as osp
import pprint
import sys
    

def entry():
    annotated_dir = sys.argv[1]
    counter = collections.Counter()
    file_counter = 0
    for dirpath, dirnames, filenames in os.walk(annotated_dir):
        for filename in filenames:
            if osp.splitext(filename)[-1] != '.json':
                continue
            filename = osp.join(dirpath, filename)
            file_counter += 1

            with open(filename) as f:
                data = json.load(f)
            for shape in data['shapes']:
                counter[shape['label']] += 1

    print(f'directory `{annotated_dir}` has {file_counter} json files')
    print('---')

    print('Statistics of Labels')
    for label, count in counter.items():
        print('{:>10}: {}'.format(label, count))
