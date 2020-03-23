# ontoPrune
Information-theoretic approach to create a parsimonious Gene Ontology.
The purpose of doing this is to prepare a small-enough network for [Visible Neural Network (VNN)](https://github.com/idekerlab/DCell).

# How to use this directory?
Please refer to `notebook/` for a step-by-step walk through.

- `1_Calculate_Entropy_for_Terms.ipynb` demostrates how to calculate entropy for terms.
- `2_Visualize_Entropy.ipynb` show what terms are of low entropy.
- `3_Pruning_Low_Entropy.ipynb` removes child terms when parent terms are of low entropy. And examine the structure of the pruned ontology.
- `4_Pruned_ontology_quick_viz*.ipynb` visualizes the pruned ontology.
- `5_Get_Differential_Terms.ipynb` tries to make sure that the pruned ontology is still capable of distinguishing the difference between neuron and microglia.
- `6_Visualize_differential_term.ipynb` shows the "differential terms" between different cell types.
- `7_Output_to_DCell.ipynb` outputs the pruned ontology to DCell format. [See here for an example].

For those who are preparing the ontology for neural network, notebook 1,3,7 are the true pipeline. But taking at a look at the network statistic in notebook 3,5,6 might help you choose a better entropy threshold.

# Dependency?
Unfortunately this repository needs two seperate conda envrionment.
Most notebooks can work in [DDOT](https://github.com/michaelkyu/ddot) environment. see `ddot.yml`
Notebook 2 needs [GOATTOOLS]. see `ontoPrune.yml`
