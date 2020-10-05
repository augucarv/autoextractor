# autoextractor: automating SExtractor runs

This script is an automated version of [SExtractor](https://www.astromatic.net/software/sextractor). It runs `source-extractor` in all .fits files contained in a certain directory with two different filters (e.g. 'default.conv' and 'gauss_5.0_9x9.conv'), matches the catalogs outputed from both runs and gives a final catalog for further analysis, as well as a .reg file to be used in [DS9](https://sites.google.com/cfa.harvard.edu/saoimageds9).

Important: 

1. This is only tested with Linux distributions, specifically Ubuntu 20.04 LTS;
2. You have to have Sextractor already installed;
3. You have to tune the default.sex file manually to account for different parameters (e.g. DETECT_THRESH etc.);

Enjoy! ;)
