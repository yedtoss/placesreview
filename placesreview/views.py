
import requests
from django.conf import settings
import json
from django.http.response import HttpResponse
from placesreview import models
import math
from django.db.models import Q
import traceback


# Views of the API


def render_to_json_response(context, status=200):
    """
    Convert json string to http response.
    @param context variable in json, dictionary
    @return http response corresponding to the string
    """

    data = json.dumps(context)
    ret = HttpResponse(data, status=status)
    return ret


def is_int(value):
    result = True
    try:
        num = int(value)
        if math.isnan(num):
            result = False
    except ValueError as e:
        result = False
    return result


def clean_dict(dictionary):
    """
    Clean a dictionary by removing all key whose value are None
    """
    dictionary = {}

    for key in dictionary.keys():
        if dictionary[key] is None:
            del dictionary[key]

    return dictionary


def search_places(request):
    # See https://developers.google.com/places/documentation/search
    # For documentation of the parameters. Only parameters here are supported
    # but you can always use the extra parameters to pass more

    types = None
    location = None
    radius = 20
    key = settings.GOOGLE_KEY
    pagetoken = None

    if request.GET.get("location") is not None:
        location = request.GET.get("location")

    if request.GET.get("radius") is not None:
        radius = request.GET.get("radius")

    if request.GET.get("types") is not None:
        types = request.GET.get("types")

    if request.GET.get("google_key") is not None:
        key = request.GET.get("google_key")

    if location is None:
        return render_to_json_response({"error": "location is required"}, 400)

    if request.GET.get("pagetoken"):
        pagetoken = request.GET.get("pagetoken")

    payload = {
        "types": types,
        "location": location,
        "radius": radius,
        "key": key,
        "pagetoken": pagetoken

    }

    clean_dict(payload)

    try:
        response = requests.get(settings.GOOGLE_PLACE_URL + "/nearbysearch/json", params=payload)

        data = json.loads(response.content)

        for place in data["results"]:
            entity = models.Place.objects.filter(google_id=place["place_id"])
            if entity.count() > 0:
                continue
            entity = models.Place()
            entity.google_id = place["place_id"]
            entity.save()
            entity.types = []

            for cat in place["types"]:
                res = models.PlaceType.objects.filter(name=cat)

                if res.count() <= 0:
                    res = models.PlaceType()
                    res.name = cat
                    res.save()
                else:
                    res = res[0]

                entity.types.add(res)

            entity.save()


            restaurant_type = models.PlaceType.objects.filter(name="restaurant")

            services = settings.DEFAULT_SERVICES
            tastes = settings.DEFAULT_TASTES

            #if restaurant_type in entity.types.all():
              #  pass

            for name in services:
                placeService = models.PlaceService()
                placeService.name = name
                placeService.place = entity
                placeService.save()

                for str in tastes:
                    to_review = models.TasteToBeReviewed()
                    to_review.name = str
                    to_review.service = placeService

            place["services"] = services

            place["tastes"] = tastes

        return render_to_json_response(data)

    except Exception as e:
        traceback.print_exc()
        return render_to_json_response({"error": "error while searching"}, 400)


def add_review(request):
    """
    Add a review
    """

    place_id = ""
    google_id = ""
    facebook_id = ""
    text = ""
    service_name = settings.DEFAULT_SERVICES[0]
    app_id = ""

    ratings = []
    tastes = []

    if request.GET.get("place_id") is not None:
        place_id = request.GET.get("place_id")

    if request.GET.get("google_user_id") is not None:
        google_id = request.GET.get("google_user_id")

    if request.GET.get("facebook_user_id") is not None:
        facebook_id = request.GET.get("facebook_user_id")

    if request.GET.get("text") is not None:
        text = request.GET.get("text")

    if request.GET.get("service") is not None:
        service_name = request.GET.get("service")

    if request.GET.get("tastes") is not None:
        tastes = request.GET.get("tastes").split(',')

    temp = None
    if request.GET.get("ratings") is not None:
        temp = request.GET.get("ratings").split(',')

    if len(ratings) != len(tastes):
        return render_to_json_response({"error": "you should provide a rating for each taste. ratings and tastes "
                                                 "array should thus be equal."}, 400)

    if temp:
        for rating in ratings:
            if rating and is_int(rating):
                ratings.append(int(request.GET.get("ratings")))

    if request.GET.get("app_id"):
        app_id = int(request.GET.get("app_id"))

    reviewer = models.Reviewer.objects.filter(Q(google_id=google_id) | Q(facebook_id=facebook_id))

    if reviewer.count() <= 0:
        reviewer = models.Reviewer()
        reviewer.google_id = google_id
        reviewer.facebook_id = facebook_id
        reviewer.save()
    else:
        reviewer = reviewer[0]

    application = models.Application.objects.filter(name=app_id)

    place = models.Place.objects.filter(google_id=place_id)

    if place.count() > 0:
        place = place[0]

    service = models.PlaceService.objects.filter(name=service_name, place__pk=place.pk)

    if service.count() > 0:
        service = service[0]

    if application.count() > 0:
        application = application[0]
    else:
        application = None

    try:
        if reviewer:
            review = models.Review()
            review.reviewer = reviewer

            if application:
                review.application = application

            review.text = text

            review.service = service
            review.save()

            num = 0.
            for i in range(len(ratings)):

                score_by_taste = models.ReviewScoreByTaste()
                score_by_taste.review = review
                score_by_taste.rating = ratings[i]
                taste = models.TasteToBeReviewed.objects.filter(name=tastes[i], service=service)
                if taste.count() > 0:
                    score_by_taste.taste = taste[0]
                num += ratings[i]

                score_by_taste.save()

            if len(ratings) > 0:
                review.score = num/len(ratings)

            review.save()
    except Exception as e:
        traceback.print_exc()
        return render_to_json_response({"error": "error while adding review"}, 400)

    return render_to_json_response({"success": True})


def get_review(request):
    """
    Get a review
    """
    if request.GET.get("place_id") is not None:
        place_id = request.GET.get("place_id")

    qs = models.Review.objects.filter(service__place__google_id=place_id).order_by('created_on')

    if request.GET.get("app_id"):
        qs = qs.filter(created_by=request.GET.get("app_id"))

    data = []

    for review in qs:

        ratings = []

        rats = models.ReviewScoreByTaste.objects.filter(review__pk=review.pk)

        for rat in rats:
            ratings.append({
                "rating": rat.rating,
                "text": rat.text,
                "taste": rat.taste.name
            })
        temp = {
            "reviewer_google_id": review.reviewer.google_id,
            "reviewer_facebook_id": review.reviewer.facebook_id,
            "text": review.text,
            "score": float(review.score),
            "service": review.service.name,

            "ratings": ratings
        }

        data.append(temp)

    return render_to_json_response(data)
