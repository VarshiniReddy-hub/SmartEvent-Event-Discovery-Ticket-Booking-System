# SmartEvent – Event Discovery & Ticket Booking System

SmartEvent is a full-stack web application for discovering events and booking tickets online.

Users can register and log in, view available events, book tickets, manage their bookings, access digital tickets with QR codes, and verify tickets. The application also includes notifications and organizer features for managing events.

## Features

### User Authentication

* User registration
* User login
* JWT-based authentication
* Password hashing using bcrypt
* Protected API routes
* User profile
* Automatic authentication using a stored token

### Event Discovery

* View available events
* View individual event details
* Event information includes:

  * Event name
  * Date and time
  * Location
  * Category
  * Ticket price
  * Available tickets

### Ticket Booking

* Select the number of tickets
* Calculate total ticket price
* Confirm bookings
* View booking history
* Cancel confirmed bookings
* Prevent unauthorized users from accessing other users' bookings

### Digital Tickets

* Generate digital tickets for confirmed bookings
* Unique ticket code for every ticket
* QR code generation
* View digital tickets
* Download QR ticket
* Display ticket and booking information

### Ticket Verification

* Verify tickets using the unique ticket code
* Display ticket verification status
* Show booking ID and ticket information
* QR code can be used for ticket verification

### Notifications

* Booking confirmation notifications
* Booking cancellation notifications
* Notification unread count
* Mark notifications as read

### Organizer Features

* Organizer role support
* Organizer event management
* Protected organizer routes

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* bcrypt
* QRCode

### Frontend

* React
* Vite
* JavaScript
* Axios
* React Router
* CSS

### Development Tools

* Visual Studio Code
* Git
* GitHub
* Uvicorn

## Project Structure

```text
SmartEvent-FullStack-main/
│
├── backend/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── bookings.py
│   │   ├── events.py
│   │   ├── notifications.py
│   │   ├── organizer.py
│   │   └── tickets.py
│   │
│   ├── static/
│   │   └── qrcodes/
│   │
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── database.py
│   ├── requirements.txt
│   ├── update_db.py
│   └── update_role.py
│
├── frontend/
│   └── ...
│
├── screenshots/
│   ├── Screenshot (236).png
│   ├── Screenshot (237).png
│   ├── Screenshot (238).png
│   ├── Screenshot (239).png
│   ├── Screenshot (240).png
│   ├── Screenshot (241).png
│   ├── Screenshot (242).png
│   ├── Screenshot (243).png
│   ├── Screenshot (244).png
│   └── Screenshot (245).png
│
├── .gitignore
└── README.md
```

## Backend Setup

Open PowerShell and go to the backend folder:

```powershell
cd "C:\Users\reddy\OneDrive\Desktop\SmartEvent-FullStack-main\backend"
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\activate
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

Start the FastAPI server:

```powershell
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open another PowerShell terminal and go to the frontend folder:

```powershell
cd "C:\Users\reddy\OneDrive\Desktop\SmartEvent-FullStack-main\frontend"
```

Install frontend dependencies:

```powershell
npm install
```

Start the React development server:

```powershell
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

## Application Flow

The main application flow is:

```text
Register
   ↓
Login
   ↓
View Events
   ↓
Select Event
   ↓
Book Tickets
   ↓
Booking Confirmation
   ↓
Generate Digital Ticket
   ↓
QR Code
   ↓
Verify Ticket
```

## API Endpoints

The backend API uses the `/api/v1` prefix.

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
```

### Events

```text
GET /api/v1/events
GET /api/v1/events/{event_id}
```

### Bookings

```text
POST /api/v1/bookings
GET /api/v1/bookings/my-bookings
GET /api/v1/bookings/{booking_id}
PATCH /api/v1/bookings/{booking_id}/cancel
```

### Tickets

```text
POST /api/v1/tickets/booking/{booking_id}
GET /api/v1/tickets/my-tickets
GET /api/v1/tickets/verify/{ticket_code}
```

### Notifications

```text
GET /api/v1/notifications
GET /api/v1/notifications/unread-count
PATCH /api/v1/notifications/{notification_id}/read
```

## Authentication

SmartEvent uses JWT tokens for authentication.

After login, the authentication token is stored on the frontend and automatically sent with protected API requests.

Protected features include:

* My Bookings
* My Tickets
* Ticket Verification
* Notifications
* Booking and cancellation operations

## Booking and Ticket System

When a user books an event, the system creates a booking with:

* Booking ID
* User ID
* Event ID
* Number of tickets
* Total amount
* Booking status
* Booking date

After a confi
