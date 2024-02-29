base_rest = http://localhost:8000/api/v1/


auth : 
    - {{base_rest}}accounts/login/ : user login account
    {
        "email": "chentochea2002@gmail.com",
        "password":"Chento@123"
    }
    - {{base_rest}}accounts/token/refresh/ : refresh token
    {
        "refresh":"{{refresh}}"
    }
    - {{base_rest}}accounts/register/ : registation account
    {
    "email": "sophearum14@gmail.com",
    "username": "Sophe4rum",
    "password": "Sophearum@123",
    "is_confirmed":"True"
    }
    - {{base_rest}}accounts/logout/ : acount logout
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5ODY3MDczNywiaWF0IjoxNjk4NTg0MzM3LCJqdGkiOiIyNzU4NTM4MDgzODE0OTFhODU2Yzc1NGY2ZmNhZGE4NiIsInV1aWQiOiIxZGUzOWQyMC1mNzA3LTQ3NjktOWEzNi03ZGJiMDcxYjU2ZjAifQ.HfH2lYjBdDFG2i7G2y4a_aq4QydiPTCZlCLcTv8sblY"
    }
    - {{base_rest}}accounts/verify/  : verify by sendding code
    {
    "email":"sophearum14@gmail.com",
    "verification_code":"118092"
    }
    - {{base_rest}}accounts/change-password/ : user change password
    -{{base_rest}}accounts/me/ : get own account 
    - {{base_rest}}accounts/google/ : login by google
    {
     "auth_token":""
    }

flie:
    - {{base_rest}}files/upload/images/ : image uplaoding
    - {{base_rest}}files/file-upload/50/ : uplaod by user id
    - {{base_rest}}files/user/10/?filename=Data&type= : find file by user id and filter by name
    - {{base_rest}}files/user/9/f6405c8f-e60c-41fb-8b46-ac31bab59170/ : delete by id
    - {{base_rest}}files/files-detail-dataset/f6405c8f-e60c-41fb-8b46-ac31bab59170/ : update by uuid
    {
     "file":"23"
    }
    - {{base_rest}}files/details/6f29bd77-25bc-4857-b49c-948487137f3c/?size=0 : view file by name
    - {{base_rest}}share-dataset/ : share dataset to other users
    {
     "file":4,
     "member":9,
     "owner":19
    }
    
cleaning process:
    - {{base_rest}}data-clean/cleansing/9/bae27c02-6666-4d6f-a89f-92bbd2fbcd40/ : find the unnacurate data
    - {{base_rest}}data-clean/processing-cleaning-file/ : step of cleaing data

tutorials: 
    - {{base_rest}}tutorials/ : insert tutorial
    {
    "title":"ji",
    "content":"https://www.youtube.com/watch?v=DnkNfXMmEYM",
    "published_by":1
    }
    - {{base_rest}}tutorials/?p=1&size=1&title=h : find all tutorials
    - {{base_rest}}tutorials/4 : find toturial by id
    - {{base_rest}}tutorials/1/ : update tutorial
    {
    "title":"Hello Chento",
    "content":"h1 hello bye bye",
    "published_by":1,
    "slug":"how to be single"
    }
    - {{base_rest}}tutorials/4 : delete tutorial

request_tutorials:
    - {{base_rest}}request_tutorials/ : user request for tutorial
    {
    "subject":"i love you",
    "message":"<h1>hello everyone</h1>",
    "request_by":1
    }
    - {{base_rest}}request_tutorials/?p=1&size=1  : find user all user request tutorial
    - {{base_rest}}request_tutorials/1 : find user user request tutorial by id
    - {{base_rest}}request_tutorials/1/ : update tutorial 
    {
    "description":"jessica Sun ou kung",
    "request_by":1
    }

contact us:
    - {{base_rest}}contact_us/ : user contact messages
    {
    "title":"i love cambodia",
    "email":"chento@gmail.com",
    "message":"hello cambodia",
    "created_by":1
    }
    - {{base_rest}}contact_us/ : find all users contact
    {
    "count": 1,
    "next": false,
    "previous": false,
    "results": [
        {
            "email": "sophearum14@gmail.com",
            "message": "I have lost my data drung upload the file.",
            "created_at": "2023-11-20T08:38:10.046122+07:00",
            "is_read": false
        }
    ]
    }
    - {{base_rest}}contact_us/1/ : : find all users contact by id
    {
    "email": "sophearum14@gmail.com",
    "message": "I have lost my data drung upload the file.",
    "created_at": "2023-11-20T08:38:10.046122+07:00",
    "is_read": false
    }
    - {{base_rest}}contact_us/1/ : update status in read
    {
    "is_read":true
    }

role:
    {{base_rest}}roles : set user role base

share:
    {{base_rest}}share-dataset/list/ : share dataset by username
    [
    {
        "file": {
            "id": 4,
            "filename": "509af0dd9ffb494f969c943ff9213e31.csv",
            "file": "Car_sales.csv",
            "uuid": "ebfcaecc-d111-47c6-9c45-52e58a52f0db",
            "size": 15700,
            "type": "csv",
            "created_at": "2023-11-20T01:57:26.146381+07:00",
            "is_original": true,
            "is_deleted": true,
            "created_by": 15
        },
        "owner": {
            "username": "Papi",
            "gender": null,
            "dob": null,
            "uuid": "a92d866a-b16c-4044-b643-c89c02f165c0",
            "email": "sophearum142023@gmail.com",
            "phone_number": null,
            "full_name": null,
            "address": null,
            "biography": null,
            "avatar": null,
            "storage_data": 0.0,
            "created_at": "2023-11-20T08:27:57.747356+07:00",
            "auth_provider": "email",
            "is_deleted": false,
            "is_confirmed": true
        },
        "member": {
            "username": "chento",
            "gender": null,
            "dob": null,
            "uuid": "e13b7c4b-ec05-4241-9c8e-20c7c45dd51a",
            "email": "chentochea2002@gmail.com",
            "phone_number": null,
            "full_name": null,
            "address": null,
            "biography": null,
            "avatar": null,
            "storage_data": 0.0,
            "created_at": "2023-11-19T22:24:00.651381+07:00",
            "auth_provider": "email",
            "is_deleted": false,
            "is_confirmed": true
        },
        "uuid": "0a0f92fc-4b2e-4019-9c09-a022e0f3db02",
        "is_deleted": false,
        "shared_at": "2023-11-21T08:16:43.261692+07:00",
        "status": "pending"
    }
    ]

user:
    - {{base_rest}}users/ : get all users in application
    - {{base_rest}}users/1/ : get all users in application by id
    - {{base_rest}}users/ : create user into application 
    {
    "username":"13fefdewfwd23dd32",
    "gender":"Male",
    "email":"chentwrewedwwefdo@gmail.com",
    "password":"C@123",
     "group_ids":["1"]
    }
    - {{base_rest}}users/2/ : delete user by id
    - {{base_rest}}users/31/ : update user
    {
    "phone_number":"099384617",
    "address":"Phnom Penh",
    "biography":"I love Cambodia",
    "avatar":"123.jpg",
    "username":"Jessica dog",
    "gender":"Male"
    }
    - {{base_rest}}users/uuid/3d4a6db6-a2cb-4f8d-9cde-bc16286bf629 : find user by uuid
    - {{base_rest}}users/uuid/3d4a6db6-a2cb-4f8d-9cde-bc16286bf629 : delete user by uuid
    - {{base_rest}}users/uuid/3d4a6db6-a2cb-4f8d-9cde-bc16286bf629/ : update user by uuid
    - {{base_rest}}users/uuid/3d4a6db6-a2cb-4f8d-9cde-bc16286bf629/ : find by email
     - {{base_rest}}users/uuid/3d4a6db6-a2cb-4f8d-9cde-bc16286bf629/ : delete by email




