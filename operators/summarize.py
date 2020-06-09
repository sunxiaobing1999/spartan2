# encoding: utf-8
import os
import sys

import numpy as np
import scipy.sparse as ssp

import sys
dir_ = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir_)
import spartan2.spartan as st
from spartan2.models.summarize.summarizer import Summarizer

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument('input', nargs='?', type=str, default=sys.stdin, help='edgelist 文件路径')
    parser.add_argument('--dataset', type=str, default='', help='数据集名称')
    parser.add_argument('-o', '--output', type=str, default='./outputData', help='输出目录')

    args = parser.parse_args()
    input_ = args.input
    dataset = args.dataset
    output = args.output

    t = st.loadTensor(input_, '', col_idx=None, col_types=[int, int], hasvalue=0)
    g = t.toGraph(bipartite=False, directed=False)
    sm = g.sm

    summarizer = Summarizer(sm)
    summarizer.summarize(dataset, output)