# Data Processing for Ventilators
*(c)2021 - AMG -
Reased under MIT License*

Simple python data processor to c
onvert raw data into waveforms
using pandas dataframes and gplot
## Don't hold your breath!
Still not in a deployable status as a package, but all the scripts work as intended.


## usage

Install dependencies using Pipefiles: 
            
        $pipenv install -e .

Convert to excel script:

        $python convert_to_excel <inputpath > <outputhpath>

Plotter script:

        plotter.py

for plotter, you need to modify the suites to match your specific needs (e.g. files and type of plots)