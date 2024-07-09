#!/usr/bin/env python3

class Course:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} [{self.duration}] ({self.link})"

courses = [
    Course("Linux", 15, "https://hack4u.io/Linux"),
    Course("Personalizacion", 3, "https://hack4u.io/Personalizacion"),
    Course("Hacking", 53, "https://hack4u.io/Hacking" )
]

def list_courses():
    for course in courses:
        print(course)


def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course
        
    return None