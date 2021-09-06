import ssh_python
import numpy as np
import read_in_posterior_info as RIP
import reconstruct_map as rm
import os
import sys

file = sys.argv[1]
location = sys.argv[2]
Nbeta = int(sys.argv[3])
Nscafac = int(sys.argv[4])

#Download info
file = '/home/grx40/scratch/Scale_Factor_Nreg/150MHz_wSpecComplex/NoScafacs/'
location = '/users/michael/'
ssh_python.transfer_from(file, location)



chunk1 = 'BOTHAXES_150MHzAbsErrsRayleighJeansDrawPspecFractionalErrsScaled_fitwAllSky150_Nscafac_'
chunk2 = '_60MinObs_SpectralComplexity_N'


#Read in analyses
reader_obj = RIP.read_in(location, [chunk1, chunk2], Nbeta, Nscafac, include_zero_scafac = False)

reader_obj.plot_grid(saturation_lower_limit = 260, saturation_upper_limit = None, color_scheme = 'YlOrRd')

reader_obj.pass_fail_grid()

reader_obj.image_grid()
