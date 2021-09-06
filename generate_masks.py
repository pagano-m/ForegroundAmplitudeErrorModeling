import numpy as np
import matplotlib.pyplot as plt
import healpy as hp



class GenerateMasks:

    '''
    Takes in the number of scafac and an input_map and splits the map based on percentile
    '''

    def __init__(self,N_reg_scafac, input_map ):

        self.masks = np.zeros(( len(input_map), N_reg_scafac))

        delta_per = 100./N_reg_scafac

        print('Jump in percentile increments of ' + str(delta_per))
        
        reg = 1
        while(reg <= N_reg_scafac):
            masks_ = np.zeros(( len(input_map)))
            if reg == N_reg_scafac:
                masks_[input_map > np.percentile(input_map ,  delta_per*(reg-1))] = 1
                self.masks[:,-1] = masks_
                print('Last region consists of points greate than ' , np.percentile(input_map ,  delta_per*(reg-1)))
                reg += 1
                continue
            if reg == 1:
                masks_[input_map <= np.percentile(input_map ,  delta_per*reg)] = 1
                print('First region consists of points less than  ', np.percentile(input_map ,  delta_per*reg))
                
                self.masks[:,0] = masks_
                reg += 1
                continue
            masks_[(input_map > np.percentile(input_map ,  delta_per*(reg-1) )) & (input_map <= np.percentile(input_map ,  delta_per*reg))]  = 1
            
            low = np.percentile(input_map ,  delta_per*(reg-1))
            high = np.percentile(input_map ,  delta_per*reg)
            
            print('Region ' + str(reg-1) + ' consists of points between '+ str(low) + ' and ' + str(high))
            self.masks[:,int(reg- 1)] = masks_
            
            reg += 1

