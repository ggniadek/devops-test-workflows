# tmp-devops-test-workflows

Each test case consists of three files:

- `example.ipynb`: the notebook containing the source for all workflow components. The beginning of each cell contains a description of the cell's inputs, outputs, parameters, confs, secrets and dependencies ([documentation](https://naavre.net/docs/NaaVRE_Interface/#overriding-definition-of-cell-inputs-and-outputs)). Those notebooks can be opened locally with Jupyter Lab.
- `example.naavrewf`: the workflow in the NaaVRE graphical editor format. These files can be can visualize in the [NaaVRE Open Lab](https://naavre.lifewatch.dev/vreapp/vlabs/openlab). However, they can't be run directly. If you need to run them, first containerize the cells from the notebook ([tutorial](https://naavre.net/docs/tutorials/)), then build a similar workflow with your own cells.
- `example.argo.yaml`: the workflow in the Argo Workflows format. You can run this on any Argo Workflows instance.
