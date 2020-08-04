
import argparse
import sys,torch,json,os
import numpy as np
import spartan as st
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名")

    parser.add_argument("--model", type=str, default="/",
                        help="模型路径")
    parser.add_argument("--attrlabels",type=str,default="1,2,3",
                        help="时间序列的列名，以,分割")
    parser.add_argument("--network_config", type=str, default="beatgan_config.json",
                        help="网络配置文件")

    parser.add_argument("-o", "--output", type=str, default='output.csv',
                        help="输出文件名")
    args = parser.parse_args()

    args_input = args.input
    args_attrlabels=args.attrlabels.split(",")
    args_model_path=args.model
    args_config=args.network_config
    
    args_output = args.output

    

    # load time data
    time, value = st.loadTensor(path=args_input).toDTensor(hastticks=True)
    time_series = st.Timeseries(value, time)

    with open(args_config, 'r') as load_f:
        param = json.load(load_f)
        param["model_path"] = args_model_path

    beatgan = st.BeatGAN(time_series, **param)
    beatgan.fit()
    res = beatgan.predict()


    np.savetxt(args_output, res, delimiter=",")
 
    
