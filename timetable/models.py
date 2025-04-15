from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    availability = models.JSONField(default=list)  # List of available time slots
    
    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in hours")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students_enrolled = models.IntegerField()
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def __lt__(self, other):
        # Compare courses by code for sorting
        return self.code < other.code

class Timetable(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    schedule = models.JSONField()  # Will store the generated timetable
    
    def __str__(self):
        return self.name