# QuickAid - Emergency First Aid Application

## Application Structure

This project now has two versions:

### 1. Web Application (React + Python Flask Backend)
- **Frontend**: React with Vite, TypeScript, TailwindCSS
- **Backend**: Python Flask API
- **Database**: Supabase (PostgreSQL) or in-memory storage

### 2. Android Application (Java)
- Native Android app in the `app/` directory
- Requires Android Studio and Java SDK to build

## Quick Start - Python Backend + React Frontend

### Option A: Using the provided run script
```bash
chmod +x run.sh
./run.sh
```

### Option B: Manual setup

1. **Install Python dependencies:**
```bash
pip3 install --break-system-packages flask flask-cors
```

2. **Start the Python backend:**
```bash
cd backend
PORT=3001 python3 app.py
```

3. **Start the React frontend (in a new terminal):**
```bash
npm install
npm run dev
```

4. **Or build for production:**
```bash
npm run build
npm run preview
```

## API Endpoints

The Python Flask backend provides these endpoints:

### Health Check
- `GET /api/health` - Check API status

### Emergency Contacts
- `GET /api/contacts` - List all contacts
- `POST /api/contacts` - Add new contact
- `PUT /api/contacts/:id` - Update contact
- `DELETE /api/contacts/:id` - Delete contact

### First Aid Kit
- `GET /api/first-aid-items` - List all items
- `POST /api/first-aid-items` - Add new item
- `PUT /api/first-aid-items/:id` - Update item
- `DELETE /api/first-aid-items/:id` - Delete item

### Quiz
- `GET /api/quiz/questions` - Get all questions
- `GET /api/quiz/questions?category=burns` - Get questions by category
- `POST /api/quiz/submit` - Submit quiz results
- `GET /api/quiz/results` - Get quiz history

### Body Map
- `GET /api/body-parts` - Get all body parts info
- `GET /api/body-parts/:partId` - Get specific body part first aid

### Emergency Workflows
- `GET /api/emergencies` - Get all emergency procedures
- `GET /api/emergencies/:type` - Get specific emergency workflow

### Preparedness Guides
- `GET /api/preparedness` - Get all disaster preparedness guides
- `GET /api/preparedness/:guideId` - Get specific guide

## Features

1. **SOS Emergency** - One-tap to call 911
2. **Body Map** - Tap body parts for first aid info
3. **Emergency Contacts** - Add and call personal contacts
4. **First Aid Kit** - Track medical supplies inventory
5. **Quiz** - Test your first aid knowledge
6. **AI Assistant** - Get instant guidance
7. **Preparedness** - Disaster guides (earthquake, flood, fire, cyclone)

## Technologies Used

- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, Lucide Icons
- **Backend**: Python 3, Flask, Flask-CORS
- **Database**: Supabase (PostgreSQL) or in-memory storage
- **Mobile**: Android (Java) - requires Android Studio

## Building the Android App

The Android app requires:
1. Java JDK 11+
2. Android Studio
3. Android SDK

To build:
```bash
./gradlew assembleDebug
```

The APK will be generated in `app/build/outputs/apk/debug/`
