# Contains basic Python example to interact with eCat(GeoNetwork) APIs.  

## create_record.py:  
The script create_record.py can be used create ecat record.  
The xml file used in this script is from ecat [codebase](https://github.com/ga-gn/core-geonetwork/blob/test/schemas/iso19115-3.2018/src/main/plugin/iso19115-3.2018/templates/ga-19115-3-dataset.xml)  
It expects the following input values, can be supplied as environment variables. If set within the script, then don't need to supply anything:  
- `ENV`: Mandatory, to set the correct base url `dev` or `test` or `prod`.  
- `ECAT_USERNAME`: Mandatory, eCat user with priviledges to create record.  
- `ECAT_PASSWORD`: Mandatory, password for the user mentioned above.  


## Note  
This is purpose built side project; only maintained as required.