from ddot import Ontology
import pandas as pd
import numpy as np
import warnings
import sys
sys.path.append('/cellar/users/hsher/ontoPrune')
from ontoPrune.prune import find_term_child
def count_gene(ont):
    '''
    count gene per term/term children for an ontology
    ont: ddot.Ontology
    
    return: Pandas.DataFrame, index = Term, value = gene count
    '''
    
    # find genes directly connected to term
    ont_table = ont.to_table()
    dir_connection = ont_table.loc[ont_table['EdgeType'] == 'Gene-Term']
    dir_count = dir_connection.groupby(by = 'Parent').count()['Child']
    
    # find term-term connection
    term_connection = ont_table.loc[ont_table['EdgeType'] == 'Child-Parent']
    term_count = term_connection.groupby(by = 'Parent').count()['Child']
    
    # find indirect connection (gene-term)
    pro_ont = ont.propagate(direction = 'forward', gene_term = True, term_term = False)
    pro_ont_table = pro_ont.to_table()
    indir_connection = pro_ont_table.loc[pro_ont_table['EdgeType'] == 'Gene-Term']
    indir_count = indir_connection.groupby(by = 'Parent').count()['Child']
    
    
    ont_count = pd.concat([dir_count, indir_count, term_count], axis = 1)
    ont_count.columns = ['direct gene count', 'indirect gene count', 'term count']
    ont_count.fillna(0, inplace = True)
    
    
    
    
    return ont_count 

def delete_empty_term(ont, ont_count):
    '''
    delete terms that has 0 or 1 gene, theoretically these terms contain no information at all
    '''
    ont_table = ont.to_table()
    # remove term with less gene
    zero_term = set(ont.terms) - set(ont_count.index)  # not even counted
    one_term = set(ont_count[ont_count['indirect gene count'] == 1].index)
    
    # remove term with only one child term, remove its child
    one_term_term = ont_count.loc[ont_count['direct gene count']+ont_count['term count'] == 1].index # in total only 1 child
    child_to_remove = find_term_child(ont_table,one_term_term)
        
    ont.delete(list(zero_term.union(one_term).union(child_to_remove)), preserve_transitivity=True, inplace = True)

def one_term_entropy(term, ont_table, ont_count):
    '''calculate entropy for one term'''
    child_count = []
    
    # for child "term"
    
    child_id = ont_table.loc[ont_table['EdgeType'] == 'Child-Parent'].loc[ont_table['Parent'] == term]['Child'] # child's id
    if len(child_id) > 0:
        child_count = child_count + ont_count.loc[child_id, 'indirect gene count'].tolist()
    
    
    # for child "gene"
    if ont_count.loc[term, 'direct gene count'] > 0:
        child_count = child_count + [1]*int(ont_count.loc[term, 'direct gene count']) # each gene count as a term of size 1
    
    no_children = len(child_count)
    
    if no_children < 1: 
        warnings.warn('term {} has {} child. Entropy not calculated'.format(term, no_children))
        return np.nan
    
    # normalized entropy
    child_prob = child_count/np.sum(child_count)
    normalized_entropy = -np.sum(np.multiply(child_prob, np.log(child_prob))/np.log(no_children))
    
    return(normalized_entropy)
    
    
def term_entropy(ont, ont_count):
    pass
    
    