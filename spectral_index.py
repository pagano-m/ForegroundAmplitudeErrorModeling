import os
import numpy as np
import matplotlib.pyplot as pl
import healpy as hp

class find_spec_index():
    '''
        This simple class takes in an input map and output map (both need to be in healpy ring format)
        and extrapolates one mean to the other ensuring that ONLY the mean is constant. If one map is masked, then the other map needs to have the same region masked
    '''
    def __init__(self, map1, map2, map1_freq, map2_freq):
        self.map1 = map1
        self.map2 = map2
        self.map1_freq = map1_freq
        self.map2_freq = map2_freq
        self.Tcmb = 2.725
        if self.map1.ndim != 1 or self.map2.ndim !=1:
            print('Incorrect dimension of map')
            raise IndexError
        
        #skip the CMB for now
        #self.map1 = np.subtract(self.map1 , self.Tcmb)
        #self.map2 = np.subtract(self.map2, self.Tcmb)

        #beta map
        #find the mean of the maps
        #first check whether the maps are masked
        
        #check map1
        masked_pixels = np.where(self.map1 == hp.UNSEEN)
        n = 0
        for i in range(len(masked_pixels[0])):
            self.map1[masked_pixels[0][i]] = 0
            n += 1
        
        self.mean1 = np.sum(self.map1)/float(len(self.map1) - n)
        
        
        masked_pixels2 = np.where(self.map2 == hp.UNSEEN)
        n = 0
        for i in range(len(masked_pixels2[0])):
            self.map2[masked_pixels2[0][i]] = 0
            n += 1
        self.mean2 = np.sum(self.map2)/float(len(self.map2) - n)
        
        
        if (self.map2_freq > self.map1_freq):
                
                self.beta = np.log(self.mean2/self.mean1)/np.log(self.map1_freq/self.map2_freq)
        else:
                self.beta = np.log(self.mean1/self.mean2)/np.log(self.map2_freq/self.map1_freq)










