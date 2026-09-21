# 🌾 AgriAI

### AI-Powered Digital Farm History

AgriAI is a digital farm history platform that helps farmers record, organize, search, and understand their farming data.

Instead of keeping crop activities, input usage, expenses, and harvest information across notebooks and separate records, AgriAI stores everything in a structured digital history and allows farmers to ask questions using natural language.

---

## 🎯 Problem Statement

**PRARAMBHA 2.0 — PS-02: AI-Powered Digital Farm History**

Farmers generate valuable information throughout every farming cycle:

- Field preparation
- Crop information
- Irrigation
- Fertilizer and input usage
- Expenses
- Harvest information
- Seasonal records

These records are often scattered across notebooks, bills, photographs, and personal records.

AgriAI provides a centralized digital system where this information can be stored chronologically and queried using AI.

---

# 🚀 Key Features

## 1. Digital Farm Records

AgriAI organizes farm information using:

```text
User
 └── Farm
      └── Field
           └── Season
                └── Crop
                     ├── Activities
                     ├── Inputs
                     ├── Expenses
                     └── Harvests
2. Farm Management

Farmers can manage:

Farm name
Location
Total area
Area unit
Multiple farms
3. Field Management

Each farm can contain multiple fields.

Each field stores:

Field name
Area
Associated farm
4. Season Management

Each field can have multiple seasons.

Each season stores:

Season name
Start date
End date
5. Crop Management

Each season can contain multiple crops.

Crop records include:

Crop name
Variety
Sowing date
Harvest date
6. Activity Tracking

Farmers can record activities such as:

Irrigation
Fertilizer application
Field preparation
Weeding
Other farming activities
7. Input Tracking

Inputs include:

Input name
Input type
Quantity
Unit
Application date
Cost
Description

Example:

Urea
50 kg
10 July 2026
₹2500
8. Expense Tracking

Expenses can be categorized as:

Labour
Tractor
Seeds
Transport
Irrigation
Fertilizer
Pesticide
Other

Each expense stores its amount, date, category, and description.

9. Harvest Tracking

Harvest records contain:

Harvest date
Quantity
Unit
Selling price
Description
10. Complete Farm History

AgriAI combines:

Activities
Inputs
Expenses
Harvests

into a chronological farm timeline.

History can be filtered by:

Field
Season
Crop
Record type
11. AI Farm Assistant 🤖

Farmers can ask questions in natural language.

Examples:

How much urea did I use?

How much fertilizer did I use in total?

How much did I spend on wheat?

How much did I spend on labour?

What activities were performed on my wheat crop?

What was my wheat harvest?

How much revenue did I get from wheat?

How much pesticide did I use?
12. Evidence-Based Answers

AgriAI does not only return an AI-generated answer.

It also provides the farm records used as supporting evidence.

Question
   ↓
Relevant Farm Records
   ↓
AI Answer
   ↓
Supporting Evidence

This makes the response traceable and easier to verify.

13. Secure User Data

AgriAI uses JWT authentication.

Each authenticated user can access only their own farm records.

🏗️ System Architecture
                 ┌──────────────────────┐
                 │      Android App     │
                 │      Java + XML      │
                 └──────────┬───────────┘
                            │
                       REST / HTTPS
                            │
                            ▼
                 ┌──────────────────────┐
                 │   FastAPI Backend    │
                 │   Python + FastAPI   │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │ PostgreSQL │ │   History  │ │ Gemini AI  │
      │  Database  │ │ Retrieval  │ │   Engine   │
      └────────────┘ └────────────┘ └────────────┘
🧠 AI Query Architecture
Farmer Question
      │
      ▼
JWT Authentication
      │
      ▼
Identify User
      │
      ▼
Retrieve Farm Records
      │
      ├── Field
      ├── Season
      ├── Crop
      ├── Activities
      ├── Inputs
      ├── Expenses
      └── Harvests
      │
      ▼
Build Farm Context
      │
      ▼
Gemini AI
      │
      ▼
Generate Answer
      │
      ▼
Retrieve Supporting Evidence
      │
      ▼
Answer + Evidence

The AI is instructed to use the supplied farm records rather than inventing farm information.

🛠️ Technology Stack
Android
Java
XML
Android SDK
Material UI
Retrofit
Gson
ViewModel
Repository architecture
Backend
Python
FastAPI
Uvicorn
SQLAlchemy
Async SQLAlchemy
PostgreSQL
asyncpg
Pydantic
JWT
OAuth2
Passlib / bcrypt
AI
Google Gemini API
google-genai
Development
Git
GitHub
PostgreSQL
Android Studio
Render
📁 Project Structure
AgriAI/
│
├── README.md
│
├── android/
│   └── Android Application
│
└── backend/
    │
    ├── app/
    │
    ├── routers/
    │   ├── auth.py
    │   ├── farms.py
    │   ├── fields.py
    │   ├── seasons.py
    │   ├── crops.py
    │   ├── activities.py
    │   ├── inputs.py
    │   ├── expenses.py
    │   ├── harvests.py
    │   ├── history.py
    │   └── query.py
    │
    ├── services/
    │   ├── user.py
    │   ├── history.py
    │   └── ai.py
    │
    ├── database.py
    ├── dependency.py
    ├── hash.py
    ├── jwt_handling.py
    ├── main.py
    ├── models.py
    ├── schema.py
    └── requirements.txt
🗄️ Database Structure
User
 │
 └── Farm
      │
      └── Field
           │
           └── Season
                │
                └── Crop
                     │
                     ├── Activity
                     │
                     ├── Input
                     │
                     ├── Expense
                     │
                     └── Harvest
User
id
username
email
password
Farm
id
user_id
name
location
total_area
area_unit
created_at
Field
id
farm_id
name
area
Season
id
field_id
name
start_date
end_date
Crop
id
season_id
name
variety
sowing_date
harvest_date
Activity
id
crop_id
activity_type
activity_date
description
Input
id
crop_id
input_name
input_type
quantity
unit
application_date
cost
description
Expense
id
crop_id
expense_type
amount
expense_date
description
Harvest
id
crop_id
harvest_date
quantity
unit
selling_price
description
🔐 Authentication

AgriAI uses JWT-based authentication.

Register
POST /users/

Example:

{
  "username": "farmer1",
  "email": "farmer@example.com",
  "password": "password123"
}
Login
POST /users/login

Response:

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}

Protected requests use:

Authorization: Bearer JWT_TOKEN
📡 API Endpoints
Authentication
POST /users/
POST /users/login
POST /users/token
Farms
GET    /farms/
POST   /farms/
GET    /farms/{farm_id}
PUT    /farms/{farm_id}
DELETE /farms/{farm_id}
Fields
GET    /fields/farm/{farm_id}
POST   /fields/
GET    /fields/{field_id}
PUT    /fields/{field_id}
DELETE /fields/{field_id}
Seasons
GET    /seasons/field/{field_id}
POST   /seasons/
GET    /seasons/{season_id}
PUT    /seasons/{season_id}
DELETE /seasons/{season_id}
Crops
GET    /crops/season/{season_id}
POST   /crops/
GET    /crops/{crop_id}
PUT    /crops/{crop_id}
DELETE /crops/{crop_id}
Activities
POST   /activities/
GET    /activities/crop/{crop_id}
GET    /activities/{activity_id}
PUT    /activities/{activity_id}
DELETE /activities/{activity_id}
Inputs
POST   /inputs/
GET    /inputs/crop/{crop_id}
GET    /inputs/{input_id}
PUT    /inputs/{input_id}
DELETE /inputs/{input_id}
Expenses
POST   /expenses/
GET    /expenses/crop/{crop_id}
GET    /expenses/{expense_id}
PUT    /expenses/{expense_id}
DELETE /expenses/{expense_id}
Harvests
POST   /harvests/
GET    /harvests/crop/{crop_id}
GET    /harvests/{harvest_id}
PUT    /harvests/{harvest_id}
DELETE /harvests/{harvest_id}
Farm History
GET /history/
GET /history/crop/{crop_id}

Optional filters:

field_id
season_id
crop_id
record_type

Example:

GET /history/?crop_id=1
AI Query
POST /query/

Request:

{
  "question": "How much fertilizer did I use on wheat?"
}

Response:

{
  "question": "How much fertilizer did I use on wheat?",
  "answer": "You used 75 kg of fertilizer on wheat.",
  "evidence": [
    {
      "type": "input",
      "name": "DAP",
      "quantity": 25,
      "unit": "kg",
      "date": "2026-06-25",
      "description": "DAP applied during early crop growth"
    }
  ]
}
📱 Android Application Flow
Login
  │
  ▼
Farm
  │
  ▼
Field
  │
  ▼
Season
  │
  ▼
Crop
  │
  ├── Activities
  ├── Inputs
  ├── Expenses
  ├── Harvest
  └── Complete History

The Complete History screen provides a chronological view of farming records.

Filters:

Field
Season
Crop
Record Type
🌾 Example Farm History
Wheat Field A
│
└── Kharif 2026
     │
     └── Wheat
          │
          ├── 10 Jun
          │    Tractor Expense
          │
          ├── 25 Jun
          │    DAP - 25 kg
          │
          ├── 10 Jul
          │    Urea - 50 kg
          │
          ├── 12 Jul
          │    Labour Expense
          │
          ├── 15 Jul
          │    Irrigation
          │
          └── Harvest
               18 quintal
💻 Backend Installation
Requirements
Python 3.11+
PostgreSQL
Git
Clone Repository
git clone https://github.com/HARSHADDESAI2236/AgriAI.git
cd AgriAI
Enter Backend
cd backend
Create Virtual Environment
Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
Linux / macOS
python3 -m venv venv
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
🐘 PostgreSQL Setup

Create a PostgreSQL database:

AgriAi

Example connection:

postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/AgriAi
⚙️ Environment Variables

Create:

.env

inside the backend directory.

Example:

DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/AgriAi
SECRET_KEY=YOUR_SECRET_KEY
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
⚠️ Important

Never commit .env to GitHub.

Never expose:

Gemini API keys
Database passwords
JWT secrets
Production credentials
▶️ Run Backend

From the backend directory:

uvicorn main:app --reload

API:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs
📱 Android Local Development

For a physical Android phone, use the computer's local network IP.

Example:

http://192.168.x.x:8000/

The phone and computer must be connected to the same network.

For Android Emulator:

http://10.0.2.2:8000/

Do not use:

http://127.0.0.1:8000/

from a physical phone.

☁️ Production Deployment

Planned production architecture:

Android App
     │
     │ HTTPS
     ▼
Render FastAPI
     │
     ├──────────────► PostgreSQL
     │
     └──────────────► Gemini API
Render Backend

Build command:

pip install -r requirements.txt

Start command:

uvicorn main:app --host 0.0.0.0 --port $PORT

Required environment variables:

DATABASE_URL
SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
GEMINI_API_KEY

After deployment, update the Android Retrofit base URL to the production HTTPS API.

🧪 Testing Checklist
Backend
 Register user
 Login
 JWT authentication
 Create farm
 Create field
 Create season
 Create crop
 Add activity
 Add input
 Add expense
 Add harvest
 View history
 Filter history
 AI query
 Evidence returned
 User data isolation
Android
 Login
 Token persistence
 Farm loading
 Field loading
 Season loading
 Crop loading
 Activity CRUD
 Input CRUD
 Expense CRUD
 Harvest CRUD
 Complete history
 History filters
 AI query
 Evidence display
 Loading states
 Empty states
 Error handling
Final Demo
 Backend deployed
 Database connected
 Gemini configured
 HTTPS working
 Android connected to production API
 APK tested
 GitHub updated
 Demo video tested
 Submission links verified
🎥 Suggested Demo Flow

A simple demonstration can follow this sequence:

1. Login
      ↓
2. Open Farm
      ↓
3. Select Field
      ↓
4. Select Season
      ↓
5. Open Wheat Crop
      ↓
6. Show Activities
      ↓
7. Show Inputs
      ↓
8. Show Expenses
      ↓
9. Show Harvest
      ↓
10. Open Complete History
      ↓
11. Ask AI Question
      ↓
12. Show AI Answer
      ↓
13. Show Supporting Evidence

Example final query:

How much did I spend on wheat?

Follow with:

What activities were performed on my wheat crop?

Then show the supporting records.

🎯 Evaluation Alignment
Evaluation Area	AgriAI
Retrieval Accuracy	Structured farm record retrieval
Organization Quality	Farm → Field → Season → Crop hierarchy
Natural-Language Query	Gemini-powered AI queries
Evidence Traceability	Supporting source records
Response Usefulness	Quantities, dates, costs and context
Chronological Organization	Unified farm timeline
Data Security	JWT + user-specific records
🔮 Future Enhancements

Potential future features:

Voice-based farm queries
Marathi/Hindi regional language support
OCR for bills and documents
Weather history
Season comparison
Crop performance analytics
Yield trend analysis
Cost vs revenue analysis
Automated farm reports
Offline data entry and synchronization
More advanced retrieval and RAG
AI-powered farming insights
👥 Team

Project: AgriAI
Problem Statement: PS-02 — AI-Powered Digital Farm History
Hackathon: PRARAMBHA 2.0
Domain: AgriTech

📄 License

This project was developed as a hackathon prototype.


This version is suitable as the **root `README.md` for the AgriAI GitHub repository** and keeps the focus on the actual project rather than the development process.

Would you like the README tailored for a hackathon submission or a production-ready open-source project?
