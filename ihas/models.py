from django.contrib.auth.models import User
from accounts.models import Address
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)
    category_slug = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.category_slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


STATUS_CHOICES = (
    ("Active", "Active"),
    ("Passive", "Passive")
)


class Uav(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    brand = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    year = models.DateField()
    weight = models.IntegerField()
    features = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Passive")
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', default='uploads/default.jpg', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'uavs'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Uav, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uav = models.ForeignKey(Uav, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default='2024-01-01')
    end_date = models.DateTimeField(default='2024-01-01')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.uav.name} - {self.start_date} to {self.end_date}"
