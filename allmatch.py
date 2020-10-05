def allmatch(file_name,cat1,cat2,sep,wdir):
    """ This function matches sources of two SExtractor catalogs, cat1 and cat2, 
    obtained with two different filters, and returns a final catalog with the 
    result of the operation cat1+cat2-cat1∩cat2.
    
    All the entry parameters, except sep, must be entered as strings.
    
    Entry parameters:
        
        file_name: name of the .fits file whose catalogs were obtained
        cat1 = first catalog
        cat2 = second catalog
        sep = distance in pixels for the sources to be considered a match
        wdir = working directory (where the .fits file is and where the final 
        catalog will be saved)
                
    Returns:
        
        1. .txt file with all the sources and parameters
        2. .coo file for DAOPHOT preprocessing
        3. .reg file for checking the detection with DS9
    
    Call example:
        
        allmatch('FILE.fits','def.cat','mex.cat',3,'/home/usr/')
            
    """

    from astropy.table import Table, vstack
    from astropy.io import ascii
    import numpy as np
    from scipy.spatial.distance import cdist

    wdir = str(wdir)
    img_name = str(file_name) 
    seo1 = str(cat1)
    seo2 = str(cat2)

    catA = Table.read(wdir+seo1, format='ascii')
    catB = Table.read(wdir+seo2,format='ascii') 

    if len(catA) > len(catB):
        cat_base = catA
        cat = catB
    else:
        cat_base = catB
        cat = catA
        
    A = np.array([cat['X_IMAGE_DBL'],cat['Y_IMAGE_DBL']]).T
    B = np.array([cat_base['X_IMAGE_DBL'],cat_base['Y_IMAGE_DBL']]).T
    
    lim = 1000
    n_batches = round(len(A)/lim)
    dist = []
    idx = []
    idx_matches = []

    for i in range(0,n_batches+1):
        bottom_lim = i*lim
        upper_lim = min(lim+i*lim-1,len(A))
        dist = cdist(A[bottom_lim:upper_lim], B, metric='euclidean')
        idx = np.argmin(dist > sep, axis=1)
        idx2 = idx[idx>0]
        idx_matches = np.append(idx_matches,idx2)
        dist = []
        idx = []

    cat_base.remove_rows(idx_matches.astype(int)) 
    
    final_catalog = vstack([cat_base,cat])
    final_catalog['NUMBER']=np.arange(1,len(final_catalog)+1)

    ascii.write(final_catalog, wdir+'/'+img_name[:-5]+'.txt', overwrite=True)
    ascii.write(final_catalog['NUMBER','X_IMAGE_DBL','Y_IMAGE_DBL'], wdir+'/'+img_name[:-5]+'.coo', overwrite=True)
    ascii.write(final_catalog['X_IMAGE_DBL','Y_IMAGE_DBL'],wdir+'/'+img_name[:-5]+'.reg', format='no_header', overwrite=True)