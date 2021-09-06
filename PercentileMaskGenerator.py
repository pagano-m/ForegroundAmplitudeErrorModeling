import numpy as np
import matplotlib.pyplot as plt
import healpy as hp


'''
   This code takes in a map and splits the map into N_reg_scafac regions by percentile
   Future: give options to change this.
'''

def generate_masks(N_reg_scafac, input_map):
    

    masks = np.zeros(( len(input_map), N_reg_scafac))
    temp_divider = np.zeros((N_reg_scafac + 1))
    print('the temperature dividers are ' , len(temp_divider), ' long ')

    temp_divider[0] = np.min(input_map)
    temp_divider[-1] = np.max(input_map)

    print('The max of the map is ' , temp_divider[-1] )
    percentiles = np.linspace(1, 97, int(N_reg_scafac -1 ) )
    for i in range(N_reg_scafac - 1):
        print('dividing percentiles are ' , percentiles[i])
        temp_divider[i + 1] = np.percentile(input_map ,  percentiles[i])

    print('the temperature dividers are ', temp_divider )
    for i in range(N_reg_scafac - 1):
        print('values must be between ' ,temp_divider[i] , ' percentile and ' , temp_divider[i+1] )
        masks[:,i] = np.where((input_map >= temp_divider[i]) & (input_map < temp_divider[i+1]), 1,0 )

    masks[:, -1] = np.where((input_map >= temp_divider[-2]) & (input_map < temp_divider[-1]), 1,0 )



    #take a look to see if everything went well
    for i in range(N_reg_scafac):
        hp.visufunc.mollview(np.multiply(input_map, masks[:,i]) , cmap = 'inferno')
        pl.show()
        pl.close()

    return masks



