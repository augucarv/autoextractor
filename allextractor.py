def allextractor(exdir,fitsdir,filterlist):
    """ This function automates SExtractor runs for all .fits files in a directory,
    runs source-extractor with two different filters, matches the catalogs and 
    returns a final catalog with matched sources.
    
    NOTE: You have to manually tune parameters in the default.sex file.
    
    Inputs:
        exdir: source-extractor directory;
        fitsdir: Directory containing all the .fits files to be assessed;
        filterlist: list containing the name of the two filters to be used;
    
    Outputs:
        A 'results' directory with:
            - single catalogs for each filter;
            - .reg file for importing in DS9;
            - a final catalog with matches for both filters. 
            
        NOTE: This directory will be inside fitsdir.
    
    Requirements:
        pandas, allmatch, gnome-terminal
        
    Call example:
        allextractor('/usr/source-extractor','/usr/fits',['default.conv','mexhat_5.0_11x11.conv'])
    """
    
    import os
    import glob
    import shutil
    import pandas as pd
    from allmatch import allmatch
    import subprocess
    #################### Source detection/extraction step #########################

    extractor_dir = exdir # Folder with source-extractor main instances
    fits_dir = fitsdir # Folder with all .fits files to have sources extracted from
    filter_list = filterlist  # Selecting which filters will be used
    os.chdir(fits_dir)
    filelist = glob.glob('*.fits') # Fetching all the .fits files from fits_dir
    shutil.rmtree(fits_dir+"results", ignore_errors=True)
    os.mkdir(fits_dir+"results")

    os.chdir(extractor_dir) # Changing current directory to extractor_dir (avoids mistakes)

    read_param = pd.read_csv('default.sex',sep='delimiter', header=None, engine='python')

    for fitsfile in filelist:
        os.mkdir(fits_dir+"results/"+fitsfile[:-5])
        for filter_name in filter_list:
            read_param[0][4] = 'CATALOG_NAME     '+fits_dir+filter_name[:3]+'.cat       # name of the output catalog'
            read_param[0][14] = 'FILTER_NAME      '+filter_name+'   # name of the file containing the filter'
            read_param.to_csv('default.sex', sep='\t', encoding='utf-8',index=False,header=False)
            subprocess.call(["gnome-terminal","--disable-factory","--","source-extractor",fits_dir+fitsfile]) 
        allmatch(fitsfile,filter_list[0][:3]+".cat",filter_list[1][:3]+".cat",3,fits_dir)
        srcdir = fits_dir+"results/"+fitsfile[:-5]
        shutil.move(fits_dir+filter_list[0][:3]+".cat",srcdir)
        shutil.move(fits_dir+filter_list[1][:3]+".cat",srcdir)
        shutil.move(fits_dir+fitsfile[:-5]+".coo",srcdir)
            #    shutil.move(fits_dir+fitsfile[:-5]+".reg",srcdir)
        shutil.move(fits_dir+fitsfile[:-5]+".txt",srcdir)
            
