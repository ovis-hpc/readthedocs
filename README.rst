OVIS-HPC Documentation
########################

This repository hosts all Ovis/LDMS related documentation such as how-to tutorials, getting started with LDMS, docker-hub links, LDMS API and much more. Documentation webpage can be found here: `ovis-hpc/readthedocs <https://ovis-hpc.readthedocs.io/en/latest/>`_

Contributing to ReadTheDocs
############################
Instructions and documentation on how to use ReadTheDocs can be found here:
`readthedocs Help Guide <https://sublime-and-sphinx-guide.readthedocs.io/en/latest/images.html>`_


* Clone the repository:

.. code-block:: RST

  > git clone git@github.com:<current-repo>/ovis-docs.git

* Add any existing file name(s) you will be editing to paper.lock

.. code-block:: RST

  > vi paper.lock
  <add Name | Date | File(s)>
  <username> | mm/dd | <filename>

* Make necessary changes, update paper.lock file and push to repo.

.. code-block:: RST

  > vi paper.lock
  <add Name | Date | File(s)>
  ## remove line
  > git add <files>
  > git commit -m "add message"
  > git push
  
Adding A New File 
******************
For any new RST files created, please include them in docs/src/index.rst under their corresponding sections. All RST files not included in index.rst will not populate on the offical webpage (e.g. readthedocs).

Documentation Generation For Man Pages
*****************************************
Rst files for man pages are generated using the pandoc_man_2_rst.py python file. It requires python3 and pandoc installations. It points at an installation (defined by OVIS_ROOT variable in the file, currently at /opt/ovis/build/ovis) and grabs .man files. There are source/dest arrays that define where to pull data from in OVIS_ROOT and where to put it in the readthedocs dir. 
Pandoc single file usage:


.. code-block:: RST

    /usr/local/bin/pandoc -f man -s -t rst --toc {input.man} -o {output.rst}

IF YOU WANT TO CHANGE THE CONTENTS OF A GENERATED RST FILE, CHANGE THE MAN PAGE INSTEAD AND THEN REGENERATE. 

Paper Lock
************
This is for claiming any sections you are working on so there is no overlap.
Please USE paper.lock to indicate if you are editing an existing RST file.  


