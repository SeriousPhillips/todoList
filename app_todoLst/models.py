from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Task(models.Model):

	#priority_cats=[ (0,'low'),(1,'medium'),(2,'high')  ]
	#status_cats=[ (0,'waiting'),(1,'in_progress'),(2,'done')  ]

	task_text=models.CharField(max_length=300)
	priority=models.IntegerField()
	status=models.IntegerField()
	user=models.ForeignKey(User, on_delete=models.CASCADE)


		

