# API-Test-Restful-Booker.Herokuapp
API test of https://restful-booker.herokuapp.com/

Apidoc can be found at https://restful-booker.herokuapp.com/apidoc/index.html

## Introduction

This repository contains sets of API smoke tests realized by OOP method.
Test documentation for manual testing (check-lists, bug-reports) can be found in test_documentation.xlsx file.



The following tests have been implemented:

- Validating status codes of basic CRUD http methods

- Validating of specified json data/schemas validation

- Generating of authentication token

- Getting ids of available bookings upon various filters data provided (specified id, firstname & lastname, checkin & checkout)

- Creating new booking

- Updating specified bookings fully and partially

- Deleting specified booking


## Set-up
1) Clone the repository to your local machine
2) Install all requirements: 
 ```
 pip install -r requirements
 ```
3) Run tests through the terminal
```
pytest -s -v tests_api.py

```
