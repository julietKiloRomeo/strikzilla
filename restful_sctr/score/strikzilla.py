# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:02:57 2017

@author: jkr
"""




import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd


def is_match(p,q, N, r_max):
    res = []
    
    for r in range(-int(r_max), int(r_max)+1):
        # k of each?
        if (((N-r*q)%(p+q)) == 0 ):
            k   = (N-r*q)/(p+q)
            res += [(k,k+r)]

    return res

def get_solutions(N, dN):

    r_max = dN - 1.

#    upper_limit = lambda p2: max(N*2.0/(dN+r_max) -(dN-r_max)*1./(dN+r_max)*p2, 0)
#    lower_limit = lambda p2: max(N*2.0/(dN-r_max) -(dN+r_max)*1./(dN-r_max)*p2, 0)
    
    p1_max = min(np.floor(2.*N/(dN-r_max)), 2.*N/(dN))
    
#    p1_min_frac = (N*1./dN)
    p1_min = np.ceil(N*1./dN)
    p1_max = 2*p1_min
    
    p2_max = p1_min
    p2_min = 0


    all_solutions = []
    for p in range(int(p1_min), int(p1_max)+1):
        for q in range(p2_min, int(p2_max)+1):# range( int(np.ceil(lower_limit(p))), int(np.floor(upper_limit(p)))):
            possible_matches = is_match(p,q, N, r_max)
            if possible_matches is not None:
                for res in possible_matches:
                    is_actual_match = sum(res)==dN
                    if is_actual_match:
                        all_solutions += [(p,q,res)]
                        
    if len(all_solutions) == 0:
        return None
        
    return sorted(all_solutions, key=lambda t: abs( t[0]-t[1] )+abs( t[2][0]-t[2][1] )   )[0]


def xcrease(start_masks, end_masks, verbose=True):

    N     = start_masks
    dN    = abs(end_masks - start_masks)
    sign  = np.sign(end_masks - start_masks)
        
    sol = get_solutions(N, dN)
    
    instr = ''
    
    if sol is None:
        print '!'*20
        print start_masks, end_masks
        print '!'*20
        return None
        
    p,q,res = sol

    if res[0]>=res[1]:
        p_most  = p
        p_least = q
        n_most  = res[0]
        n_least = res[1]
    else:
        p_most  = q
        p_least = p
        n_most  = res[1]
        n_least = res[0]

    instructions = ''
    
    n_middle = n_least
    n_repeat = n_most/n_least
    n_start  = (n_most - n_middle*n_repeat)/2
    n_end    = n_most - n_middle*n_repeat - n_start

    sym_most  = 'X '
    sym_least = 'O '
    sym_sign  = '+' if sign>0 else '-'

    for i in range(n_start):
        instructions += sym_most
    instructions += '  '
    for i in range(n_middle):
        instructions += sym_most*n_repeat+sym_least
    instructions += '  '
    for i in range(n_end):
        instructions += sym_most
        
    instr += '{:s} : {:d} of {:d} {:s} 1'.format(sym_least, n_least, p_least, sym_sign) + '\n'
    instr += '{:s} : {:d} of {:d} {:s} 1'.format(sym_most, n_most, p_most, sym_sign) + '\n'
    instr += instructions
    if verbose:
        print instr

    return sol, instr, n_start, n_middle, n_end

##%%
#
#
#for start_masks in range(30, 150):
#    for dN in range(2, start_masks*2/3+1):
#        for sign in [-1, 1]:
#            end_masks = start_masks + sign*dN
#            xcrease(start_masks, end_masks, verbose=False)













