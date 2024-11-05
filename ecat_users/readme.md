# Contains basic Python example to interact with eCat(GeoNetwork) APIs.  

## ecat_users_group.py:  
The script ecat_users_groups.py can be used to retrieve all user groups.  
 
It expects the following input values which can be supplied as environment variables. If set within the script, then don't need to supply anything:  
- `ENV`: Mandatory, to set the correct base url `dev` or `test` or `prod`.  
- `ECAT_USERNAME`: Mandatory, eCat user with priviledges to create record.  
- `ECAT_PASSWORD`: Mandatory, password for the user mentioned above.  


## Note  
This is purpose built side project; only maintained as required. 

## References  
[https://docs.geonetwork-opensource.org/4.2/api/the-geonetwork-api/](https://docs.geonetwork-opensource.org/4.2/api/the-geonetwork-api/)  