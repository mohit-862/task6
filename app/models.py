from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.


class Customuser(AbstractUser):
    phone = models.PositiveBigIntegerField(null = True)
    role = models.CharField(max_length=10)
    def __str__(self):
        return self.first_name
    

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True,null=False)
    def __str__(self):
        return self.name
    
    

class Product(models.Model):
    title = models.CharField(max_length=30,unique=True)
    description = models.TextField()
    product_img = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=50,null=False,unique=True)
    category  = models.ForeignKey(Category,on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # return f"{self.slug}/"
        # {% for obj in object_list  %}
        #    <a href="{{obj.get_absolute_url}} ">{{obj.title}}</a> <br>
        # {% endfor %}
        # Or better yet, use the view name using reverse: def get_absolute_url(self): return reverse("viewname in urls.py", kwargs={"slug": self.slug})
        return reverse('product_details',kwargs={'slug':self.slug})
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.description:
            self.description = f"This is a {self.title}"

        return super().save(*args,**kwargs)

    

