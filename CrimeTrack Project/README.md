<<<<<<< HEAD
# CrimeTrack – Citizen Crime Complaint Intake & Tracking System

CrimeTrack is a modern, full-stack web application designed to empower citizens to report crimes and allow law enforcement administrators to track, manage, and analyze these reports effectively.

## 🚀 Features

### For Citizens
- **Secure Authentication**: JWT-based registration and login.
- **Incident Reporting**: Submit detailed reports with titles, descriptions, and categories.
- **Geospatial Integration**: Pinpoint locations using an interactive Google Map.
- **Evidence Upload**: Attach photos or documents to reports.
- **Real-time Tracking**: Monitor the status of filed complaints with a visual timeline.
- **Search & Filter**: Easily find past reports by ID or title.

### For Administrators
- **Comprehensive Dashboard**: View all reported crimes in a centralized table.
- **Status Management**: Update reports through four stages: *Submitted*, *Under Review*, *Action Taken*, and *Closed*.
- **Audit Trail**: Add internal remarks and track the history of status changes.
- **Advanced Analytics**: Interactive charts (Doughnut & Bar) for status distribution and crime categories.
- **Search & Filter**: Powerful tools to manage large volumes of data.

## 🛠️ Tech Stack

- **Frontend**: Clean HTML5, Vanilla CSS3 (with Glassmorphism), and Modern JavaScript (ES6+).
- **Backend**: Python Flask (Modular REST API).
- **Database**: Supabase (PostgreSQL) for relational data and real-time features.
- **Auth**: Supabase Auth (JWT).
- **Storage**: Supabase Storage for evidentiary files.
- **Maps**: Google Maps JS API.
- **Charts**: Chart.js.

## 📂 Project Structure

```text
├── backend/
│   ├── app/
│   │   ├── admin.py           # Admin management routes
│   │   ├── auth.py            # Authentication logic
│   │   ├── complaints.py      # Complaint CRUD operations
│   │   ├── main.py            # Flask app initialization
│   │   └── supabase_client.py # Client connectivity
│   ├── config.py              # Environment configuration
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── assets/
│   │   ├── css/style.css      # Custom design system
│   │   └── js/                # utils.js & auth.js
│   ├── index.html             # Landing & Auth
│   ├── citizen.html           # Citizen dashboard
│   ├── admin.html             # Admin portal
│   └── track.html             # Tracking & Timeline
├── supabase_schema.sql        # Database initialization script
├── setup_instructions.md      # Detailed installation guide
└── README.md                  # Project overview
```

## 🔧 Installation

For detailed setup instructions, please refer to [setup_instructions.md](setup_instructions.md).

1. Initialize your Supabase project and run `supabase_schema.sql`.
2. Configure your `.env` in the `backend/` folder.
3. Install Python requirements: `pip install -r backend/requirements.txt`.
4. Replace the Google Maps API key in `frontend/citizen.html`.
5. Run the backend: `python -m backend.app.main`.

## 🛡️ Security

- **Role-Based Access Control (RBAC)**: Enforced both in the Flask API and via Supabase Row Level Security (RLS).
- **Data Protection**: 256-bit encryption for data at rest (handled by Supabase).
- **Input Validation**: Sanitization and validation for all API inputs.

---

Built with ❤️ for a safer community.
=======
# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
>>>>>>> b43a684d715cc2a6d89a5a7d9fd12a7a37c2f451
