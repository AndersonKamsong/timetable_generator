from django.urls import path
from .views import GenerateTimetableView, timetable_list, timetable_detail,timetable_delete

urlpatterns = [
    path('', timetable_list, name='timetable_list'),
    path('generate/', GenerateTimetableView.as_view(), name='generate_timetable'),
    path('<int:pk>/', timetable_detail, name='timetable_detail'),
    path('<int:pk>/delete/', timetable_delete, name='timetable_delete'),

]