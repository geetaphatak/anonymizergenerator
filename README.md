# Anonymizer

### Demographics Data Generation API

http://{ip}:{port}/get_data

| Parameter name  | Description  | 
| ------ | ------------ |
|n|number of rows|
|m|male percentage|
|exclude_loc|comma seperated strigng of US zip code, US cities and US states|

Example: 

http://40.112.222.75:8080/get_data?n=1&m=0.3&exclude_loc=los%20angeles,%20san%20francisco

```json
{"data":["922254|Mary Z Meyer|Mary|Z|Meyer|Dr.|Single|Cell Phone|Alaska|georgemarilyn@hotmail.com|F|33269 Monroe Shores|Dominguezhaven|KY|93302|USA|N3856059|1982-05-06|N||710-141-8432|365-276-9662|757-260-9867|602-60-6783"],"delimiter":"|","exclusion":"los angeles, san francisco","female_n":1,"male_n":0}

```

### Indian Demographics Data Generation API

http://{ip}:{port}/get_indian_data

| Parameter name  | Description  | 
| ------ | ------------ |
|n|number of rows|
|m|male percentage|
|exclude_loc|comma seperated strigng of US zip code, US cities and US states|

Example: 

http://40.112.222.75:8080/get_indian_data?n=1&m=0.3&exclude_loc=los%20angeles,%20san%20francisco

```json
{"data":["505086|Indira M Gandhi|Indira|M|Gandhi|Dr.|Married|Cell Phone|Native|christine38@hotmail.com|F|326 Terry Roads|Lake Victoria|WV|29839|USA|J9312776|1980-04-17|N||771-222-9161|459-031-5264|241-322-9419|780-10-1466"],"delimiter":"|","exclusion":"los angeles, san francisco","female_n":1,"male_n":0}
```
### Libraries

The primary library used for generating user profiles is Faker (https://github.com/joke2k/faker). This a Python package to bootstrap your database or anonymize data taken from a production service. In addition, multiple language support for extending the apis is also available.

The RESTful API is created using Flask. Flask applications are known for being lightweight, mainly when compared to their Django counterparts. Flask developers call it a microframework, where micro means that the goal is to keep the core simple but extensible. 

Data encryption can be performed using the steps outlined [here](https://github.com/Marlabs1/Analytics-Mithun/blob/master/flask_encryption.md)

### Header

Data is generated for the below header:

| Field  | Description  | 
| ------ | ------------ |
|id|unique id|
|name|full name containg first name, middle initial and last name|
|first_name|first name linked to name field|
|middle_name|middle name linked to name field|
|last_name|last name linked to name field|
|suffix|suffix differentiated for gender - Mr., Mrs., Dr., Miss, etc.|
|martial_status|'Married', 'Single', 'Divorced', 'Widowed'|
|preferred_communication|
|ethnicity|This field indicates how the user wants to be communicated - cell phone, land line, email, mail|
|email|a masked email|
|sex|gender corresponding to name|
|address_line1|street address field|
|city|US city|
|state|US state|
|zip|US zip|
|country|US country|
|driverlicense|US driver's license|
|dob|date of birth|
|deceased_flag|indicates if user is alive|
|death_date|date of death if deceased flag is true|
|phone_cell|primary mobile no (US)|
|phone_fax|fax number if available (US)|
|phone_home|land line no (US)|
|ssn|social security #|
