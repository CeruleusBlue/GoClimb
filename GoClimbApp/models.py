from django.db import models


# Create your models here.
class MBPost(models.Model):
    text = models.TextField()
    title = models.TextField()
    time = models.DateTimeField(primary_key=True)        
class cragDestination(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    summary = models.TextField
    description = models.TextField()
    access = models.TextField()
    approach = models.TextField()
    history = models.TextField()

class cragRoute(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    grade = models.IntegerField()
    image = models.ImageField(null=True, blank=True, upload_to = "static/images/cragRoutes")
    description = models.TextField()
    bolts = models.IntegerField()
    rating = models.IntegerField()
    length = models.IntegerField()
    ascents = models.IntegerField()
    firstAscent = models.TextField()
    cragDestinationFK = models.ForeignKey(cragDestination, default=None, on_delete=models.CASCADE)

class cragRouteReview(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    cragRouteFK = models.ForeignKey(cragRoute, default=None, on_delete=models.CASCADE)

class cragFace(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    locationX = models.FloatField()
    locationY = models.FloatField()
    description = models.TextField()
    access = models.TextField()
    approach = models.TextField()
    ethics = models.TextField()
    cragRouteFK = models.ForeignKey(cragRoute, default=None, on_delete=models.CASCADE)


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.product.name