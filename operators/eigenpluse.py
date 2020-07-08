import sys
sys.path.append('..')
import spartan2.spartan as st

# set the computing engine
st.config(st.engine.SINGLEMACHINE)

# load graph data
data = st.loadTensor(name = "example", path = "../live-tutorials/inputData/", col_types = [int, int], hasvalue=0)

graph = data.toGraph()

# create a eigen decomposition model
edmodel = st.anomaly_detection.create(graph.sm, "EIGENPLUSE", "my_svds_model")
outlier = edmodel.run(k=10)
print(outlier)
