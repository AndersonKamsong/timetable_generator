import random
import sys
from collections import defaultdict
from .constraints import no_teacher_overlap, room_capacity_check, teacher_availability

from collections import defaultdict
import random

# def generate_timetable(courses, rooms, days, time_slots, max_attempts=100):
#     """
#     Generate a timetable with structure:
#     {
#         'Monday': {
#             '9:00-11:00': {
#                 'Room 101': {'course': course_obj, 'teacher': teacher_obj},
#                 'Room 102': {'course': None, 'teacher': None},  # Free
#                 ...
#             },
#             ...
#         },
#         ...
#     }
#     """
#     print("\n=== Starting Timetable Generation ===")
    
#     # Initialize timetable structure with all slots free
#     timetable = {
#         day: {
#             slot: {
#                 room.name: {'course': None, 'teacher': None}
#                 for room in rooms
#             }
#             for slot in time_slots
#         }
#         for day in days
#     }
    
#     # Track scheduled courses to avoid duplicates
#     scheduled_courses = set()
    
#     # Sort courses by difficulty (larger classes first, then by teacher availability)
#     sorted_courses = sorted(
#         courses,
#         key=lambda c: (-c.students_enrolled, len(c.teacher.availability))
#     )
    
#     for course in sorted_courses:
#         if course in scheduled_courses:
#             continue
            
#         scheduled = False
        
#         # Try to find an available slot
#         for attempt in range(max_attempts):
#             # Try rooms in order of capacity (smallest suitable first)
#             suitable_rooms = sorted(
#                 [r for r in rooms if r.capacity >= course.students_enrolled],
#                 key=lambda r: r.capacity
#             )
            
#             # Try days and slots in random order
#             random.shuffle(days)
#             random.shuffle(time_slots)
            
#             for day in days:
#                 for slot in time_slots:
#                     # Check teacher availability
#                     if (day, slot) not in course.teacher.availability:
#                         continue
                        
#                     # Find first available suitable room
#                     for room in suitable_rooms:
#                         if timetable[day][slot][room.name]['course'] is None:
#                             # Schedule the course
#                             timetable[day][slot][room.name] = {
#                                 'course': course,
#                                 'teacher': course.teacher
#                             }
#                             scheduled_courses.add(course)
#                             scheduled = True
#                             print(f"Scheduled {course.code} in {room.name} at {day} {slot}")
#                             break
#                     if scheduled:
#                         break
#                 if scheduled:
#                     break
#             if scheduled:
#                 break
                
#         if not scheduled:
#             print(f"Warning: Could not schedule {course.code} after {max_attempts} attempts")
    
#     return timetable

# timetable/optimization/solver.py

from collections import defaultdict
import random

def generate_timetable(courses, rooms, days, time_slots):
    """
    Generate a timetable with structure:
    {
        'Monday': {
            '9:00-11:00': {
                'Room 101': {'course': course_obj, 'teacher': teacher_obj},
                'Room 102': {'course': None, 'teacher': None},  # Free
                ...
            },
            ...
        },
        ...
    }
    """
    # Initialize timetable structure with all slots free
    timetable = {
        day: {
            slot: {
                room.name: {'course': None, 'teacher': None}
                for room in rooms
            }
            for slot in time_slots
        }
        for day in days
    }
    
    # Track teacher schedules to prevent double-booking
    teacher_schedule = defaultdict(set)  # {teacher: {(day, slot)}}
    
    # Sort courses by difficulty (larger classes first)
    sorted_courses = sorted(
        courses,
        key=lambda c: (-c.students_enrolled, len(c.teacher.availability)))
    
    for course in sorted_courses:
        scheduled = False
        
        # Get all possible time slots for this course (teacher availability)
        # print(course.teacher.availability)
        # print(course.teacher.name)
        # print(days)
        # print(time_slots)
        # print((day, slot) 
            # for day in days 
            # for slot in time_slots)
        available_slots = [
            [day, slot] 
            for day in days 
            for slot in time_slots 
            if [day, slot] in course.teacher.availability
        ]
        # print(available_slots)
        print("available_slots")
        # Randomize the order we try slots
        random.shuffle(available_slots)
        # print(available_slots)
        
        for day, slot in available_slots:
            # Skip if teacher already booked at this time
            # print(teacher_schedule[course.teacher])
            # print(day)
            # print(slot)
            if (day, slot) in teacher_schedule[course.teacher]:
                continue
                
            # Find suitable rooms (with enough capacity)
            # print(rooms)
            # print("rooms")
            suitable_rooms = [
                room for room in rooms
                if room.capacity >= course.students_enrolled
                and timetable[day][slot][room.name]['course'] is None
            ]
            # print(suitable_rooms)
            
            if suitable_rooms:
                # Pick the smallest suitable room
                room = min(suitable_rooms, key=lambda r: r.capacity)
                
                # print(room)
                # print(room.name)
                # Schedule the course
                timetable[day][slot][room.name] = {
                    'course': course,
                    'teacher': course.teacher
                }
                print(day,slot,room.name,timetable[day][slot][room.name])
                
                teacher_schedule[course.teacher].add((day, slot))
                scheduled = True
                break
                
        if not scheduled:
            print(f"Warning: Could not schedule {course.code}")
    # print("timetable")
    # print(timetable)
    return timetable

def greedy_timetable(courses, rooms, days, time_slots):
    """Alternative greedy algorithm implementation"""
    print("\nRunning alternative greedy algorithm...")
    
    # We'll use the same implementation as the main function now
    return generate_timetable(courses, rooms, days, time_slots, max_attempts=len(days)*len(time_slots))