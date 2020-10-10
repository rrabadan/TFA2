import uproot
import numpy as np

def write_tuple(rootfile, array, branches, tree="tree") : 
  """
     Store numpy 2D array in the ROOT file using uproot. 
       rootfile : ROOT file name
       array : numpy array to store. The shape of the array should be (N, V), 
               where N is the number of events in the NTuple, and V is the 
               number of branches
       branches : list of V strings defining branch names
       tree : name of the tree
     All branches are of double precision
  """
  with uproot.recreate(rootfile, compression=uproot.ZLIB(4)) as file :  
    file[tree] = uproot.newtree( { b : "float64" for b in branches } )
    d = { b : array[:,i] for i,b in enumerate(branches) }
    #print(d)
    file[tree].extend(d)

def read_tuple(rootfile, branches, tree = "tree") : 
  """
    Load the contents of the tree from the ROOT file into numpy array. 
  """
  with uproot.open(rootfile) as file : 
    t = file[tree]
    a = [ t.array(b) for b in branches ]
  return np.stack(a, axis = 1)

def read_tuple_filtered(rootfile, branches, tree = "tree", selection = None, sel_branches = []) : 
  """
    Load the contents of the tree from the ROOT file into numpy array, 
    applying the selection to each entry. 
  """
  arrays = []
  with uproot.open(rootfile) as file : 
    t = file[tree]
    for data in t.pandas.iterate(branches = branches + sel_branches) : 
      if selection : df = data.query(selection)
      else : df = data
      arrays += [ df[list(branches)].to_numpy() ]
  return np.concatenate(arrays, axis = 0)
