from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('CR', 'Curd'),
    ('ML', 'Milk'),
    ('LS', 'Lassi'),
    ('MS', 'Milkshake'),
    ('PN', 'Paneer'),
    ('GH', 'Ghee'),
    ('CZ', 'Cheese'),
    ('IC', 'Ice-Creams'),
)

COUNTY_CHOICES = (
    ('mombasa', 'Mombasa'),
    ('kwale', 'Kwale'),
    ('kilifi', 'Kilifi'),
    ('tana_river', 'Tana River'),
    ('lamu', 'Lamu'),
    ('taita_taveta', 'Taita Taveta'),
    ('garissa', 'Garissa'),
    ('wajir', 'Wajir'),
    ('mandera', 'Mandera'),
    ('marsabit', 'Marsabit'),
    ('isiolo', 'Isiolo'),
    ('meru', 'Meru'),
    ('tharaka_nithi', 'Tharaka Nithi'),
    ('embu', 'Embu'),
    ('kitui', 'Kitui'),
    ('machakos', 'Machakos'),
    ('makueni', 'Makueni'),
    ('nyandarua', 'Nyandarua'),
    ('nyeri', 'Nyeri'),
    ('kirinyaga', 'Kirinyaga'),
    ('murang_a', 'Muranga'),
    ('kiambu', 'Kiambu'),
    ('turkana', 'Turkana'),
    ('west_pokot', 'West Pokot'),
    ('samburu', 'Samburu'),
    ('trans_nzoia', 'Trans Nzoia'),
    ('uasin_gishu', 'Uasin Gishu'),
    ('elgeyo_marakwet', 'Elgeyo Marakwet'),
    ('nandi', 'Nandi'),
    ('baringo', 'Baringo'),
    ('laikipia', 'Laikipia'),
    ('nakuru', 'Nakuru'),
    ('narok', 'Narok'),
    ('kajiado', 'Kajiado'),
    ('kericho', 'Kericho'),
    ('bomet', 'Bomet'),
    ('kakamega', 'Kakamega'),
    ('vihiga', 'Vihiga'),
    ('bungoma', 'Bungoma'),
    ('busia', 'Busia'),
    ('siaya', 'Siaya'),
    ('kisumu', 'Kisumu'),
    ('homabay', 'Homa Bay'),
    ('migori', 'Migori'),
    ('kisii', 'Kisii'),
    ('nyamira', 'Nyamira'),
    ('nairobi', 'Nairobi'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    county = models.CharField(choices=COUNTY_CHOICES, max_length=100)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.dicounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price