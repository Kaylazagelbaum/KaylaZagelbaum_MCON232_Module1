# reads in all records
def read_lines(filename):
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []


# normalizes each line
def normalize_line(line):
    line = line.replace(': ', ':')
    line = line.replace('GRADE', 'grade')
    line = line.replace('PROF:', 'prof:')
    line = line.replace('grade =', 'grade=')
    line = line.replace('grade= ', 'grade=')
    return line

#parses for invalid records
def parse_record(clean_line):
    if not clean_line:
        return None

    parts = [part.strip() for part in clean_line.split('|')]
    parts = [p for p in parts if p]

    if len(parts) != 4:
        return None

    student_name, age_str, professor, grade_str = parts

    try:
        age = int(age_str)
        if not (15 <= age <= 99):
            return None
    except ValueError:
        return None

    if not professor.startswith('prof:'):
        return None

    if not grade_str.startswith('grade='):
        return None

    try:
        grade = int(grade_str.split('=')[1])
        if not (0 <= grade <= 100):
            return None
    except (ValueError, IndexError):
        return None

    record_list = [student_name, str(age), professor, f"grade={str(grade)}"]
    record_str = '|'.join(record_list)
    return record_str

# combines read_lines, normalize_line, and parse_record
def combine_functions():
    raw_lines_list = read_lines('raw_records.txt')

    global valid_records, invalid_lines
    valid_records = []
    invalid_lines = []

    for line in raw_lines_list:
        clean_line = normalize_line(line)
        rec = parse_record(clean_line)
        if rec is None:
            invalid_lines.append(line)
        else:
            valid_records.append(rec)
    return (f"Valid: {valid_records}, \nInvalid: {invalid_lines}")


if __name__ == '__main__':
    print(combine_functions())

# writes records to text files
def write_records(record, filename):
    with open(filename, 'w') as f:
       for r in record:
           f.write(f"{r}\n")

write_records(valid_records, 'clean_records.txt')
write_records(invalid_lines, 'invalid_records.txt')

# calculates the average grade for the class
def average_grade(records):
    total = 0
    count = 0
    for r in records:
        sections = r.split('|')
        name, age, professor, grade = sections
        grade_num = int(grade.split('=')[1])
        total += grade_num
        count += 1
    average = total / count
    return average

# calculates the number of students and average grade per professor
def professor_summary(records):
    # return (professor_last_name, num_students, average_grade)
    summaries = []
    professors = []

    for r in records:
        sections = r.split('|')
        name, age, professor, grade = sections
        prof_name = professor.split(':')[1].lower()
        if prof_name not in professors:
            professors.append(prof_name)

    for prof_name in professors:
        num_students = 0
        total_grade = 0

        for r in records:
            sections = r.split('|')
            name, age, professor, grade = sections
            this_prof = professor.split(':')[1].lower()
            grade_num = int(grade.split('=')[1])
            if this_prof == prof_name:
                num_students += 1
                total_grade += grade_num
        average_grade = total_grade / num_students
        summaries.append((prof_name, num_students, average_grade))

    return summaries, professors

summaries, professors = professor_summary(valid_records)

# calculates top student per professor
def top_student_per_prof(records, professors):
    # (professor, student, grade) for each professor
    results = []
    for prof in professors:
        top_student = ""
        top_grade = 0
        for r in records:
            sections = r.split('|')
            name, age, professor, grade = sections
            grade_num = int(grade.split('=')[1])
            this_prof = professor.split(':')[1].lower()
            if this_prof == prof:
                if grade_num > top_grade:
                    top_student = name
                    top_grade = grade_num
        results.append((prof, top_student, top_grade))
    return results

# combines average_grade, professor_summary, and top_student_per_prof
def write_report(filename):

    valid_count = 0
    invalid_count = 0
    for r in valid_records:
        valid_count += 1
    for l in invalid_lines:
        invalid_count += 1
    class_average = average_grade(valid_records)
    summaries, professors = professor_summary(valid_records)
    top_students = top_student_per_prof(valid_records, professors)

    with open(filename, 'w') as f:
        f.write(f"Total Valid Records:\n")
        for r in valid_records:
            f.write(f"{r}\n")
        f.write(f"Total Invalid Records:\n")
        for l in invalid_lines:
            f.write(f"{l}\n")
        f.write(f"Class Average: {class_average} \n")
        f.write(f"Professor Summaries:\n")
        for s in summaries:
            f.write(f"{s}\n")
        f.write(f"Top Student Per Professor:\n")
        for t in top_students:
            f.write(f"{t}\n")

write_report('report.txt')








