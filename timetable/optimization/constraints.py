def no_teacher_overlap(courses, assignments):
    """Ensure no teacher is scheduled for two courses at the same time"""
    teacher_slots = {}
    for course, (room, day, slot) in assignments.items():
        teacher = course.teacher
        key = (day, slot)
        if teacher not in teacher_slots:
            teacher_slots[teacher] = set()
        if key in teacher_slots[teacher]:
            return False
        teacher_slots[teacher].add(key)
    return True

def room_capacity_check(courses, assignments):
    """Ensure room capacity is sufficient for each course"""
    for course, (room, day, slot) in assignments.items():
        if course.students_enrolled > room.capacity:
            return False
    return True

def teacher_availability(courses, assignments):
    """Check if teachers are available at scheduled times"""
    for course, (room, day, slot) in assignments.items():
        teacher = course.teacher
        if (day, slot) not in teacher.availability:
            return False
    return True