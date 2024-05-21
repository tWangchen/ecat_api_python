# Contains basic Python example to interact with eCat(GeoNetwork) APIs.  

## ecat_uuid.py:  
The script ecat_uuid.py can be used to get uuid for ecatid or vice versa.  
It expects the following input values, can be supplied either as runtime arguments or as environment variables. If set within the script, then don't need to supply anything:  
- `env`: to set the correct base url. Defaults to prod, so only need to supply `dev` or `test` as required. 
- `ecatid`: ecatid to get uuid for.  
- `uuid`: uuid to get ecatid for. 

See example below to set arguments during runtime:  
`python ecatid_uuid.py --ecatid=107722 --env=test`  
OR  
`python ecatid_uuid.py --uuid=fb89aea2-6531-4928-b162-506bf0c1d848 --env=test`  
OR  
`python ecatid_uuid.py --ecatid=107722 --uuid=fb89aea2-6531-4928-b162-506bf0c1d848 --env=test`  

## Note  
This is purpose built side project; only maintained as required.