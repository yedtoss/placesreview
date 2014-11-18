Installation

1-You can deploy locally.

Just install python then install django and requests and MySQL-python

Install Mysql and it's lib sudo apt-get install libmysqlclient-dev mysql on ubuntu

From the root of the submission, run  python manage.py syncdb
then python manage.py runserver


2- You can simply test the application from this URL:



Goal:

There are lot of websites which show reviews for places, restaurants, hotels and so on.
Most of them only allow the user to review  and rate the places as a whole. In the reality the user has only
experienced
a tiny part of the services offered by the business.

For example, in restaurants a user can taste a meal and find it not good enough. But that does not mean that all the
food from this restaurants are bad. There are surely some good meal there.


The first objective of this API is to give a platform to developer to take that into account. We give an API which
allows developers to allow their user to be more precise in the review and ratings.
More precisely, the API will provide to the developers the places, their services as well as the tastes user should
rate. The developers can now focus on awesome applications allowing the users to rate and review according to the
service and to the taste.

An example of a taste for a restaurant is the following: A user can appreciate a food but don't like how expensive it
 is or how he was greeted.


 The second objective of the API is to allow developers to profit on a platform where users reviews are coordinated.
 In other word, a developer will have access to the reviews of the users of another applications.
 That will help him improve the quality of his own application. This will also lead


 This is beneficial in many situations:

 1- If a user was paid to make a bad review on some business, this can be detected if he make a good review of the
 same business in another application

 2- A user can stop using frequently an application and start another one. But the first application will still have
 all reviews and rating of the user.


 It is as if the API allow a Peer to peer application development. Every applications coordinate to the same goal.
 Get a true and trustful judgement of a business



Next Features to develop:

1- Integrate the Nymi API http://www.getnymi.com/  so that user won't need anymore passwords to authenticate.
This will also lead to a true identity for each user and will lead to each user to be as trustful as possible.

2- Allow searching through reviews based on user experience.
For example a Brasil native can like a meal a US native does not like.
By being able to look through this kind of data it will be possible for user (or even machine learning algorithms) to
know if the ratings or review of a use has been biased by his background or ground truth.





Documentation

Description:  Places Review API that only peer to peer opinion based applications.

Introduction: Places Review is an API that allows developer to


Developers are expected to retrieve the current location of the user and make a request to this api in order
to get the places where the user is located.

if an application only focus on restaurant for example, it can send restaurant for the parameter types to only show the
most likely restaurant

Application are expected to use a low radius so that the first places returned is more likely the user location


The google_key can be used by each application so that they control their own limit.  The API does not store it.



API: GET  /search_places?parameters


parameters can be:
  - location (Required), The latitude/longitude around which to retrieve place information. This must be specified as
  latitude,longitude.
  - radius (Optional, Default to 20) Defines the distance (in meters) within which to return place results. The
  maximum allowed radius is
  50 000 meters.
  - types  as described  in  Restricts the results to places matching at least one of the specified types.
    Types should be separated with a pipe symbol (type1|type2|etc). See the list of supported types here
     https://developers.google.com/places/documentation/supported_types

  - google_key (Optional) The google key to use when making request to the google places API

  - pagetoken pagetoken — Returns the next 20 results from a previously run search.
    Setting a pagetoken parameter will execute a search with the same parameters used previously
     — all parameters other than pagetoken will be ignored. You can see the next token to use in the result key next_page_token


Check https://developers.google.com/places/documentation/search for information on the return format

The result format is the same as the one from the above link plus the additions of the key services which list the
list of services of the given places.

There is also the list of tastes returned in the key tastes




GET
NB For ease of use this is not a POST request but instead a GET.



Testing:
1- Make a get request to
http://127.0.0.1:8000/search_places?location=-33.8670522,151.1957362&radius=200

2- Add a review
http://127.0.0.1:8000/add_review?place_id=ChIJAWLZAzSuEmsRkMcyFmh9AQU&google_user_id=12334&text=good&service=General

3- Get the review
http://127.0.0.1:8000/get_review?place_id=ChIJAWLZAzSuEmsRkMcyFmh9AQU






















Technologies used:

Google API for accessing places search
Amazon API for RDS with Mysql
Heroku is hosting the application