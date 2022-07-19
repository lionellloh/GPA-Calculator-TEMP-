# "GPA CALCULATOR II" by CHRISTIAN RUBIO
# Jul 17, 2022
# COMP 163-001 | Professor Leflore

# This GPA calculator is created in the pursuit of creating a user-friendly, dynamic calculator that considers for different semesters,
# different GPA types (semester, major, honors, regular), allows for stopping class or semester submittal at designated times, and automatically detects
# if classes are retaken by reading the class name. I strove as well to restrain python concepts to only those introduced within chapters
# 1-5, and avoiding concepts such as functions. 

# Fundamentally, the program organizes courses in dictionaries, and keys are course names, while values are lists containing course attributes. This
# is used for easy class organization and computation of different GPAs by separating by attribute or dictionary.

print("Welcome to the [UN]official, dynamic GPA NCAT GPA calculator!")

# The "courses" dictionary is setup to emulate the classes that contribute towards the GPA that is displayed on the NCAT student
# academic transcript
courses = dict()
# The "semester_gpa_archive" is used to contain all semester GPAs for output at the end of the program.
semester_gpa_archive = dict()

# The "courses_duplicate" dictionary is setup to only include duplicate classes that do not contribute towards the GPA shown on the NCAT
# student transcript, and instead only contributes towards the honors GPA calculation.
courses_duplicate = dict()

# The "grade_key" dictionary is reused from my previous GPA calculator to once again convert letter grades to grades on a 0-4 scale according to the NCAT grade scale. 
grade_key = {
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'F': 0.0,
}

semester_sentinel = ''
semester_count = 1
course_sentinel = ''

while semester_sentinel != 'N':
    course_sentinel = ''
    while course_sentinel != 'N':
        # The course_attributes list is established within the while loop to allow for a new, clear list of attributes for each iteration and course
        course_attributes = list()

        # str.upper is used across the program to standardize text in upper-case for comparisons (such as in if-else branches).
        course_name = str.upper(input(f"Enter your course name: "))

        # the following if-else branch detects for reused names, and an attribute is assigned based upon whether or not the name is reused. This is implemented for the purpose of later organizing classes to separate dictionaries for calculation
        # of the honors or regular GPA. 
        if course_name in courses:
            course_dupli = 'Duplicate'
        else:
            course_dupli = 'Non-duplicate'


        # the following prompt and if-elif-else branch are used to determine whether or not the course is related to the major discipline (such as COMP & ELEN classes for a Computer Engineering degree)
        # The course_major question is in a while loop, as a specific Yes or No input is required to the Yes or No question. Thus, any other input is an error. It can only be broken out by a sentinel value
        # denoted 'End', and is only assigned when a proper answer is given.
        course_major_sentinel = ''
        while course_major_sentinel != 'End':
            course_major = str.upper(input(f"Is {course_name} related to your major discipline? Y or N: "))
            if course_major == 'Y':
                course_major = 'Major'
                course_major_sentinel = 'End'
            elif course_major == 'N':
                course_major = 'Non-Major'
                course_major_sentinel = 'End'
            else:
                course_major_sentinel = 'Error'
                print("INVALID CHARACTER SUBMISSION, TRY AGAIN")
                continue

        # isdigit() is a native python function that checks for if the value of a variable includes digits, and returns a variable based on the value (if variable includes digit, value returned is "True". if not, value returned is "False")
        # while loop to check for inputs on a standard 4.00 scale as used on NC A&T, as well as according to the limits of the letter grade.
        course_grade_sentinel = ''
        while course_grade_sentinel != 'End':
            course_grade = str.upper(input(f"Enter grade for {course_name} as grade points or a letter grade: "))
            if course_grade.isdigit() and float(course_grade) <= 4 and float(course_grade) >= 0:
                course_grade = float(course_grade)
                course_grade_sentinel = 'End'
            elif course_grade in grade_key:
                course_grade = grade_key[course_grade]
                course_grade_sentinel = 'End'
            else:
                couse_grade_sentinel = 'Error'
                print("Invalid grade submitted. Try Again.")
                continue

        course_hours = float(input(f"Enter the credit hours for {course_name} : "))

        # The following block of print statements and the if-else branch using the "course_confirm" variable are created to allow the user to confirm their class information,
        # and allow for resubmittal in the case of the user noticing any information they may have submitted by accident. 
        print(f'\n{course_name} has been entered with the following attributes: ')
        print(f'Grade: {course_grade:.2f}')
        print(f'Credit Hours: {course_hours:.2f} ')
        print(f'{course_major} discipline course\n')
        print("Is this correct?\n")
        course_confirm = str.upper(input("Enter \'Y\' to continue, Enter \'N\' to re-enter course: "))
        if course_confirm == 'N':
            print(f'{course_name} information will be reset for re-entry.')
            continue
        elif course_confirm == 'Y':
            print(f"{course_name} confirmed.")
        else:
            print(f'Invalid input, {course_name} will be reset.')

        # The following block of code is written with the format of "course_attributes.append(attribute)" to organize information into a list. The
        # list is paired with a dictionary key (denoted by course_name) as a value to create a key:value pair entry for the class.
#         course_major.course_major = course_major 
#         course_major.set_major(course_major) 
        
        course_attributes.append(course_major)
        course_attributes.append(course_grade)
        course_attributes.append(course_hours)
        course_attributes.append(course_dupli)
        course_attributes.append(semester_count)

        # The following if-elif branch determines if a class is retaken or not. If retaken, the original course is removed off the main 'courses' dictionary
        # and reassigned towards the duplicates dictionary. If not retaken, the course is assigned to the regular courses dictionary
        if course_dupli == 'Duplicate':
            courses_duplicate[course_name] = courses[course_name]
            del courses[course_name]
            courses[course_name] = course_attributes
        elif course_dupli == 'Non-duplicate':
            courses[course_name] = course_attributes
        
        # The following start_word variable and input allow the user to end submittal of course information when desired.
        user_char_input = str.upper(input("Enter \'N\' to end this semester. Enter any other character to continue this semester: "))
        if user_char_input == 'N': 
            break 
    
    # This block of code runs in the outer loop, and computes the semester gpa and immediately returns it to the user. 
    # This gpa is then archived to the "semester_gpa_archive" dictionary for printing on completion of the program
    semester_qlty_pts = 0
    semester_cred_hrs = 0
    semester_gpa = 0
    for names in courses:
        if courses[names][4] == semester_count:
            semester_qlty_pts += float(courses[names][1]) * float(courses[names][2])
            semester_cred_hrs += float(courses[names][2])
    # Using the if statement here prevents a divide-by-zero error
    if semester_cred_hrs != 0:
        semester_gpa = semester_qlty_pts / semester_cred_hrs
        print(f'Your semester GPA is {semester_gpa:.2f}')
    semester_gpa_archive[semester_count] = semester_gpa
    semester_count += 1
    semester_sentinel = str.upper(input("Enter \'N\' to stop. Enter any other character to add another semester: "))

# Establishes variable definition outside of for loops to allow for incrementation. 
qlty_pts_total = 0
cred_hour_total = 0
major_qlty_pts = 0
major_cred_hour = 0
hnrs_qlty_pts = 0
hnrs_cred_hours = 0

# The following "for" loop block arranges the classes for the regular GPA, computing for the total quality points (calculated by class grade * credit hours) 
# and total credit hours to then allow to compute GPA (total quality points / total credit hours)
for names in courses:
    # The following if branch detects a major discipline course, and if detected, will add the quality points and credit hours to a separate
    # set of variables to explicitly only compute Major GPA
    if courses[names][0] == 'Major':
        major_qlty_pts += float(courses[names][1]) * float(courses[names][2])
        major_cred_hour += float(courses[names][2])
    
    qlty_pts_total += float(courses[names][1]) * float(courses[names][2])
    cred_hour_total += float(courses[names][2])

# the for loop takes courses exempt from the GPA and adds them to the Honors GPA, which computes all classes, even those retaken
for names in courses_duplicate:
    hnrs_qlty_pts = (float(courses_duplicate[names][1]) * float(courses[names][2]))
    hnrs_cred_hours = float(courses_duplicate[names][2])

# The followinng if-else branch prevents a division-by-zero runtime error, as the Major GPA is only calculated if there are more than zero
# credit hours of classes related to a major discipline. 
if major_cred_hour!= 0:
    majorGPA = major_qlty_pts / major_cred_hour
else:
    majorGPA = 0

# The honors GPA components are incremented with the non-duplicate/retaken classes, thus taking into account every entered class
# and correctly calculating the Honors GPA
hnrs_qlty_pts += qlty_pts_total 
hnrs_cred_hours += cred_hour_total
hnrsGPA = hnrs_qlty_pts / hnrs_cred_hours

# This is the calculation of the general GPA (total quality points / credit hours), which includes all but exempt classes
GPA = qlty_pts_total / cred_hour_total

# The following if-else branch allows for better user understandability, so that a 0.00 major GPA can be explained in situations
# where major discipline credits were not taken.
if majorGPA == 0:
    print("\nMajor GPA unable to be computed due to lack of major discipline classes.")
else:
    print(f'\nYour major GPA is {majorGPA:.2f}')

# from here on, all GPAs are printed to a standard precision of two decimal points as displayed on the NC A&T Transcript
print(f'Your honors GPA is {hnrsGPA:.2f} ')
print(f'Your current GPA is: {GPA:.2f}\n')

# The following for loop iterates through the semester GPA archive dictionary to summarize semester GPAs
# for readability.
print("Your GPA by semester: \n")
for gpas in semester_gpa_archive:
    print(f'Semester {gpas} GPA: {semester_gpa_archive[gpas]:.2f} ')
print()
