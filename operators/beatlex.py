#!/usr/bin/env python
# encoding: utf-8
# @author: DingQuan
# @file: beatlex.py
# @time: 2020/6/15
# @version v1.0

import argparse
import numpy as np
import sys
import os
import json
import spartan as st


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件路径")

    parser.add_argument("--time_column_pos", type=int, default=0,
                        help="时间列的位置")
    parser.add_argument("--model_config", type=str, default="beatlex_config.json",
                        help="模型参数配置文件")

    parser.add_argument("-o", "--output", type=str, default='output.json',
                        help="输出文件名")

    args = parser.parse_args()
    args_input = args.input
    args_time_pos = args.time_column_pos
    args_config = args.model_config
    args_output = args.output

    time, value = st.loadTensor(path=args_input).toDTensor(hastticks=True)

    time_series = st.Timeseries(value, time)
    with open(args_config, 'r') as load_f:
        param = json.load(load_f)
    beatlex = st.BeatLex(time_series, **param)

    result = beatlex.run()

    with open(args_output, 'w') as writer:
        json_result = json.dumps(result, cls=NpEncoder)
        writer.write(json_result)
