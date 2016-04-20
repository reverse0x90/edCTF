# edCTF API Documentation

* [ctfs](#ctfs)
 * [ctfs/:id](#ctfs/:id)

## ctfs
----
  Read a list of CTFs or create a CTF

* **URL**

  /api/ctfs/

* **Method:**

  `GET` | `POST`
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  `GET`
  `?online=[boolean]`

  `POST`
  ```
  {
    "ctf": {
      "name": [ctf-name],
      "online": [boolean],
      "ctftime": null,
      "about": null,
      "home": null,
      "challengeboard": null,
      "scoreboard": null
    }
  }
  ```

* **Success Response:**
  
  <_What should the status code be on success and is there any returned data? This is useful when people need to to know what their callbacks should expect!_>

  * **Code:** 200

    **Content:**
    ```
    {
      "ctf": {
        "id": [:id],
        "name": [ctf-name],
        "online": [boolean],
        "challengeboard": [:id],
        "scoreboard": [:id],
        "home": [:id],
        "about": [:id]
      }
    }
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST

    **Content:**
    ```
    {
      'errors': {
        'message': [error],
        'fields': [error-fields],
      }
    }
    ```

* **Sample Call:**

  `GET`
  ```javascript
  $.ajax({
    url: "/api/ctfs?online=true",
    dataType: "json",
    type : "GET",
    success : function(r) {
      console.log(r);
    }
  });
  ```

  `POST`
  ```javascript
  $.ajax({
    url: "/api/ctfs",
    dataType: "json",
    type : "POST",
    data: {
      "ctf": {
        "name": "new ctf",
        "online": true,
        "ctftime": null,
        "about": null,
        "home": null,
        "challengeboard": null,
        "scoreboard": null
      }
    },
    success : function(r) {
      console.log(r);
    }
  });
  ```

* **Notes:**

  This route is used to create ctfs and to obtain the current online ctf that edCTF is running.

## ctfs/:id

