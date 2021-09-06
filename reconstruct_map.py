import numpy as np
import matplotlib.pyplot as plt
import healpy as hp
import os
import copy

class Reconstructor:
    
    '''
    Takes in ampitude scale factors. Each amp scale factor multiplies the input_base for the particular region defined in the mask arrays
    '''

    def __init__(self, amp_scale_factors, foreground_map, masks, **kwargs):
        self.amp_scale_factors = amp_scale_factors
        self.unperturbed_foreground_map = foreground_map
        self.masks = masks
        self.return_residuals = kwargs.pop('return_residuals', False)


    def reconstruct_map(self):
        self.reconstructed_map = np.zeros_like(self.unperturbed_foreground_map)
        for i in range(len(self.amp_scale_factors)):
            self.reconstructed_map += self.amp_scale_factors[i]*np.multiply(self.unperturbed_foreground_map, self.masks[:,i])

        if self.return_residuals:
            self.residuals = np.subtract(self.unperturbed_foreground_map, self.reconstructed_map)

    '''
    #this method reconstructs the map by multiplying the basemap by the scalefactors for each region defined in masks
    #if there are any points in between regions, i.e. the masks don't fully span the basemap, then those pixels are
    #obviously the basemap pixels, and so we would never know if there are stragglers. The above method reconstruct_map
    #rebuilds the basemap from scratch and so it will be apparent if there are any straggling pixels. It is recommended to use
    #reconstruct_map method
    '''
    def reconstruct_map_notfromscratch(self):
        self.reconstructed_map = copy.deepcopy(self.unperturbed_foreground_map)
        for i in range(len(self.amp_scale_factors)):
            #which pixels are we multiplying??
            non_zero_pix = np.where(self.masks[:,i] != 0)
            
            self.reconstructed_map[non_zero_pix] = self.amp_scale_factors[i]*self.unperturbed_foreground_map[non_zero_pix]
    
        if self.return_residuals:
            self.residuals = np.subtract(self.unperturbed_foreground_map, self.reconstructed_map)


    def plot(self, data_map, **kwargs):
        
        #plot saturates at vmax
        vmax = kwargs.pop('vmax', 900)
        
        percentile_buffer_high = kwargs.pop('percentile_buffer_high', 99)
        percentile_buffer_low = kwargs.pop('percentile_buffer_low', 1)
        
        mean_reconstructed = np.mean(self.reconstructed_map)
        mean_unperturbed_foreground_map = np.mean(self.unperturbed_foreground_map)
        hp.visufunc.mollview(data_map , max = vmax, cmap = 'inferno', title = r'Data Foreground map, $\mu$ = ' + str(np.mean(data_map)))

        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize = (20,5))
        plt.axes(ax1)
        hp.visufunc.mollview(self.reconstructed_map , max = vmax, hold = True, cmap = 'inferno', title = r'Reconstructed map, $\mu = $' + str(mean_reconstructed))
        plt.axes(ax2)
        hp.visufunc.mollview(self.unperturbed_foreground_map , max = vmax, hold = True, cmap = 'inferno', title = r'Unperturbed Foreground map, $\mu$ = ' + str(mean_unperturbed_foreground_map))

        plt.show()
        plt.close()

    
        
        hp.visufunc.mollview(self.reconstructed_map - self.unperturbed_foreground_map  ,  min = self.compute_vmin_vmax(self.reconstructed_map - self.unperturbed_foreground_map, percentile_buffer_low), max = self.compute_vmin_vmax(self.reconstructed_map - self.unperturbed_foreground_map, percentile_buffer_high),   cmap = 'inferno', title = r'Residuals: Reconstructed - Unperturbed Model')
        
        
        hp.visufunc.mollview(self.reconstructed_map - data_map ,   max = self.compute_vmin_vmax(self.reconstructed_map - data_map, percentile_buffer_high),  min = self.compute_vmin_vmax(self.reconstructed_map - data_map, percentile_buffer_low),  cmap = 'RdBu', title = r'Residuals: Reconstructed - Data')
    
        hp.visufunc.mollview(self.reconstructed_map - data_map ,   max = 15,  min = -15,  cmap = 'RdBu', title = r'Saturated Residuals: Reconstructed - Data')

    
    def compute_vmin_vmax(self, map, percentile_buffer):
                
        flatten_values = map.flatten()
        sorted_temperatures = np.sort(flatten_values)
        '''
        checks that the percentile is working
        num_gtr = float(len(sorted_temperatures[sorted_temperatures > temp_min]))
        num_lt = float(len(sorted_temperatures[sorted_temperatures < temp_min]))
                    
        print(temp_min, 'greater than that number: '  , float(num_gtr)/len(sorted_temperatures), 'less than that number: '  , float(num_lt)/len(sorted_temperatures)  )
        '''
                        
        return np.percentile(sorted_temperatures ,  percentile_buffer)









