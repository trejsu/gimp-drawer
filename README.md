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
| i    | n/a     | path to the input file                                                                                                                                                               |
| d    | 0       | number representing "good enough" similarity between images where ```0``` means that every pixel is exactly the same. Thus, the bigger distance, the less similarity between images. |
| v    | off     | verbose output                                                                                                                                                                       |
| r    | 0       | render mode (0 - only "accepted" actions, 1 - no rendering, 2 - every action)                                                                                                                                                                      |
    
## Known bugs

*   Passing ```jpg``` file as argument to ```-f``` option of ```run.py``` displays following message in console at runtime:
    ```
    While parsing XMP metadata:
    Error on line 13 char 1: End of element <xmpMM:DerivedFrom> not expected in this context
    ```
    No impact to script functionality detected. Error comes from ```gimp_file_load()``` function from ```GIMP Library```