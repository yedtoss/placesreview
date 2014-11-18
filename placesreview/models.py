from django.db import models


# models of the API.


class Application(models.Model):
    """
    Used to identified an application accessing the API
    """
    name = models.CharField(max_length=1000)


class Reviewer(models.Model):
    """
    The reviewer model
    """
    google_id = models.TextField(null=True, blank=True)
    facebook_id = models.TextField(null=True, blank=True)


class PlaceType(models.Model):
    """
    Type of places.  Eg   restaurant
    """

    name = models.CharField(max_length=1000)


class Place(models.Model):
    """
    The places modes
    """
    google_id = models.TextField()
    types = models.ManyToManyField(PlaceType)


class PlaceService(models.Model):
    """
    The different services offered by the place.
    Eg: For a restaurant we have multiple menu
    """
    name = models.CharField(max_length=1000)
    place = models.ForeignKey(Place)


class TasteToBeReviewed(models.Model):
    """
    Represents a list of choices or tastes the reviewer can review
    Eg: For restaurant, we have food quality, service, cost , food taste ...
    """
    name = models.CharField(max_length=1000)
    service = models.ForeignKey(PlaceService)


class Review(models.Model):
    """
    Represents a review for a place
    """

    reviewer = models.ForeignKey(Reviewer)
    created_on = models.DateTimeField(auto_now_add=True)
    # The application which has updated this review
    created_by = models.ForeignKey(Application, null=True)
    text = models.TextField()
    # general score given by this review
    score = models.DecimalField(default=0, decimal_places=2, max_digits=19)
    service = models.ForeignKey(PlaceService)


class ReviewScoreByTaste(models.Model):
    review = models.ForeignKey(Review)
    taste = models.ForeignKey(TasteToBeReviewed)
    rating = models.IntegerField(default=5)
    text = models.TextField(blank=True, null=True)



