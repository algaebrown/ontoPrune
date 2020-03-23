import numpy as np
from ddot import Ontology
import pandas as pd
def find_term_child(ont_table, terms):
    '''
    find child term of low entropy term
    '''
    termterm = ont_table.loc[ont_table['EdgeType'] == 'Child-Parent']
    child = termterm.loc[termterm['Parent'].isin(terms)]['Child']
    
    return(set(child))
def find_child(ont_table, term):
    '''
    find child for one term
    return two list, gene_list, and term_list
    '''
    child = ont_table.loc[ont_table['Parent'] == term]
    gene_list = child.loc[child['EdgeType'] == 'Gene-Term']['Child'].tolist()
    term_list = child.loc[child['EdgeType'] == 'Child-Parent']['Child'].tolist()
    
    return gene_list, term_list
    

def delete_term_by_entropy(ont, term_entropy, entropy_thres):
    '''
    prune ontology based on normalized entropy
    return trimmed ontology and No. terms trimmed
    '''
    terms = term_entropy.loc[term_entropy['normalized entropy']< entropy_thres].index
    
    # find children to delete
    ont_table = ont.to_table()
    child_to_delete = find_term_child(ont_table, terms)
    
    # delete it!
    del_ont = ont.delete(child_to_delete, preserve_transitivity=True, inplace = False)
    
    return(del_ont, len(child_to_delete))