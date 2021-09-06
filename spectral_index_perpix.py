import os
import numpy as np
import matplotlib.pyplot as pl
import healpy as hp
import misc_functions as mf

class SI_calculator():
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
        self.mask_cutoff = -1e20
        if self.map1.ndim != 1 or self.map2.ndim !=1:
            raise IndexError('Incorrect dimension of map')
        if len(self.map1) != len(self.map2):
            print('maps are not the same nside')
            if len(self.map2) > len(self.map1):
                try:
                    self.map1 = hp.pixelfunc.ud_grade(self.map1, int(np.sqrt(len(self.map2)/12.)))
                except:
                    raise IndexError('Check the nsides')
            else:
                raise IndexError('The target map has a smaller nside than the first map')

        #beta map
        self.beta = np.log(np.true_divide( np.subtract(self.map1, self.Tcmb), np.subtract(self.map2 , self.Tcmb)))/float(np.log(self.map2_freq/self.map1_freq))
        
        #check to see if there are any masked pixels
        masked_pixels1 = np.where(self.map1  < self.mask_cutoff)
        if len(masked_pixels1[0]) > 0:
            #there are masked pixels so mask the pixels in the beta map
            self.beta = mf.apply_hp_mask(self.beta, self.mask_cutoff)
        
        #now check map2
        masked_pixels2 = np.where(self.map1  < self.mask_cutoff)
        if len(masked_pixels2[0]) > 0:
            #there are masked pixels so mask the pixels in the beta map
            self.beta = mf.apply_hp_mask(self.beta, self.mask_cutoff)



class extrapolate_per_pixel:
    '''
        This class takes in a map at a specific frequency, and then extrapolates it to
        another frequency using a user specified spectral index map. The model for such an extrapolation is
        does not assume any spectral curvature
    '''

    def __init__(self, input_map,  nu_0, nu_desired, beta_map):
        self.input_map = input_map
        self.nu_0 = nu_0
        self.nu_desired  = nu_desired
        self.beta_map = beta_map
        self.Tcmb = 2.725
        self.mask_cutoff = -1e20

        self.extrapolated_map = np.zeros_like(self.input_map)

        for i in range(len(self.extrapolated_map)):
            self.extrapolated_map[i] = ((self.input_map[i]- self.Tcmb)*(nu_desired/nu_0)**(-self.beta_map[i]) )+self.Tcmb

        #are there any masks in our input map?
        if len(np.where(self.input_map <= self.mask_cutoff)[0]) > 0:
            print('there are masked pixels in the input map, re-masking them after the extrapolation')
            self.extrapolated_map = mf.apply_hp_mask(self.extrapolated_map , 0)



class spectral_index_curvature:
    '''
        This class computes the spectral index and spectral curvature of foreground maps. The model is assumed to follow
        T_output = T_input exp( -beta*ln(nu_output/nu_input) + gamma*ln(nu_output/nu_input))**2
        In order to compute gamma and beta, we need to know the spectral (and temperature information) at three frequencies
        
    '''

    def __init__(self, map1,  map2, map3, nu_1, nu_2, nu_3 ):
        self.map1 = map1
        self.map2 = map2
        self.map3 = map3
        self.nu_1 = nu_1
        self.nu_2 = nu_2
        self.nu_3 = nu_3
        self.Tcmb = 2.725

        #let us write out two equations and then solve for beta and gamma point wise
        beta_coefficient_eq1 = -np.log(nu_2/nu_1)
        gamma_coefficient_eq1 = (np.log(nu_2/nu_1))**2
    
        #and equation 2
        beta_coefficient_eq2 = -np.log(nu_3/nu_2)
        gamma_coefficient_eq2 = (np.log(nu_3/nu_2))**2
        
        #put them into a matrix so numpy can understand
        coefficients = np.array([[beta_coefficient_eq1, gamma_coefficient_eq1], [beta_coefficient_eq2, gamma_coefficient_eq2]])
        
        #make copies of beta and gamma
        self.beta = np.zeros_like(self.map1)
        self.gamma = np.zeros_like(self.map1)
        
        #solve for the values at each pixel
        for i in range(len(self.map1)):
            RHS_eq1 = np.log(self.map2[i]) -np.log(self.map1[i])
            RHS_eq2 = np.log(self.map3[i]) - np.log(self.map2[i])
            RHSs = np.array([RHS_eq1, RHS_eq2])
            self.beta[i], self.gamma[i] = np.linalg.solve(coefficients, RHSs)

        #are there any masks in our input map?
        #if len(np.where(self.input_map <= self.mask_cutoff)[0]) > 0:
        ##    print('there are masked pixels in the input map, re-masking them after the extrapolation')
#   self.extrapolated_map = mf.apply_hp_mask(self.extrapolated_map , 0)







        
        
            
        
    
        







