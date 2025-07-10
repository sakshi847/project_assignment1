# project_assignment1
# Smart Registration Portal

A Django-based OTP-authenticated student registration system built for school exam enrollments. This system allows parents to register multiple students with secure mobile OTP verification, fee calculation, payment simulation, and a dashboard view.

---

##  Features

- OTP-based login for parents (with 45-second expiry and 3 resend limits)
- Mobile number validation and blocking for misuse (after 3 attempts or resends)
- Parent + Multiple Student registration
- Auto fee calculation with tax
- Fake payment gateway simulation
- Post-payment dashboard view for registered students
- Responsive UI using Bootstrap 5
- Session management and validations
- Duplicate prevention and validation
- SQLite Database + Django Admin enabled

---

## Tech Stack

- Python 3.12
- Django 5.2
- SQLite (default)
- Bootstrap 5
- HTML5/CSS3
- GitHub (for version control)

---

## 📁 Folder Structure

smart_registration_portal/
├── accounts/ # OTP login logic and templates
├── registration/ # Parent + Student form handling
├── studentform/ # Core registration models and logic
├── payment/ # Payment simulation and success page
├── templates/ HTML templates
├── static/ # Logo
├── db.sqlite3 # Database file
├── manage.py

### 1. Clone the Repository

```bash
git clone https://github.com/sakshi847/project_assignment1.git
cd project_assignment1

