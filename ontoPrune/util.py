import numpy as np
from ddot import Ontology
import pandas as pd
def check_ontology_structure(ont, terminal_terms):
    '''
    given ontology and a set of terminal terms,
    return ontology statistics: max level, max depth, genes connected to rootm no.genes, no. terms, no. gene-term, no. term-term.
    '''
    #rand_genes = random.sample(ont.genes,50)
    
    root = ont.get_roots() # MF, CC, BP roots
    
    # check depth and level; whether is an imbalanced tree
    terminal_terms = list(set(terminal_terms).intersection(ont.terms)) # cannot check terms that don't exist (purned)
    long = ont.longest_paths(terminal_terms, root) #gene * root numpy array
    max_long = long.max(axis = 0)
    short = ont.shortest_paths(terminal_terms, root)
    max_short = long.max(axis = 0)
        
    # check how many genes directly connect to root
    ont_tbl = ont.to_table()
    rt_gene = ont_tbl.loc[(ont_tbl['EdgeType']=='Gene-Term') & (ont_tbl['Parent'].isin(root))].groupby(by = 'Parent').count()['Child']
    rt_gene = rt_gene/len(ont.genes)
    
    stat = np.concatenate((max_long, max_short,rt_gene.values)).reshape(3, len(root))
    
    # check number of term per level
    # memory expensive don't do that
    
    # summary
    n_gene = len(ont.genes)
    n_term = len(ont.terms)
    n_geneterm = sum([len(x) for x in ont.gene_2_term.values()])
    n_termterm = sum([len(x) for x in ont.parent_2_child.values()])
    
     
    
    
    return(stat, [n_gene, n_term, n_geneterm, n_termterm])
