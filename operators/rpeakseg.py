import argparse
import sys, os
import spartan2.spartan as st

st.config(st.engine.SINGLEMACHINE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名")

    parser.add_argument("--attrlabels", type=str, default="1,2,3",
                        help="时间序列的列名，以,分割")
    parser.add_argument("--sample_rate", type=int, default=360,
                        help="采样率")
    parser.add_argument("--left", type=int, default=120,
                        help="r峰前段长度")
    parser.add_argument("--right", type=int, default=136,
                        help="r峰后段长度")

    parser.add_argument("-o", "--output", type=str, default='output.csv',
                        help="输出文件名")
    args = parser.parse_args()


    input_path, input_name = os.path.split(args.input)

    # load time data
    data = st.loadTensor(name=input_name, path=input_path, col_types=[float, float, float], hasvalue=True)
    time_series = data.toTimeseries(attrlabels=args.attrlabels)

    seg = st.series_segmentation.create(time_series, st.sseg_policy.RPeaks, "rpeak")

    ts_segs = seg.run(args.sample_rate, args.left, args.right, args.output)
    


