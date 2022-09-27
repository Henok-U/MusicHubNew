# Profile
User can manage their profile, for example 
add profile avatar, edit personal information, change password etc.

In order to interact with any of profile actions, user must be logged in,
otherwise an appropiate HTTP `401 Unauthorized` response will be returned.

## View/Edit profile information
Following request will retrive information about user:

**Request**:

`GET` `/api/user/profile/`

Headers:

```
Authorization: Token 3729f87c3d274c994264127967c3a0d6c34fe4da
```

**Response**:
```json
{ 
    "email" : "example@mail.com",
    "first_name": "Joe",
    "last_name": "Doe" 
}
```

To edit first name or last name:

**Request**:

`PATH` `/api/user/profile/`

Headers:

```
Authorization: Token 3729f87c3d274c994264127967c3a0d6c34fe4da
```

Parameters:

Name | Type | Description
---|---|---
first_name | string | first name to be changed
last_name | string | last name to be changed

**Response**:
```json
{ 
    "Message" : "Profile Updated successfully" 
}
```
If user will provide invalid data,
HTTP `400 Bad request` response with appropiate error message will be returned.

## Add/Update profile avatar
User can upload a profile avatar picture, which can be one of the
*.jpg, .jpeg, .png* extension. 
The file cannot be bigger than 3Mb and must be a valid picture.

**Request**:

`PATH` `/api/user/upload-photo/`

Headers:

```
Authorization: Token 3729f87c3d274c994264127967c3a0d6c34fe4da
```

Parameters:

Name | Type | Description
---|---|---
picture | file | uploaded picture


**Response**:
```json
{ 
    "data" : "Picture added successfully" 
}
```
If user will provide invalid data,
HTTP `400 Bad request` response with appropiate error message will be returned.


## Change password
User can also change their password:

**Request**:

`PATH` `/api/user/change-password/`

Headers:

```
Authorization: Token 3729f87c3d274c994264127967c3a0d6c34fe4da
```

Parameters:

Name | Type | Description | Validation
---|---|---|---
old_password | string | old password | must be a valid previous password
password | string | The user's password | cannot be the same as old password
confrim_password | string | The user's password confrimation | must be the same as password


**Response**:
```json
{ 
    "data" : "Password changed successfully" 
}
```
If user will provide invalid data,
HTTP `400 Bad request` response with appropiate error message will be returned.