import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import image
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes


def read_horizontal(path2files, base_dir_name, N_dirs):
    

    #how many directories do we need to run the loop for?
    N_range = np.arange(N_dirs) + 1

    #initialize arrays to store the relevant information
    logZs = np.zeros_like(N_range)
    scale_factors = []
    betas  = []

    base_dir_name = [base_dir_name +  str(total) for counter, total in enumerate(N_range)  ]

    
    for ctr, beta_total in enumerate(N_range):
        f = open(os.path.join(path2files,base_dir_name[ctr] , 'test.stats'), 'r')
        lines = f.read()
        
        #this needs to be changed every time we do this :(
        #not anymore!
        where = base_dir_name[ctr].find('Nscafac_')
        N_reg_scafac = base_dir_name[ctr][(where + len('Nscafac_') ) : (where + len('Nscafac_') + 1)   ]
   
        
        
        r = lines.find('log(Z)       =')
        #print(lines[r+15:r + 39])
        logZs[ctr]  = float(lines[r+15:r + 40])
        
        scafacs = []
        sis = []
        #i = 0 corresponds to 1 dim
        print('-----------------------------Read in Betas and Scafacs -------------------------------------------------')
        for ctr_j , beta in enumerate(np.arange(beta_total) + 1):
            #which dim in test.stats are we reading?
            digit = str(beta)
            r = lines.find(digit + '  0.')
            #print('file ', os.path.join(path2files,base_dir_name[ctr]),  'dim ' , float(lines[r + 3:r + 26]))
            sis.append(float(lines[r+ 3:r + 26]))
        betas.append(sis)

        #Read in scale factors, if any
        for ctr_i , scafac in enumerate(np.arange(int(N_reg_scafac) ) + beta_total + 1):
            #which dim in test.stats are we reading?
            digit = str(scafac)
            r = lines.find(digit + '  0.')
            scafacs.append(float(lines[r+ 3:r + 26]))
        scale_factors.append(scafacs)

        
        
        
        f.close()


    betas = np.array(betas)
    scale_factors = np.array(scale_factors)


    plt.figure(figsize = (10,10))
    plt.ylabel(r'log(Z)', fontsize = 24)
    plt.xlabel(r'N', fontsize = 24)
    plt.title(r'N$_a$ = ' + str(N_reg_scafac) , fontsize = 30  )
    plt.plot(N_range[5:],logZs[5:], marker = 'o', markersize = 8, linewidth = 3, color = 'k')
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.show()


    print(scale_factors)





def read_BOTH(path2files, base_dir_name_chunks, Nscafac, Nbeta):
    

    def base_dir_name(base_dir_name_chunks, a,b):
        return base_dir_name_chunks[0] + str(a) + base_dir_name_chunks[1] + str(b)
    
    
    
    
    #how many directories do we need to run the loop for?
    N_range_betas = np.arange(Nbeta) + 1
    N_range_scafacs = np.arange(Nscafac) + 1
    
    #initialize arrays to store the relevant information
    logZs = np.zeros((Nbeta, Nscafac))
    scale_factors = []
    betas  = []
    
   
    #these loops only open files
    for ctr_b, beta_dir in enumerate(N_range_betas):
        for ctr_a, scafac_dir in enumerate(N_range_scafacs):
        
            f = open(os.path.join(path2files,base_dir_name(base_dir_name_chunks, scafac_dir, beta_dir) , 'test.stats'), 'r')
            lines = f.read()
            
            #not anymore!
            #where = base_dir_name[ctr].find('Nscafac_')
            #N_reg_scafac = base_dir_name[ctr][(where + len('Nscafac_') ) : (where + len('Nscafac_') + 1)   ]
            
            
            #load log(Z) for this file
            r = lines.find('log(Z)       =')
            #print(lines[r+15:r + 39])
            logZs[ctr_b][ctr_a]  = float(lines[r+15:r + 40])
            
            scafacs = []
            sis = []

            print('-----------------------------Read in Betas and Scafacs -------------------------------------------------')
            for ctr_j , beta in enumerate(np.arange(beta_dir) + 1):
                #which dim in test.stats are we reading?
                digit = str(beta)
                r = lines.find(digit + '  0.')
                #print('file ', os.path.join(path2files,base_dir_name[ctr]),  'dim ' , float(lines[r + 3:r + 26]))
                sis.append(float(lines[r+ 3:r + 26]))
            betas.append(sis)
            
            #Read in scale factors, if any
            for ctr_i , scafac in enumerate(np.arange(int(scafac_dir) ) + beta_dir + 1):
                #which dim in test.stats are we reading?
                digit = str(scafac)
                r = lines.find(digit + '  0.')
                scafacs.append(float(lines[r+ 3:r + 26]))
            scale_factors.append(scafacs)
        
            f.close()
    
    
    betas = np.array(betas)
    scale_factors = np.array(scale_factors)
    print(N_range_betas.shape,logZs[:,0].shape )
    
    plt.figure(figsize = (10,10))
    plt.ylabel(r'log(Z)', fontsize = 24)
    plt.xlabel(r'N$_\beta$', fontsize = 24)
    plt.title(r'N$_a$ = ' + str(N_range_scafacs[0]) , fontsize = 30  )
    plt.plot(N_range_betas[5:], logZs[5:,0], marker = 'o', markersize = 8, linewidth = 3, color = 'k')
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.show()
    
    
    print(scale_factors)




class read_in:
    
    
    def __init__(self, path2files, base_dir_name_chunks, Nscafac, Nbeta, **kwargs):
        
        self.include_zero_scafac = kwargs.pop('include_zero_scafac', False)
        self.path2files = path2files
        self.base_dir_name_chunks = base_dir_name_chunks
        #how many directories do we need to run the loop for?
        self.N_range_betas = np.arange(Nbeta) + 1
        if self.include_zero_scafac:
            Nscafac += 1
            self.N_range_scafacs = np.arange(Nscafac)
        else:
            self.N_range_scafacs = np.arange(Nscafac) + 1
        #initialize arrays to store the relevant information
        self.logZs = np.zeros((Nbeta, Nscafac))
        self.pass_fail = np.zeros_like(self.logZs)
        self.images = np.zeros(( Nbeta, Nscafac, 900, 840, 3 ))
        
    
        def base_dir_name(base_dir_name_chunks, a,b):
            return base_dir_name_chunks[0] + str(a) + base_dir_name_chunks[1] + str(b)
    
        self.scale_factors = []
        self.betas  = []
        
        
        #these loops only open files
        for ctr_b, beta_dir in enumerate(self.N_range_betas):
            for ctr_a, scafac_dir in enumerate(self.N_range_scafacs):
                
                #try:
                img_path = os.path.join(path2files, base_dir_name(self.base_dir_name_chunks, scafac_dir, beta_dir) , 'analysis/total_comparison.pdf')
                save_path = os.path.join(path2files, base_dir_name(self.base_dir_name_chunks, scafac_dir, beta_dir))
                img = convert_from_path(img_path, output_folder = save_path ,output_file= 'beta' + str(beta_dir) + 'scafac' + str(scafac_dir))
                
                img_array = np.asarray(Image.open(save_path + '/beta' + str(beta_dir) + 'scafac' + str(scafac_dir) +'0001-1.ppm' ))[0:-60,50:-390]
                self.images[ctr_b][ctr_a] = img_array
                print(img_array.shape)

                
                f = open(os.path.join(path2files, base_dir_name(self.base_dir_name_chunks, scafac_dir, beta_dir) , 'test.stats'), 'r')
                lines = f.read()
                
                #load log(Z) for this file
                r = lines.find('log(Z)       =')
                #print(lines[r+15:r + 39])
                self.logZs[ctr_b][ctr_a]  = float(lines[r+15:r + 40])
                
                scafacs = []
                sis = []
                
                #print('-----------------------------Read in Betas and Scafacs -------------------------------------------------')
                for ctr_j , beta in enumerate(np.arange(beta_dir) + 1):
                    #which dim in test.stats are we reading?
                    digit = str(beta)
                    r = lines.find(digit + '  0.')
                    #print('file ', os.path.join(path2files,base_dir_name[ctr]),  'dim ' , float(lines[r + 3:r + 26]))
                    sis.append(float(lines[r+ 3:r + 26]))
                self.betas.append(sis)
                
                #Read in scale factors, if any
                '''
                #note to future self: you can add whatever you want to the np.arange() function, but if there is a 0 inside those brackets, it will be
                #an empty list and nothing will end up adding to it.
                '''
                for ctr_i , scafac in enumerate(np.arange(int(scafac_dir) ) + beta_dir + 1):
                    #which dim in test.stats are we reading?
                    digit = str(scafac)
                    r = lines.find(digit + '  0.')
                    scafacs.append(float(lines[r+ 3:r + 26]))
                self.scale_factors.append(scafacs)
                
                #Read in the amplitude of the 21cm model
                if scafac_dir == 0:
                    scafac = 0
                digit = str(scafac + 3)
                r = lines.find(digit + '  0.')
                amplitude_21 = float(lines[r+ 3:r + 26])
                amplitude_error = float(lines[r+ 30:r + 55])
                
                digit = str(scafac + 2)
                r = lines.find(digit + '  0.')
                delta_nu = float(lines[r+ 3:r + 26])
                
                #check whether pass or fail
                if (np.abs(amplitude_21) - np.abs(amplitude_error) > 0.015):
                    self.pass_fail[ctr_b][ctr_a] = False
                else:
                    self.pass_fail[ctr_b][ctr_a] = True
                
                print('scafac_dir beta_dir ', scafac_dir, beta_dir, amplitude_21,amplitude_error , delta_nu, bool(self.pass_fail[ctr_b][ctr_a]))
                
        
                f.close()


        self.betas = np.array(self.betas)
        self.scale_factors = np.array(self.scale_factors)

        
        
        
    def plot_along_one_direction(self,  **kwargs):
        plt.figure(figsize = (10,10))
        plt.ylabel(r'log(Z)', fontsize = 24)
        
        N_start = int(kwargs.pop('N_start', 5))
        if 'beta' in kwargs:
            beta = kwargs.get('beta')
            #we are looking at fixed scafac and varying beta
            idx = np.where(self.N_range_betas == beta)[0]
      
            plt.xlabel(r'N$_a$', fontsize = 24)
            plt.title(r'N$_\beta$ = ' + str(self.N_range_betas[idx]) , fontsize = 30  )
            plt.plot(self.N_range_scafacs[N_start:], self.logZs[idx,N_start:], marker = 'o', markersize = 8, linewidth = 3, color = 'k')
        
        if 'scafac' in kwargs:
            scafac = kwargs.get('scafac')
            idx = np.where(self.N_range_scafacs == scafac)[0]
            plt.xlabel(r'N$_\beta$', fontsize = 24)
            plt.title(r'N$_a$ = ' + str(self.N_range_scafacs[idx]) , fontsize = 30  )
            plt.plot(self.N_range_betas[N_start:], self.logZs[N_start:,idx], marker = 'o', markersize = 8, linewidth = 3, color = 'k')
    
        plt.xticks(fontsize = 20)
        plt.yticks(fontsize = 20)
        plt.show()


    def plot_grid(self, **kwargs):
        
        saturation_lower_limit = kwargs.pop('saturation_lower_limit', 150)
        saturation_upper_limit = kwargs.pop('saturation_upper_limit', None)
        clr_scheme = kwargs.pop('color_scheme' , 'Blues')
        
        print(self.include_zero_scafac)
        plt.figure(figsize = (16,16))
        ax = plt.gca()
        im = ax.imshow(self.logZs, vmin = saturation_lower_limit, vmax = saturation_upper_limit,  origin = 'lower', cmap = clr_scheme, extent = [1- np.array(self.include_zero_scafac).astype(int) , self.logZs.shape[1]   , 1, self.logZs.shape[0]    ]   )
        plt.title('Log(Z)', fontsize = 32)
        plt.xlabel(r'N$_A$', fontsize = 36)
        plt.xticks(fontsize = 20)
        plt.yticks(fontsize = 20)
        #plt.xticks(np.linspace(0,1024,1024)[0::128], np.round(np.linspace(100,200,1024),0)[0::128])
        #plt.xticks(np.linspace(0,1024,1024)[0::128], np.round(np.linspace(100,200,1024),0)[0::128])
        
        #plt.yticks(tickloc, tols)
        plt.ylabel(r'N$_\beta$', fontsize = 36)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        cax.set_ylabel('Log(Z)', fontsize = 30)
        plt.savefig(self.path2files + 'SpectralComplexityLogZGrid.png', dpi = 300)
        plt.show()
        plt.close()
    
    
    def pass_fail_grid(self, **kwargs):
        clr_scheme = kwargs.pop('color_scheme' , 'Blues')
        
        plt.figure(figsize = (16,16))
        ax = plt.gca()
        im = ax.imshow(self.pass_fail,   origin = 'lower', cmap = clr_scheme, extent = [1- np.array(self.include_zero_scafac).astype(int) , self.logZs.shape[1]   , 1, self.logZs.shape[0]    ]   )
        plt.title('Null Test Result', fontsize = 32)
        plt.xlabel(r'N$_A$', fontsize = 36)
        plt.xticks(fontsize = 20)
        plt.yticks(fontsize = 20)
        #plt.xticks(np.linspace(0,1024,1024)[0::128], np.round(np.linspace(100,200,1024),0)[0::128])
        #plt.xticks(np.linspace(0,1024,1024)[0::128], np.round(np.linspace(100,200,1024),0)[0::128])
        
        #plt.yticks(tickloc, tols)
        plt.ylabel(r'N$_\beta$', fontsize = 36)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        cax.set_ylabel('Pass/Fail', fontsize = 30)
        plt.savefig(self.path2files + 'SpectralComplexityPassFailGrid.png', dpi = 300)
        plt.show()
        plt.close()
    
    def image_grid(self, **kwargs):
     
        
        f, axarr = plt.subplots(self.images.shape[0], self.images.shape[1],figsize=(35, 35), sharex = True, sharey = True)
        f.subplots_adjust(hspace=0.05)
        
        
        for i in range(self.images.shape[0]):
            for j in range(self.images.shape[1]):
                ctr_i = self.images.shape[0] - i -1
                ctr_j =  j #self.images.shape[1] - j -1
                im = axarr[i,j].imshow(self.images[ctr_i][ctr_j].astype('uint8'),  extent = [1- np.array(self.include_zero_scafac).astype(int) , self.logZs.shape[1]   , 1, self.logZs.shape[0]    ]   )
    
    
    #plt.title('Result', fontsize = 32)
    #   plt.xlabel(r'N$_A$', fontsize = 36)
        #plt.xticks(fontsize = 20)
        #plt.yticks(fontsize = 20)

        
        #plt.yticks(tickloc, tols)
        '''
        plt.set_ylabel(r'N$_\beta$', fontsize = 36)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        cax.set_ylabel('Pass/Fail', fontsize = 30)
        '''
        plt.savefig(self.path2files + 'SpectralComplexityImageGrid.png', dpi = 300)
        plt.show()
        plt.close()
    
    
    
    
    @staticmethod
    def info():
        print('Chunk file names are the directory name split into two (N_reg and N_scafac). For example, the directory 150MHzAbsErrsRayleighJeansDrawPspecFractionalErrsScaled_fitwAllSky150_Nscafac_10_60MinObs_SpectralComplexity_N10 would be split into : ' ,  '150MHzAbsErrsRayleighJeansDrawPspecFractionalErrsScaled_fitwAllSky150_Nscafac_'
              , '_2 = _60MinObs_SpectralComplexity_N', flush = True)


        
        





    
    


