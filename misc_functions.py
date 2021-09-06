import healpy as hp
import numpy as np
import matplotlib.pyplot as pl
from scipy import stats
import copy
import os

#extrapolate
def extrapolate_in_nu(map_in, nu_base, nu_desired, beta):
    map_in_copy = map_in.copy()
    return map_in_copy*(nu_desired/nu_base)**(-beta)

def extrapolate_in_nu_perpixel(map_in, nu_base, nu_desired, beta):
    map_in_copy = map_in.copy()
    extrapolated_map = np.zeros_like(map_in_copy)
    for i in range(len(extrapolated_map)):
        extrapolated_map[i] = map_in_copy[i]*(nu_desired/nu_base)**(-beta[i])
    return extrapolated_map

def apply_hp_mask(map_in, threshold):
    map_out = map_in.copy()
    for i in range(map_in.shape[0]):
        if map_in[i] == threshold:
            map_out[i] = hp.UNSEEN
    return map_out

#they both do the same thing
def apply_hp_mask(map_in, threshold):
    mask = np.where(map_in <= threshold)
    map_out = map_in.copy()
    for i in range(len(mask[0])):
        map_out[mask[0][i]] = hp.UNSEEN
    
    return map_out


def replace_area_with_number(map_to_be_replaced, value, map_replacer):
    #takes in a map, finds the masked regions and replaces it with the value found in another map
    map_to_be_replaced_copy = map_to_be_replaced.copy()
    map_replacer_copy = map_replacer.copy()
    regions_to_replace = np.where(map_to_be_replaced_copy == value)
    ctr = 0
    for i in range(len(regions_to_replace[0])):
        map_to_be_replaced_copy[regions_to_replace[0][i]] = map_replacer_copy[regions_to_replace[0][i]]
        ctr += 1
    print(str(ctr) + ' points were replaced ')

    return map_to_be_replaced_copy


def copy_masked_area_from_one_to_another(map_with_masks, map_to_be_masked):
    #takes in a map, finds the masked regions and replaces it with the value found in another map
    map_with_masks_copy = map_with_masks.copy()
    map_to_be_masked_copy = map_to_be_masked.copy()
    regions_to_replace = np.where(map_with_masks_copy == hp.UNSEEN)
    for i in range(len(regions_to_replace[0])):
        map_to_be_masked_copy[regions_to_replace[0][i]] = hp.UNSEEN
    
    return map_to_be_masked_copy


def mean_unmasked_region(map_with_masks, mask_value):
    masked_regions = np.where(map_with_masks == mask_value)
    #make a copy
    map_with_masks_copy = map_with_masks.copy()
    try:
        n = 0
        for i in range(len(masked_regions[0])):
            map_with_masks_copy[masked_regions[0][i]] = 0
            n += 1
        return np.sum(map_with_masks_copy)/float(len(map_with_masks_copy ) - n)
    except:
        print('There are no masked regions')
        return np.mean(map_with_masks_copy)



def convert_ell_to_degrees(ell):
    return float(360)/float(2*ell)

def convert_ell_to_rads(ell):
    return float(2*np.pi)/float(2*ell)
