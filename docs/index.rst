.. NGaDNAP documentation master file, created by
   sphinx-quickstart on Thu Jan 14 13:20:51 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

NGaDNAP: Next-generation ancient DNA pipeline.
==============================================

:Author: James Boocock (`github <github.com/smilefreak>`_) and Joseph Saunderson (`github <github.com/jsaunderson>`_)
:contact: james.boocock@otago.ac.nz 
:License: `MIT <https://opensource.org/licenses/MIT>`_
:Source code: `Github <https://github.com/smilefreak/NGaDNAP>`_

NGaDNAP is a bioinformatics pipeline that was designed to process and analyse NGS generated for the study of ancient DNA data.
Using a number of publicly avaliable tools the pipeline processes raw FASTQ files through all the important steps of a NGS analysis. In addition, the pipeline augments the standard NGS pipeline with a number of extra processing steps specific for ancient DNA analysis, such as checking for contamination, adjusting base qualities by damage probabilities, and lowering the base quality of the sites at the beginning and end of the reads (these are most likely to be damaged). While a number of other pipelines exist for this purpose, such as PALEOMIX, NGaDNAPs true defining feature is the web-interface to the pipeline. This provides not only an interface to process and manage the runs of the pipeline, but also some visualisation and analysis of the results.

Contents:

.. toctree::
   :maxdepth: 2
   
   installing
   tutorial
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

