from django.db import models

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(
        upload_to='media/categories/', blank=True, null=True)

    # Adds text field for descrition with no lenght limit and it is optional
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return 'https://cdn.shopify.com/s/files/1/0648/0124/3361/files/logo-light.png?v=1656315496&width=100'
