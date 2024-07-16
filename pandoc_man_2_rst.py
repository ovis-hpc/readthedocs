#/usr/bin/python3
#requires pandoc v3 for man input format
#point X_ROOT to the build directory

#import os
#import glob

#OVIS_ROOT='/opt/ovis/build/ovis'
#source = ['man','src/contrib/sampler/*','src/contrib/store/*','src/ldmsd/test/','src/sampler/*','src/store/*']
#dest = ['ldms/ldms_man','ldms/sampler_man','ldms/store_man','ldms/ldms_man','ldms/sampler_man','ldms/store_man']
#for c,s in enumerate(source):
#    files = glob.glob(f'{OVIS_ROOT}/ldms/{s}/*man')
#    for i in files:
#        fname = i.split('/')[-1].replace('.man','.rst')
#        os.system('mkdir -p man2rst/ldms')
#        os.system(f'/usr/local/bin/pandoc -f man -s -t rst --toc {i} -o man2rst/ldms/{fname}')
#        plugin = fname.replace('.rst','')
#        plugin_title = '='*len(plugin)
#        os.system('sed -i -e "0,/man/{s/man/'+plugin+'/}" man2rst/ldms/'+fname) 
#        os.system('sed -i -e "s/===/'+plugin_title+'/" man2rst/ldms/'+fname) 
#        os.system(f'cp man2rst/ldms/{fname} docs/source/{dest[c]}') 


#SOS_ROOT='/opt/ovis/build/sos'
#source = ['rpc','sos/python']
#dest = ['sos/sos_man','sos/sos_man']
#for c,s in enumerate(source):
#    files = glob.glob(f'{SOS_ROOT}/{s}/*man')
#    for i in files:
#        fname = i.split('/')[-1].replace('.man','.rst')
#        os.system('mkdir -p man2rst/sos')
#        os.system(f'/usr/local/bin/pandoc -f man -s -t rst --toc {i} -o man2rst/sos/{fname}')
#        plugin = fname.replace('.rst','')
#        plugin_title = '='*len(plugin)
#        os.system('sed -i -e "0,/man/{s/man/'+plugin+'/}" man2rst/sos/'+fname) 
#        os.system('sed -i -e "s/===/'+plugin_title+'/" man2rst/sos/'+fname) 
#        os.system(f'cp man2rst/sos/{fname} docs/source/{dest[c]}') 

