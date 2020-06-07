
import argparse
import sys,torch
import sys,os
sys.path.append("/Users/zhoubin/Project/Lab/spartan2")
import spartan2.spartan as st

st.config(st.engine.SINGLEMACHINE)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名")
    
    parser.add_argument('--input_path', type=str, default="inputData/",
                        help="输入文件目录")
    parser.add_argument("--attrlabels",type=str,default="1,2,3",
                        help="时间序列的列名，以,分割")
    parser.add_argument("--model_path",type=str,default="/",
                        help="模型路径")
    parser.add_argument("--model_name", type=str, default="my_model",
                        help="模型名字（自定义）")
    parser.add_argument("--network", type=str, default="CNN",
                        help="模型网络 CNN/RNN")
    parser.add_argument("--net_type", type=str, default="gru",
                        help="RNN单元 gru/rnn/lstm")
    parser.add_argument("--layers", type=int, default=1,
                        help="RNN层数")
    parser.add_argument("--hidden_size", type=int, default=1,
                        help="RNN隐层神经元个数")
    parser.add_argument("--seq_len", type=int, default=64,
                        help="序列长度")
    parser.add_argument("--stride", type=int, default=64,
                        help="序列分割滑动步长")
    parser.add_argument("--input_size", type=int, default=1,
                       help="序列维度")
    parser.add_argument("--rep_size", type=int, default=10,
                       help="编码长度")
    parser.add_argument("--batch_size", type=int, default=64,
                        help="batch大小")
    parser.add_argument("--lamb", type=float, default=1.0,
                        help="lambda参数")
    
    

    parser.add_argument("-o", "--output", type=str, default='/source/out.jpg',
                        help="输出文件名")
    args = parser.parse_args()

    args_input = args.input
    args_input_path=args.input_path
    args_attrlabels=args.attrlabels.split(",")
    args_model_name=args.model_name
    
    args_model_path=args.model_path
    args_network = args.network
    args_net_type = args.net_type
    args_layers = args.layers
    args_hidden_size = args.hidden_size
    args_seq_len = args.seq_len
    args_stride = args.stride
    args_input_size = args.input_size
    args_rep_size = args.rep_size
    args_batch_size = args.batch_size
    args_lamb = args.lamb
    
    
    
    args_output = args.output

    # load time data
    data = st.loadTensor(name=args_input, path=args_input_path, col_types=[float, float, float], hasvalue=True)
    time_series = data.toTimeseries(attrlabels=args_attrlabels)
    ad_model = st.anomaly_detection.create(time_series, st.ad_policy.BEATGAN, args_model_name)

    param_run = {
        'model_path': args_model_path,
        'network': args.network,
        'net_type': args.net_type,
        'layers': args.layers,
        'seq_len': args.seq_len,
        'stride': args.stride,
        'input_size': args.input_size,
        'hidden_size': args.hidden_size,
        'rep_size': args.rep_size,
        'batch_size': args.batch_size,
        'max_epoch': 5,
        'lr': 0.01,
        'lambda': args_lamb
    }

    ad_model.init_model(param_run, device)

    beatgan,res = ad_model.run(None, time_series, param_run, device)
    
    with open(args_output,"w") as f:
        f.write(str(res))
    
    
