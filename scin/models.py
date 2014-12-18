from django.db import models
from django.utils import timezone

# Create your models here.
class pub_meta(models.Model):
	doc_id = models.CharField(max_length=50)
	src_address = models.CharField(max_length=100)
	pdf_address = models.CharField(max_length=100)
	publisher = models.CharField(max_length=100)
	title = models.CharField(max_length=800)
	editors = models.CharField(max_length=200)
	pub_date = models.DateField()
	copyright = models.TextField()
	data_availibility = models.TextField()
	funding = models.TextField()
	competing_interest = models.TextField()
	rec_update_time = models.DateTimeField(auto_now=True)
	rec_update_by = models.CharField(max_length=20)

class pub_material_n_method(models.Model):
	doc_id = models.ForeignKey(pub_meta)
	section_id = models.IntegerField()
	header = models.CharField(max_length=800)
	content_seq = models.IntegerField()
	content = models.TextField()

class pub_figure(models.Model):
	doc_id = models.ForeignKey(pub_meta)
	figure_id = models.IntegerField()
	header = models.CharField(max_length=800)
	content = models.TextField()
	url = models.CharField(max_length=100)