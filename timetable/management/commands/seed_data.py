from django.core.management.base import BaseCommand
from timetable.models import Room, Teacher, Course
import random
from itertools import cycle

class Command(BaseCommand):
    help = 'Populates the database with optimized timetable data for one week'

    def handle(self, *args, **options):
        self.stdout.write("Seeding optimized timetable data...")
        
        # Clear existing data
        Room.objects.all().delete()
        Teacher.objects.all().delete()
        Course.objects.all().delete()

        # Create rooms with realistic capacities
        rooms = [
            {"name": "Lecture Hall A", "capacity": 50},
            {"name": "Lecture Hall B", "capacity": 45},
            {"name": "Room 101", "capacity": 30},
            {"name": "Room 102", "capacity": 25},
            {"name": "Room 103", "capacity": 20},
            {"name": "Computer Lab", "capacity": 20},
            {"name": "Science Lab", "capacity": 15},
            {"name": "Seminar Room", "capacity": 15},
            {"name": "Room 201", "capacity": 35},
            {"name": "Room 202", "capacity": 25},
        ]
        
        for room_data in rooms:
            Room.objects.create(**room_data)
        
        # Time structure
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        time_slots = ['9:00-11:00', '11:00-13:00', '14:00-16:00', '16:00-18:00']
        
        # Expanded list of subjects
        all_subjects = [
            "Mathematics", "Physics", "Chemistry", "Biology",
            "Computer Science", "Programming", "Data Science",
            "Literature", "History", "Philosophy", "Linguistics",
            "Economics", "Business", "Accounting", "Marketing",
            "Psychology", "Sociology", "Political Science",
            "Engineering", "Architecture", "Art", "Music"
        ]
        
        # Create 20 teachers with realistic availability patterns
        teacher_names = [
            "Dr. Smith", "Prof. Johnson", "Dr. Williams", "Prof. Brown",
            "Dr. Davis", "Dr. Wilson", "Prof. Taylor", "Dr. Anderson",
            "Prof. Martinez", "Dr. Robinson", "Prof. Clark", "Dr. Rodriguez",
            "Prof. Lewis", "Dr. Lee", "Prof. Walker", "Dr. Hall",
            "Prof. Allen", "Dr. Young", "Prof. Hernandez", "Dr. King"
        ]
        
        # Create availability patterns
        availability_patterns = [
            ["Monday", "Wednesday", "Friday"],  # MWF pattern
            ["Tuesday", "Thursday"],            # TTh pattern
            ["Monday", "Tuesday", "Wednesday"], # Early week
            ["Wednesday", "Thursday", "Friday"], # Late week
            ["Monday", "Thursday", "Friday"]    # Mixed pattern
        ]
        
        teacher_objs = []
        for i, name in enumerate(teacher_names):
            # Assign 2-3 subjects per teacher
            subjects = random.sample(all_subjects, random.randint(2, 3))
            
            # Assign availability pattern (cycling through patterns)
            pattern = availability_patterns[i % len(availability_patterns)]
            
            # Generate availability slots (60-80% of possible slots)
            possible_slots = [(day, slot) for day in pattern for slot in time_slots]
            num_slots = int(len(possible_slots) * random.uniform(0.6, 0.8))
            availability = random.sample(possible_slots, num_slots)
            
            teacher = Teacher.objects.create(
                name=name,
                availability=availability,
            )
            teacher_objs.append((teacher, subjects))
        
        # Create balanced courses with realistic scheduling needs
        courses = [
            # Core subjects (multiple sections)
            {"code": "MATH101", "name": "Calculus I", "duration": 2, "students": 30, 
             "preferred_slots": ["9:00-11:00", "11:00-13:00"], "weekly_sessions": 3},
            {"code": "PHYS201", "name": "Classical Mechanics", "duration": 2, "students": 25, 
             "preferred_slots": ["9:00-11:00"], "weekly_sessions": 2},
            {"code": "CHEM101", "name": "General Chemistry", "duration": 2, "students": 25, 
             "preferred_slots": ["14:00-16:00", "16:00-18:00"], "weekly_sessions": 3},
            {"code": "BIO201", "name": "Cell Biology", "duration": 1, "students": 15, 
             "preferred_slots": ["11:00-13:00", "16:00-18:00"], "weekly_sessions": 2},
            
            # Computer Science
            {"code": "CS101", "name": "Intro to Programming", "duration": 2, "students": 20, 
             "preferred_slots": ["14:00-16:00"], "weekly_sessions": 4},
            {"code": "CS201", "name": "Data Structures", "duration": 2, "students": 20, 
             "preferred_slots": ["9:00-11:00"], "weekly_sessions": 2},
            {"code": "CS301", "name": "Algorithms", "duration": 2, "students": 18, 
             "preferred_slots": ["11:00-13:00"], "weekly_sessions": 2},
            
            # Humanities
            {"code": "LIT101", "name": "World Literature", "duration": 1, "students": 20, 
             "preferred_slots": ["9:00-11:00", "16:00-18:00"], "weekly_sessions": 3},
            {"code": "HIST202", "name": "Modern History", "duration": 1, "students": 20, 
             "preferred_slots": ["11:00-13:00"], "weekly_sessions": 2},
            {"code": "PHIL101", "name": "Introduction to Philosophy", "duration": 1, "students": 15, 
             "preferred_slots": ["14:00-16:00"], "weekly_sessions": 1},
            
            # Business/Economics
            {"code": "ECON101", "name": "Microeconomics", "duration": 1, "students": 30, 
             "preferred_slots": ["11:00-13:00"], "weekly_sessions": 3},
            {"code": "BUS202", "name": "Business Management", "duration": 1, "students": 25, 
             "preferred_slots": ["14:00-16:00"], "weekly_sessions": 2},
            {"code": "ACCT101", "name": "Financial Accounting", "duration": 2, "students": 25, 
             "preferred_slots": ["9:00-11:00"], "weekly_sessions": 2},
            
            # Social Sciences
            {"code": "PSY101", "name": "Intro to Psychology", "duration": 1, "students": 20, 
             "preferred_slots": ["9:00-11:00"], "weekly_sessions": 3},
            {"code": "SOC201", "name": "Sociology", "duration": 1, "students": 15, 
             "preferred_slots": ["16:00-18:00"], "weekly_sessions": 2},
            {"code": "POL101", "name": "Political Science", "duration": 1, "students": 20, 
             "preferred_slots": ["11:00-13:00"], "weekly_sessions": 1},
            
            # STEM Electives
            {"code": "ENGR101", "name": "Engineering Principles", "duration": 2, "students": 25, 
             "preferred_slots": ["14:00-16:00"], "weekly_sessions": 1},
            {"code": "DATA101", "name": "Data Science Fundamentals", "duration": 2, "students": 20, 
             "preferred_slots": ["16:00-18:00"], "weekly_sessions": 1},
            
            # Arts
            {"code": "ART101", "name": "Art Appreciation", "duration": 1, "students": 15, 
             "preferred_slots": ["14:00-16:00"], "weekly_sessions": 1},
            {"code": "MUS101", "name": "Music Theory", "duration": 1, "students": 15, 
             "preferred_slots": ["11:00-13:00"], "weekly_sessions": 1},
        ]
        
        # Assign teachers and create courses
        for course_data in courses:
            # Find suitable teachers
            suitable_teachers = []
            course_name_words = course_data["name"].lower().split()
            
            for teacher, subjects in teacher_objs:
                for subject in subjects:
                    if any(word in subject.lower() for word in course_name_words):
                        suitable_teachers.append(teacher)
                        break
            
            if not suitable_teachers:
                # If no subject match, pick from teachers with lightest schedules
                suitable_teachers = [t[0] for t in sorted(
                    teacher_objs, 
                    key=lambda x: Course.objects.filter(teacher=x[0]).count()
                )]
            
            # Create multiple sessions with different teachers if needed
            sessions_needed = course_data["weekly_sessions"]
            teachers_for_course = random.sample(
                suitable_teachers, 
                min(len(suitable_teachers), sessions_needed)
            )
            
            # If we don't have enough unique teachers, reuse some
            if len(teachers_for_course) < sessions_needed:
                teachers_for_course += [random.choice(suitable_teachers) 
                                      for _ in range(sessions_needed - len(teachers_for_course))]
            
            for i, teacher in enumerate(teachers_for_course):
                Course.objects.create(
                    code=f"{course_data['code']}-{i+1}",
                    name=course_data["name"],
                    duration=course_data["duration"],
                    teacher=teacher,
                    students_enrolled=course_data["students"]
                )
        
        self.stdout.write(self.style.SUCCESS(
            f"Successfully created:\n"
            f"- {Room.objects.count()} rooms\n"
            f"- {Teacher.objects.count()} teachers\n"
            f"- {Course.objects.count()} course instances\n"
            f"All configured for {len(days)} days with {len(time_slots)} time slots each day."
        ))