import re
from collections import defaultdict

class CTTParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {
            "name": "",
            "courses": 0,
            "rooms": 0,
            "days": 0,
            "periods_per_day": 0,
            "curricula": 0,
            "constraints": 0,
            "course_data": [],
            "room_data": [],
            "curricula_data": [],
            "constraints_data": []
        }
        self.parse_file()

    def parse_file(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        # Remove newline characters and filter out empty lines
        lines = [line.strip() for line in lines if line.strip()]

        # Process header information
        self.data["name"] = self._get_value(lines.pop(0), "Name: ")
        self.data["courses"] = int(self._get_value(lines.pop(0), "Courses: "))
        self.data["rooms"] = int(self._get_value(lines.pop(0), "Rooms: "))
        self.data["days"] = int(self._get_value(lines.pop(0), "Days: "))
        self.data["periods_per_day"] = int(self._get_value(lines.pop(0), "Periods_per_day: "))
        self.data["curricula"] = int(self._get_value(lines.pop(0), "Curricula: "))
        self.data["constraints"] = int(self._get_value(lines.pop(0), "Constraints: "))

        # Process sections
        self._parse_section(lines, "COURSES:", self.data["course_data"], self._parse_course)
        self._parse_section(lines, "ROOMS:", self.data["room_data"], self._parse_room)
        self._parse_section(lines, "CURRICULA:", self.data["curricula_data"], self._parse_curriculum)
        self._parse_section(lines, "UNAVAILABILITY_CONSTRAINTS:", self.data["constraints_data"], self._parse_constraint)

    def _get_value(self, line, prefix):
        """Extract the value after a specified prefix."""
        return line[len(prefix):].strip()

    def _parse_section(self, lines, section_header, data_list, parse_fn):
        """Parse a section given its header, list to store results, and parsing function."""
        # Find section header
        if lines.pop(0) != section_header:
            raise ValueError(f"Expected section header '{section_header}' not found.")

        # Parse lines until we encounter the next section or the end marker "END."
        while lines and lines[0] not in {"COURSES:", "ROOMS:", "CURRICULA:", "UNAVAILABILITY_CONSTRAINTS:", "END."}:
            data_list.append(parse_fn(lines.pop(0)))

        if lines and lines[0] == "END.":
            lines.pop(0)

    def _parse_course(self, line):
        """Parse a course entry."""
        parts = line.split()
        course_id, teacher = parts[0], parts[1]
        lectures, min_working_days, students = map(int, parts[2:])
        return {
            "course_id": course_id,
            "teacher": teacher,
            "lectures": lectures,
            "min_working_days": min_working_days,
            "students": students
        }

    def _parse_room(self, line):
        """Parse a room entry."""
        parts = line.split()
        room_id, capacity = parts[0], int(parts[1])
        return {
            "room_id": room_id,
            "capacity": capacity
        }

    def _parse_curriculum(self, line):
        """Parse a curriculum entry."""
        parts = line.split()
        curriculum_id, num_courses = parts[0], int(parts[1])
        member_ids = parts[2:]
        return {
            "curriculum_id": curriculum_id,
            "num_courses": num_courses,
            "members": member_ids
        }

    def _parse_constraint(self, line):
        """Parse a constraint entry."""
        parts = line.split()
        course_id, day, day_period = parts[0], int(parts[1]), int(parts[2])
        return {
            "course_id": course_id,
            "day": day,
            "day_period": day_period
        }

    def get_data(self):
        """Return the parsed data."""
        return self.data

# Example usage:
# parser = CTTParser("comp01.ctt")
# data = parser.get_data()
# print(data)
