# API Documentation

The edCTF API utilizes a hierarchical, RESTful structure in order to allow for simple interaction and to be highly scalable.  This guide describes the API in detail.

===

## Table of Contents
* [Overview](#Overview)
* [abouts/:id](#abouts-id)
* [categories](#categories)
 * [categories/:id](#categories-id)
* [challenges](#challenges)
 * [challenges/:id](#challenges-id)
* [challengeboards](#challengeboards)
 * [challengeboards/:id](#challengeboards-id)
* [ctfs](#ctfs)
 * [ctfs/:id](#ctfs-id)
* [ctftime/:id](#ctftime-id)
* [flags](#flags)
 * [flags/:id](#flags-id)
* [homes/:id](#homes-id)
* [scoreboards](#scoreboards)
 * [scoreboards/:id](#scoreboards-id)
* [session](#session)
* [teams](#teams)
 * [teams/:id](#teams-id)

===

## Overview
The edCTF API is structured to support multiple CTFs on the same framework.

To accomplish this, the API uses a hierarchical pattern where a `ctf` is the peak and smaller, more frequent, objects are placed towards the bottom, such as `teams` and `challenges`.

The general structure of this can be seen as follows:
```
 - ctfs
   |- challengeboards
      |- categories
         |- challenges
   |- scoreboards
      |- teams
```
There are more routes than those listed above.  These routes add more functionality to edCTF.  One of these for example, is the [ctftime](#ctftime) route.  More information on these routes can be seen below.

===

<a name="abouts-id"></a>
## abouts/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

## categories
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

<a name="categories-id"></a>
## categories/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

## challenges
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

<a name="challenges-id"></a>
## challenges/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

## challengeboards
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

<a name="challengeboards-id"></a>
## challengeboards/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

## ctfs
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

<a name="ctfs-id"></a>
## ctfs/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

<a name="ctfs-id"></a>
## ctfs/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

<a name="ctftime-id"></a>
## ctftime/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

## flags
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

<a name="flags-id"></a>
## flags/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

<a name="homes-id"></a>
## homes/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

## scoreboards
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

<a name="scoreboards-id"></a>
## scoreboards/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

## session
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===

## teams
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

<a name="teams-id"></a>
## teams/:id
  <!-- brief description -->

* **URL**

  <!--
  /api/
  -->

* **Method:**

  <!--
  `GET` | `POST` | `DELETE` | `PUT`
  -->
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  <!--- Data params by request -->

* **Success Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->
 
* **Error Response:**

  * **Code:** <!--- Error Code -->

    **Content:**
    <!--- JSON Response -->

* **Sample Call:**

  <!--- Example call using ajax -->

* **Notes:**

  <!--- Add notes not mentioned above -->

===
