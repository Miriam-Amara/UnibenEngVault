# UnibenEngVault 📚

**UnibenEngVault** is a centralized academic platform designed for Engineering students at the **University of Benin**.  
It provides easy access to course materials, tutorials, and academic resources across all levels (100–500).  
The platform aims to reduce fragmentation of learning resources by providing a single, structured hub for students and lecturers.  

---

## 🚀 Features (Work in Progress)

- **User Authentication**  
  - Register, login, and session management for students and admins.  

- **Student Dashboard**  
  - View course outlines.  
  - Access and download course files.  
  - Links to tutorials.  
  - Upload course materials.  
  - Report broken or incorrect files.  

- **Admin Dashboard**  
  - Manage courses and departmental structures.  
  - Upload, update, and delete course outlines, tutorials, and files.  
  - Monitor downloads and control access.  
  - View feedback, notifications, and help reports.  

- **General**  
  - Organized by level (100–500) and department.  
  - Support for shared and general courses.  
  - Notifications and student support system.  

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask), SQLAlchemy ORM  
- **Database:** PostgreSQL  
- **Storage:** AWS S3 (for course materials)  
- **Deployment:** Docker + AWS EC2 (planned)  
- **Version Control:** Git & GitHub  

---

## 📂 Project Structure (in progress)

unibenengvault/
├── api/
│ └── v1/
│ ├── auth/ # Authentication & authorization logic
│ ├── views/ # API route definitions
│ └── ...
├── models/ # Database models
├── tests/ # Unit tests
├── README.md
└── requirements.txt


---

## ⚡ Getting Started

### Prerequisites
- Python 3.10+  
- PostgreSQL  
- Virtual environment tool (venv or pipenv)  

### Installation

```bash
# Clone repository
git clone https://github.com/<Miriam-Amara>/unibenengvault.git
cd unibenengvault

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start development server
python3 -m api.v1.app

The app will be available at http://127.0.0.1:5000/.

---
## ✅ Roadmap

- Complete authentication (login, logout, session storage).

- Build student features (view courses, download/upload files).

- Implement admin dashboard features.

- Connect to AWS S3 for file storage.

- Dockerize and deploy to AWS EC2.

---
## 🧪 Testing

Run unit tests with:

pytest