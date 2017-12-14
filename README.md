# Gimp Drawer

## Getting Started

### Setup

* Set environment variables 
    * ```GIMP_PLUGIN``` to the path of your gimp plugins directory
        * Local - usually `````$HOME/.gimp-{version}/plug-ins`````
        * Global - usually `````/usr/lib/gimp/{version}/plug-ins`````
    * ```GIMP_PROJECT``` to the path of cloned project
    *  Add ```$GIMP_PROJECT/``` to ```PYTHONPATH```
 
* ```./setup.sh```

### Build

```
./build.sh
```

### Run 

```
python run.py -i <file_name> -d <acceptable_distance>
```
| Flag | Default | Description                                                                                                                                                                          |
|------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| s    | n/a     | Path to the source file                                                                                                                                                              |
| d    | 0       | Number representing "good enough" similarity between images where ```0``` means that every pixel is exactly the same. Thus, the bigger distance, the less similarity between images. |
| v    | off     | Verbose output                                                                                                                                                                       |
| r    | 0       | Render mode (0 - only "accepted" actions, 1 - no rendering, 2 - every action)                                                                                                        |                                                             |
| i    | n/a     | Path to the input file from which scripts starts drawing. When missing, starting point is white, empty image.                                                                                                     |                                                             |
    
## Known bugs/issues

*   Passing ```jpg``` file as argument to ```-s``` option of ```run.py``` displays following message in console at runtime:
    ```
    While parsing XMP metadata:
    Error on line 13 char 1: End of element <xmpMM:DerivedFrom> not expected in this context
    ```
    No impact to script functionality detected. Error comes from ```gimp_file_load()``` function from ```GIMP Library```