import argparse
import pandas as pd
import spartan as st

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名")
    argsinput = args.input

    x_data = pd.read_csv(argsinput, sep=",", header=None)
    st.util.geneutil.build_sampled_coexpression_matrix(x_data, "out")
