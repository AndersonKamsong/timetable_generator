from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from .models import Room, Teacher, Course, Timetable
from .optimization.solver import generate_timetable
from .forms import TimetableForm


class GenerateTimetableView(FormView):
    template_name = 'timetable/generate.html'
    form_class = TimetableForm
    
    def form_valid(self, form):
        courses = list(Course.objects.all())
        rooms = list(Room.objects.all())
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        time_slots = ['9:00-11:00', '11:00-13:00', '14:00-16:00', '16:00-18:00']
        
        timetable = generate_timetable(courses, rooms, days, time_slots)
        
        # Prepare data for saving
        serialized = {}
        for day in days:
            serialized[day] = {}
            for slot in time_slots:
                serialized[day][slot] = {}
                for room_name, assignment in timetable[day][slot].items():
                    if assignment['course']:
                        serialized[day][slot][room_name] = {
                            'course': {
                                'code': assignment['course'].code,
                                'name': assignment['course'].name,
                                'id': assignment['course'].id
                            },
                            'teacher': {
                                'name': assignment['teacher'].name,
                                'id': assignment['teacher'].id
                            }
                        }
                    else:
                        serialized[day][slot][room_name] = 'Free'
        # Save to database
        timetable_obj = Timetable.objects.create(
            name=form.cleaned_data['name'],
            schedule=serialized
        )
        print("timetable_obj")
        print(timetable_obj.schedule)
        
        return render(self.request, 'timetable/result.html', {
            'timetable': timetable_obj,
            'days': days,
            'time_slots': time_slots,
            'rooms': Room.objects.all().order_by('name')  # Make sure to pass rooms
        })
        
# class GenerateTimetableView(FormView):
#     template_name = 'timetable/generate.html'
#     form_class = TimetableForm
    
#     def form_valid(self, form):
#         courses = list(Course.objects.all())
#         rooms = list(Room.objects.all())
#         days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#         time_slots = ['9:00-11:00', '11:00-13:00', '14:00-16:00', '16:00-18:00']
        
#         print("\n=== Timetable Generation Parameters ===")
#         print(f"Courses: {len(courses)}")
#         print(f"Rooms: {len(rooms)}")
        
#         timetable = generate_timetable(courses, rooms, days, time_slots)
        
#         # Prepare data for saving and display
#         serialized_timetable = {}
#         print(timetable)
#         for day in days:
#             serialized_timetable[day] = {}
#             for slot in time_slots:
#                 serialized_timetable[day][slot] = {}
#                 for room_name, assignment in timetable[day][slot].items():
#                     if assignment['course']:
#                         serialized_timetable[day][slot][room_name] = {
#                             'course': {
#                                 'code': assignment['course'].code,
#                                 'name': assignment['course'].name,
#                                 'id': assignment['course'].id
#                             },
#                             'teacher': {
#                                 'name': assignment['teacher'].name,
#                                 'id': assignment['teacher'].id
#                             }
#                         }
#                     else:
#                         serialized_timetable[day][slot][room_name] = 'Free'
        
#         # Save to database
#         timetable_obj = Timetable.objects.create(
#             name=form.cleaned_data['name'],
#             schedule=serialized_timetable
#         )
        
#         return render(self.request, 'timetable/result.html', {
#             'timetable': timetable_obj,
#             'days': days,
#             'time_slots': time_slots,
#             'rooms': rooms
#         })

def timetable_list(request):
    timetables = Timetable.objects.all().order_by('-created_at')
    return render(request, 'timetable/list.html', {'timetables': timetables})

def timetable_detail(request, pk):
    timetable_obj = Timetable.objects.get(pk=pk)
    # schedule = timetable.schedule
    
    # Format the schedule for display
    formatted_schedule = {}    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = ['9:00-11:00', '11:00-13:00', '14:00-16:00', '16:00-18:00']
    # courses = list(Course.objects.all())
    # rooms = list(Room.objects.all())
    
    return render(request, 'timetable/result.html', {
        'timetable': timetable_obj,
        'days': days,
        'time_slots': time_slots,
        'rooms': Room.objects.all().order_by('name')  # Make sure to pass rooms
    })
    
def timetable_delete(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        return redirect('timetable_list')
    return redirect('timetable_detail', pk=pk)
