# Gimp Drawer

TODO

## Getting Started

### Setup

* Set environment variable ```GIMP_PLUGIN``` to the path of your gimp plugins directory
    * Local - usually `````$HOME/.gimp-{version}/plug-ins`````
    * Global - usually `````/usr/lib/gimp/{version}/plug-ins`````
* Add execute permission to ```build.sh``` file

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

