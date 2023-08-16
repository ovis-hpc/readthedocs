#/usr/bin/python3
#requires pandoc v3 for man input format
#point X_ROOT to the build directory

import os
import glob

OVIS_ROOT='/opt/ovis/build/ovis'
for d in ['man','src/contrib/sampler/*','src/contrib/store/*','src/ldmsd/test/','src/sampler/*','src/store/*']:
    files = glob.glob(f'{OVIS_ROOT}/ldms/{d}/*man')
    for i in files:
        fname = i.split('/')[-1].replace('.man','.rst')
        os.system('mkdir -p man2rst/ldms')
        os.system(f'/usr/local/bin/pandoc -f man -s -t rst --toc {i} -o man2rst/ldms/{fname}')
        plugin = fname.replace('.rst','')
        os.system('sed -i -e "0,/man/{s/man/'+plugin+'/}" man2rst/ldms/'+fname) 


SOS_ROOT='/opt/ovis/build/sos'
for d in ['rpc','sos/python']:
    files = glob.glob(f'{SOS_ROOT}/{d}/*man')
    for i in files:
        fname = i.split('/')[-1].replace('.man','.rst')
        os.system('mkdir -p man2rst/sos')
        os.system(f'/usr/local/bin/pandoc -f man -s -t rst --toc {i} -o man2rst/sos/{fname}')
        plugin = fname.replace('.rst','')
        os.system('sed -i -e "0,/man/{s/man/'+plugin+'/}" man2rst/sos/'+fname) 

#MAP RST TO HIERARCHY CODE HERE
