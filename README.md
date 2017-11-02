# Gimp Drawer

TODO

## Getting Started

### Setup

* Set environment variables 
    * ```GIMP_PLUGIN``` to the path of your gimp plugins directory
        * Local - usually `````$HOME/.gimp-{version}/plug-ins`````
        * Global - usually `````/usr/lib/gimp/{version}/plug-ins`````
    * ```GIMP_PROJECT``` to the path of cloned project
 
* ```./setup.sh```

### Build

```
./build.sh
```

### Run

```
python run.py -f <file_name> -i <number_of_iterations> -m <metric>
```
* ```file_name``` - path to the input file. Necessary parameter.
* ```number_of_iterations``` - number of improvement actions which will be performed by the script. Necessary parameter. 
* ```metric``` - metric used to comparing similarity between images. Necessary parameter. Possible values are:
    * ```L1```
    * ```L2```
    
## Known bugs

* Passing ```jpg``` file as argument to ```-f``` option of ```run.py``` displays following message in console at runtime:
```
While parsing XMP metadata:
Error on line 13 char 1: End of element <xmpMM:DerivedFrom> not expected in this context
```
No impact to script functionality detected. Error comes from ```gimp_file_load()``` function from ```GIMP Library```