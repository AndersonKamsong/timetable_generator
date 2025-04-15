# AI Timetable Generator - README

## 📌 Project Overview

This Django application generates optimized university timetables using AI scheduling techniques. It creates conflict-free schedules that respect room capacities, teacher availability, and other constraints while maximizing resource utilization.

Key Features:
- 🏫 Room-based timetable visualization
- 👩🏫 Teacher availability management
- 📚 Course scheduling with multiple constraints
- ⚡ Two scheduling algorithms (constraint-based and greedy fallback)
- 📊 Comprehensive data seeding for testing

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/andersonKamsong/timetable-generator.git
   cd timetable-generator
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

## 🚀 How to Use

### 1. Populate Sample Data
```bash
python manage.py seed_data
```
This creates:
- 10 classrooms/labs
- 20 teachers with varied availability
- 20+ courses with multiple sections

### 2. Run Development Server
```bash
python manage.py runserver
```

### 3. Access the Application
- **Timetable Generator**: http://localhost:8000/timetable/generate/
- **Admin Interface**: http://localhost:8000/admin/

### 4. Generate a Timetable
1. Visit the generation page
2. Enter a timetable name
3. Click "Generate Timetable"
4. View the optimized schedule

## 🔧 Customization Options

### Adjusting Constraints
Modify these files to change scheduling rules:
- `timetable/optimization/constraints.py` - Edit constraint logic
- `timetable/optimization/solver.py` - Change algorithm parameters

### Modifying Sample Data
Edit the seed data in:
- `timetable/management/commands/seed_data.py`

Key parameters to adjust:
- Teacher availability percentages
- Room capacities
- Course durations and frequencies

## 📂 Project Structure

```
timetable_generator/
├── manage.py
├── requirements.txt
└── timetable/
    ├── management/
    │   └── commands/
    │       └── seed_data.py
    ├── migrations/
    ├── templates/
    │   └── timetable/
    │       ├── base.html
    │       ├── generate.html
    │       └── result.html
    ├── optimization/
    │   ├── constraints.py
    │   └── solver.py
    ├── models.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

## ⚙️ Technical Details

**Algorithms Used:**
1. **Constraint Satisfaction** (primary)
   - Uses python-constraint library
   - Respects all hard constraints
2. **Greedy Algorithm** (fallback)
   - Used when constraint solver fails
   - Prioritizes difficult-to-schedule classes

**Constraints Enforced:**
- No teacher double-booking
- Room capacity limits
- Teacher availability
- Course duration requirements

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

---

💡 **Tip**: For production deployment, consider using PostgreSQL for better performance with large datasets and implementing caching for frequently generated timetables.