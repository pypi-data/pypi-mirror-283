'''
Default names and values for files and directories used throughout this package.
If you prefer a different default, change it here, and it should propagate througout the package.
Some names have wildcards, such as '*', or '!', these represent name bases, generally for finding
any/all such files in a directory via glob.

@author: Andrew Wetzel <arwetzel@gmail.com>
'''

# base directory of a simulation
# setting to '.' assumes that you are running analysis from within a simulation directory
simulation_directory = '.'

# directory of all halo files, typically the first directory within simulation_directory
halo_directory = 'halo/'

# directory of all rockstar files (needs to include root halo_directory if within it)
rockstar_directory = halo_directory + 'rockstar_dm/'

# directory of rockstar raw text files, within rockstar_directory
rockstar_catalog_directory = 'catalog/'

# directory of rockstar processed hdf5 files, within rockstar_directory
rockstar_catalog_hdf5_directory = 'catalog_hdf5/'

# directory of rockstar processed hdf5 files
rockstar_job_directory = 'rockstar_jobs/'
