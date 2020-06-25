
import argparse
import sys,torch,json,os
import numpy as np
import spartan2.spartan as st

st.config(st.engine.SINGLEMACHINE)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名")

    parser.add_argument("--model", type=str, default="/",
                        help="模型路径")
    parser.add_argument("--network_config", type=str, default="beatgan_config.json",
                        help="网络配置文件")

    parser.add_argument("-o", "--output", type=str, default='output.csv',
                        help="输出文件名")
    args = parser.parse_args()

    args_input = args.input
    args_model_path=args.model
    args_config=args.network_config
    
    args_output = args.output

    input_path,input_name=os.path.split(args_input)
    

    # load time data
    
    ts_seg=np.load(args.input)
    
    ad_model = st.anomaly_detection.create(None, st.ad_policy.BEATGAN, "my_model")

    with open(args_config, 'r') as load_f:
        param = json.load(load_f)
        param["model_path"] = args_model_path

    ad_model.init_model(param, device)

    beatgan,res = ad_model.run(None, ts_seg, param, device)

    np.savetxt("foo.csv", res[0], delimiter=",")
 
    
