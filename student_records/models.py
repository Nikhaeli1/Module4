from django.db import models
from django.contrib.auth.models import User

class StudentRecord(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_records',
        help_text='The student account this record belongs to.',
    )
    full_name  = models.CharField(max_length=100)
    course     = models.CharField(max_length=50)
    year_level = models.IntegerField()
    gpa        = models.DecimalField(max_digits=4, decimal_places=2,
                                     null=True, blank=True)
    enrolled   = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} — {self.course} Year {self.year_level}'