# SF-Food-Trucks
![WebAppScreenshot](https://lh4.googleusercontent.com/Nu0ZGBXi8wWQyPWUWFvtXMICVRZ9co0iF0_-XI_x3XAmiQa4iCHu1SvxBxDy2-M0VRwuQAr2VsyEhw=w1301-h678-rw)
This is a food trucks finder in San Fransisco. This project was done in two weeks with around 38 hours of coding as part of Uber backend coding challenges. The app is hosted and can be found [here](https://ahmedameen.pythonanywhere.com/).  
## Web App Features
* Search for a location using google maps search box.
* View trucks information by clicking on the trucks markers on the map.
* Review the food trucks by clicking like/ dislike buttons on the information window (user login is required).
* View top rated food trucks based on user reviews.  
* View food trucks locations from the top list by clicking on the truck name.

## API Features
* Get food trucks near a specific location in San Fransisco.
* Get food truck information specified by ID.
* Get all users reviews for a food truck specified by ID.
* Get top food trucks IDs based on users reviews.
## API Documentation
* Get food trucks near a specific location in San Fransisco API.
  * End Point: '/foodtrucks/GetFoodTrucksNearLocation'
  * Method: GET
  * Parameters:
    * locationLat (decimal number): the latitude of the location.
    * locationLng (decimal number): the longitude of the location.
    * maxDistanceInMeters (decimal number): the maximum distance for the returned food trucks from the location in meters.
    * limit (integer number) (optional): to limit the number of returned food trucks.
  * Returns:
    * Status code: 200 ok
    * Response: array of json truck object with the following fields: 
      * objectid (integer number): the id of the food truck.
      * address (text): the address of the food truck.
      * fooditems (text): the food items the food trucks sells.
      * latitude (decimal number): the latitude of the food truck location.
      * longitude (decimal number): the longitude of the food truck location.
      * dayshours (text): the abbreviated text of the food truck working hours.
      * facilitytype (text): 'truck' or 'push cart'.              
    * Errors:
      * Status code: 400
      * Response: 'Bad request, missing or wrong passed arguments. Please review the API documentation for the correct format.' 
* Get food truck information specified by ID API.
  * End Point: '/foodtrucks/GetFoodTruck'
  * Method: GET
  * Parameters:
    * truckID (integer number): the ID of the truck.
  * Returns:
    * Status code: 200 ok
    * Response: truck object in json format.
  * Errors:
    * Status code: 400
    * Response: 'Bad request, missing or wrong passed arguments. Please review the API documentation for the correct format.' 

* Get all users reviews for a food truck API.
  * End Point: '/reviews/GetTruckReviews'
  * Method: GET
  * Parameters:
    * truckID (integer number): the ID of the truck.
  * Returns:
    * Status code: 200 ok
    * Response: json object with the following fields:
      * id (integer number): the id of the truck.
      * likes (integer number): number of likes this truck received. 
      * dislikes (integer number): number of dislikes this truck received.
  * Errors:
      * Status code: 400
      * Response: 'Bad request, missing or wrong passed arguments. Please review the API documentation for the correct format.' 
      
* Get top food trucks ID's based on users reviews API.
  * End Point: '/GetBestTrucks'
  * Method: GET
  * Parameters:
    * top (integer number)(optional): to limit the result.  
  * Returns:
    * Status code: 200 ok
    * Response: array of json object with the following fields:
      * id (integer number): the id of the truck.
      * likes (integer number): number of likes this truck received. 
      * dislikes (integer number): number of dislikes this truck received.
      
## Devlopment Languages/ Tools

### For Backend:

* Framework: Flask.  
  * Why Flask? I had no experience with Flask before I use ASP.NET for backend so I decided to work with a new framework. I went with Flask because it's suitable for small web applications and can be learnt quickly.  
* Database: SQLite.  
  * Why SQLite? In this application I used a SQLite database to store simple data about the users/ food trucks. The detailed food trucks data are retrieved from [DataSF API documentation](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat) so SQLite was a quick and suitable solution.

### For Frontend:
* Javascript.  
* Google maps API.  
* jQuery.  

## Needed/ Future Improvements
* Use a hosted database instead of SQLite for scaling.
* Use ORM to manipulate the data instead of SQL queries.
* Store all the food trucks info in the database instead of retrieving them using DataSF API to remove the dependency and update the database periodically to add the new trucks.
* Add verification steps in user registration for security.
* Add additional ways to choose a location other than the search box like choosing from the map directly or geolocalizing. 
* Add personalized recommendations for food trucks for each user user reviews and user location.
