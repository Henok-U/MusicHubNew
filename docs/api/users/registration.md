# Sign up
Unregistred user can sign up with the following request:

If user will provide invalid data, HTTP `400 Bad request` response with appropiate error message will be returned.

**Request**:

`POST` `/api/user/signup/`

Parameters:

Name | Type | Description | Validation
---|---|---|---
email | string | The user's email |  must be a valid email
password | string | The user's password | must be beetween 8-64 characters, allowed symbols (Upper/lower case letters, symbols and numbers)
confrim_password | string | The user's password confrimation | must be the same as password
first_name | string | The user's first name | max length=30, allowed symbols (Upper/lower case letters, space, “-“ symbol)
last_name | string | The user's last name | max length=30, allowed symbols (Upper/lower case letters, space, “-“ symbol)

**Success Response**:

`status 200`

```json
{ 
    "id" : "6fc71089-0047-4250-8b95-61a87a432484",
    "email": "example@mail.com",
    "fist_name": "Joe",
    "last_name": "Doe 
}
```


## Sign up verification
After signing up, an verification link is send to the given email address. 
The link contains a token which is valid for 24 hours and can be used only once.
If token date is expired, then user can sign up again to obtain a new verification link.
An example link should look like this:

*http://{host}/api/user/signup/verify/?code=3729f87c3d274c994264127967c3a0d6c34fe4da*

In order to verify user and finish registration process, user must follow link from email,
which should result in following response:


**Response**:

`status 200`

```json
{ 
    "data" : "Email address verified."
}
```
In case of any error a appropiate error message will be returned in `400 Bad request` response.


## Sign up with Google
Alternatively user can registter with google account information,
in this case information will be mapped accordingly:

MusicHub field | Google account field
---|---
email | id 
first_name | given_name 
last_name | family_name 

After signing up user will be created and authorization token will be returned.

**Request**:

`POST` `/api/user/signin-social/google-oauth2/`

Parameters:

Name | Type | Description
---|---|---
access_token | string | Google authorization token

**Response**:
```json
{ 
    "token" : "3729f87c3d274c994264127967c3a0d6c34fe4da" 
}
```

If user will provide invalid data, HTTP `400 Bad request` response with appropiate error message will be returned.

More on google sign in funcionality:

[google oauth2](https://developers.google.com/identity/protocols/oauth2)
