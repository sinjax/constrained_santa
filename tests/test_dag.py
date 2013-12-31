import santa.dag as d
def test_dag():
	dag = d.DAG()
	r = dag.node("root")
	c1l1 = dag.node("c1l1")
	c2l1 = dag.node("c2l1")
	c3l1 = dag.node("c3l1")
	dag.connect(r,c1l1)
	dag.connect(r,c2l1)
	dag.connect(r,c3l1)
	dag.connect(c1l1,r)

	assert len(dag.children(r)) == 3
	assert len(dag.parents(r)) == 1
	assert len(dag.parents(c1l1)) == 1
