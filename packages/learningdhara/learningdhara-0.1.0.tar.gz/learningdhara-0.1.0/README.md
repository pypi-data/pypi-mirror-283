## learningdhara community (Learning Community towards new era technology learning)
Author - Learningdhara Community (www.learningdhara.com)
Date   - 7th July 2024 
###### Handling of json data
1. select.py

a) select_all() 

- Parameters: 
    - file_path : It expects a relative path of the json data file
    - entity : It expects the name of the entity like customer, department or organization etc.

- Return 
    - It will return a entity json data 

2. insert.py 

a) insert_me(file_path, entity, **data)

- Parameters: 
    - file_path : It expects a relative path of the json data file
    - entity : It expects the name of the entity like customer, department or organization etc.
    - data : It expects the keyword arguments having json data.

- Return 
    - It will return a entity json data


###### Sample json data

{
    "data": [
        {
            "name": "Prashant",
            "age": "50",
            "sex": "Male",
            "organization": "TCS",
            "department": "RnD",
            "isActive": "true"
        },
        {
            "name": "Nishant",
            "age": "50",
            "sex": "Male",
            "organization": "TCS",
            "department": "RnD",
            "isActive": "true"
        },
        {
            "name": "Ranjan",
            "age": "50",
            "sex": "Female",
            "organization": "TCS",
            "department": "RnD",
            "isActive": "true"
        },
        {
            "name": "Appu",
            "age": "27",
            "sex": "Male",
            "organization": "TCS",
            "department": "RnD",
            "isActive": "true"
        }
    ]
}
