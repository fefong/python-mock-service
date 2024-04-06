# Mock Service

## Project Description

The Mock Service is a versatile and efficient tool designed for creating mock endpoints with a wide range of functionalities. It offers a completely generic approach, eliminating the need for code modifications. All the features can be easily managed through a user-friendly API, providing full control over the Mocks.

**Objective:** Study

**Version:** 0.0.1-ALPHA

## Settings

- [x] Python 3.11.2

## How to Run

Create virtualenv (venv)
```sh
virtualenv venv
```

Activate virtualenv (venv)
```sh
source venv/bin/activate
```

Install Python Packages
```sh
pip install -r requirements.txt
```

Run the *app*
```sh
python app.py
```

## Features

⚠️ *Unmarked items are under development.* ⚠️ 

- [ ] CRUD Mock endpoint
  - [x] **Create** mock endpoint
    - [x] *'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'*
  - [x] **Read** mock endpoint
    - [x] List all endpoints
      - [ ] DTO
    - [x] List endpoint details
  - [ ] **Update** mock endpoint
    - [x] Full update mock endpoint *(method: update)*
    - [ ] Partial update mock endpoint *(method: patch)*
  - [ ] **Delete** mock endpoint
    - [ ] Soft delete
    - [x] Hard delete
- [ ] CRUD Flow Mock endpoint
- [x] Header validation
  - [x] Key validation
  - [x] Value validation
- [x] Body validation
  - [x] Key validation
  - [x] Value validation
- [x] Body schema validation
- [x] Async in mocks
- [x] Delay in response
- [ ] Special tags
  - [x] Endpoint list Special tags
  - [ ] Basic Functions with Special tags

## Tests

- [ ] Tests
  - [ ] Unitary tests
  - [ ] Integration tests
  - [ ] e2e


## Docs

- [x] README
- [ ] Architecture
- [ ] Postman collection

## Container

- [ ] Docker
- [ ] Docker Compose
  - [ ] Python Mock Service (app) 
  - [ ] Mongodb

## Database

- [ ] Database
  - [x] Local
  - [x] Repository [wip]
  - [ ] Mongodb

