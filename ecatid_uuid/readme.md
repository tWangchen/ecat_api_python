# Contains basic Python example to interact with eCat(GeoNetwork) APIs.  

## ecat_uuid.py:  
The script ecat_uuid.py can be used to get uuid for ecatid or vice versa.  
It expects the follwoing input values, which can be set as environment variables or set within the script:    
- `ECAT_ADMIN_USERNAME`: Mandatory, eCat user with Admin priviledges to trigger re-index.  
- `ECAT_ADMIN_PASSWORD`: Mandatory, password for the user mentioned above.  
- `ECAT_ENV`: Optional, acceptable values: `dev.ecat, dev2.ecat; test.ecat, test2.ecat; prod2.ecat, ecat`  

Also expects either ecatid or uuid to be supplied either as runtime arguments or set within the script:  
- `ECATID`: ecatid to get uuid for.  
- `UUID`: uuid to get ecatid for. 

See example below to set arguments during runtime:  
`python ecatid_uuid.py --ecatid=107722`  
OR  
`python ecatid_uuid.py --uuid=fb89aea2-6531-4928-b162-506bf0c1d848`  
OR  
`python ecatid_uuid.py --ecatid=107722 --uuid=fb89aea2-6531-4928-b162-506bf0c1d848`  

## Note  
This is purpose built project side project; only maintained as required.