# Password reset
User can reset their password by providing address email to which reset link will be sent.
The link contains a token which is valid for 24 hours and can be used only once.
If user will provide invalid email address,
HTTP `400 Bad request` response with appropiate error message will be returned.

**Request**:

`POST` `/api/user/reset-password/`

Parameters:

Name | Type | Description
---|---|---
email | string | User's email address

**Response**:
```json
{ 
    "data" : "Reset link was sucessfully send to given address email" 
}
```

After following link from email, user can set up a new password.
Example link should look like this:

*http://{host}/api/user/reset-password/?code=3729f87c3d274c994264127967c3a0d6c34fe4da*

**Request**:

`PATH` `/api/user/reset-password/`

Parameters:

Name | Type | Description
---|---|---
password | string | new password
confrim_password | string | confrim password - must be the same as password

**Response**:
```json
{ 
    "data" : "Password was successfully changed" 
}
```

If user will provide invalid data,
HTTP `400 Bad request` response with appropiate error message will be returned.