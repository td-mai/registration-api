Welcome to registrationapi's documentation!
===========================================

.. _registerapi:

Register
---------
    **POST /api/register**
        **Request type**
            * `POST`
        **Headers**
            * Content-Type: `application/json`
        **Data**
            * `email`
            * `password`

        **Response**
            * `200`: OK
            * `409`: Conflict
                |   {
                |   "message": "This email is already used.",
                |   "status_code": 409
                |   } 
            * `422`: Unprocessable Entity
                |   {
                |   "message": "The email is not valid",
                |   "status_code": 422
                |   },
                |   {
                |   "message": "The password is not valid.
                        A valid password must be at least six characters long and contain at least one uppercase,
                        one lowercase character, one number and one special character.",
                |   "status_code": 422
                |    }

    **Example:**

    .. code-block::
    
        $ curl -d '{"email":"user01@gmail.com", "password":"myPass*1"}' -H "Content-Type: application/json" -X POST http://172.17.0.5:5000/api/register


.. _activateapi:

Activate
--------

    **POST /api/activate**
        **Request type**
            * `POST`
        **Headers**
            * Content-Type: `application/json`
            * Authorization: A basic authentication string made by `email` and `password` registered in the first step :ref:`registerapi`.
        **Data**
            * `code`: A 4 digits code received by email after the first step :ref:`registerapi`. 

        **Response**
            * `201`: Created
               "User activated"

            * `409`: Conflict
                "This account is already activated."

            * `400`: Bad Request
                "Activation code is required."

            * `401`: Unauthorized
                | "The account does not exist or already expired. Please register again.",
                | "Authorization header is required.",
                | "Wrong authorization header."

    **Basic Authentication**

    The basic authentication string is made by the word `Basic`
    followed by a space and a base64-encoded string `{email}:{password}`.

    Code to genarate the basic authentication string :

    * Python

    .. code-block::

        import base64
        email = "user01@gmail.com"
        password = "myPass*1"
        basic_auth_str = 'Basic ' + base64.b64encode((email + ':'+password).encode()).decode()
        print(basic_auth_str)


    * Bash

    .. code-block::

        $ echo Basic $(echo -n user01@gmail.com:myPass*1 | base64)


    **Example:**

    .. code-block::

        $ curl -d '{"code": 1783}' -H "Content-Type: application/json" -H "Authorization: Basic $(echo -n user01@gmail.com:myPass*1 | base64)" -X POST http://172.17.0.5:5000/api/activate


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================
* :ref:`search`
