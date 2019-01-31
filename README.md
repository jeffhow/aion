# Aion

Aion is a scheduling application for schools created with Python and Django.

Schools often share resources between classrooms. We believe scheduling and 
reserving  resources like computer labs and laptop carts is easier with a 
block-based tool like Aion.

# Getting Started

## Installation and requirements
Aion requires Python 3.6+, PostgreSQL, and OS-specific dependancy tools.

## Progress
1. Blank Cloud9 workspace created
2. Installed Python 3.6, VirtualEnv, and Django 2.1
3. Created Django Project (Aion)
4. Custom Cloud9 Runner (Command: aion/aion/settings.py | Runner: Aion Runner.run)
5. Created Django App (reservations)
8. Installed Crispy Forms
9. Configured Crispy Forms for Bootstrap4
10. Got the new blg-Admin feature working
11. Created decorator permission for school-admin
12. Built a signup module
13. Wrote all the main functionality
14. Wrote all the building admin functionaility
15. Created custom forms (extended crispy forms)
16. Created announcement feature for blg admins

### Todo
2. Complete Index Page
4. Complete email feature for super admins
5. Add bulk reservation feature
6. Research cleanup script for database (inactive users and resources or blocks)
7. Finish CSS
8. Research email options
9. Deploy to Heroku

### Changes in v2.0
1. Model: Resources replaces Rooms FK: school
2. Model: TimeBlocks added FK: school
3. Model: Schools added
4. Profile: Location FK: school
4. Announcements feature
5. School admin level
6. Super admin level
7. Bulk reservations

#### Built as a learning project by [Jeff.how](http://jeff.how)
[jeff@jeff.how](mailto:jeff.how)