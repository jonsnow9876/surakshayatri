# SurakshaYatri Backend Documentation

## Table of Contents

1. [Setup Instructions](#setup-instructions)
2. [Overview](#overview)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Database Models](#database-models)
6. [API Endpoints](#api-endpoints)

   * [Tourist Registration](#tourist-registration)
   * [Itinerary Update](#itinerary-update)
   * [Panic Alert](#panic-alert)
   * [Alerts](#alerts)
7. [Blockchain Integration](#blockchain-integration)
8. [Workflow](#workflow)
9. [Notes](#notes)

---

## Setup Instructions

Follow these steps to set up and run the SurakshaYatri backend locally in **VSCode**:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend
```

### 2. Create a Python Virtual Environment

```bash
python3 -m venv venv
```

Activate the virtual environment:

* **Windows (Powershell)**:

```powershell
venv\Scripts\activate.ps1
```

* **Linux/macOS**:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

* Open in browser: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the Swagger UI.

### 7. VSCode Development Tips

* Install **Python** and **Pylance** extensions.
* Set interpreter to the virtual environment: `Ctrl+Shift+P → Python: Select Interpreter`.
* Enable auto-reload (`--reload`) while running with Uvicorn.
* Use **Breakpoints** in VSCode for debugging.

---

## Overview

The **SurakshaYatri backend** provides a tourist safety platform where tourists can register, update itineraries, and send panic alerts. Each alert is logged to a **local blockchain** for immutable records, while resolution status is tracked in the database.

Key features:

* Tourist registration with permanent and temporary IDs.
* Update of itineraries with new temporary IDs for anonymity.
* Panic alert system with geolocation.
* Blockchain logging for every alert.
* Admin dashboard can view and resolve alerts, with resolutions stored on the blockchain.

---

## Tech Stack

* **Backend Framework**: FastAPI
* **Database**: SQLAlchemy ORM (SQLite / PostgreSQL / MySQL compatible)
* **Blockchain**: File-based JSON blockchain with SHA256 hashing
* **QR Code**: Python `qrcode` library
* **Language**: Python 3.11+

---

## Project Structure

```
backend/
│
├── main.py                  # FastAPI entry point
├── database.py              # Database connection & session helper
├── models.py                # SQLAlchemy ORM models
├── schemas.py               # Pydantic request/response models
├── blockchain.py            # Blockchain helper functions
├── routers/
│   ├── register.py          # Tourist registration & itinerary update
│   ├── panic.py             # Panic alert routes
│   ├── alerts.py            # Fetch and resolve alerts
└── data/
    └── blockchain.json      # Blockchain storage
```

---

*(The rest of your documentation — Database Models, API Endpoints, Blockchain Integration, Workflow, Notes — stays the same.)*

---

If you want, I can also add a **one-line VSCode launch configuration** so you can just press **F5** to start the FastAPI server with auto-reload inside VSCode. This makes local development much smoother.

Do you want me to add that too?

---

## Database Models

### Tourist

* **id**: permanent UUID
* **name**: Tourist name
* **passport**: unique passport number
* **temp\_id**: temporary anonymized ID for itinerary/alert linkage
* **itinerary**: optional itinerary string
* **emergency\_contact**: phone/email
* **blockchain\_hash**: last blockchain hash for reference
* **resolved**: boolean flag for any current alert resolved
* **timestamps**: created, updated, resolved

### History

* Tracks previous itineraries for a tourist.

### AlertStatus

* **alert\_uuid**: unique alert ID
* **resolved**: boolean
* **resolved\_at**: timestamp
* **resolved\_by**: admin ID/name
* **last\_block\_hash**: blockchain hash for last update

---

## API Endpoints

### Tourist Registration

#### POST `/register/new`

* **Description**: Register a new tourist. Generates permanent `id` and temporary `temp_id`. Returns a QR code with `id`.
* **Request Body**:

```json
{
  "name": "John Doe",
  "passport": "A1234567",
  "itinerary": "Mumbai → Goa",
  "emergency_contact": "9876543210"
}
```

* **Response**:

```json
{
  "tourist_id": "uuid-string",
  "temp_id": "uuid-string",
  "qr_code_base64": "data:image/png;base64,...."
}
```

### Itinerary Update

#### PATCH `/register/update_itinerary`

* **Description**: Update itinerary for a tourist. Generates new `temp_id`.
* **Request Body**:

```json
{
  "id": "tourist-permanent-uuid",
  "itinerary": "New itinerary details"
}
```

* **Response**:

```json
{
  "tourist_id": "uuid-string",
  "temp_id": "new-uuid-string",
  "qr_code_base64": "data:image/png;base64,...."
}
```

### Panic Alert

#### POST `/panic/`

* **Description**: Trigger a panic alert. Uses the **permanent `id`**, logs to blockchain.
* **Request Body**:

```json
{
  "tourist_id": "uuid-string",
  "lat": 19.0760,
  "lon": 72.8777
}
```

* **Response**:

```json
{
  "alert_uuid": "uuid-string",
  "temp_id": "uuid-string",
  "lat": 19.0760,
  "lon": 72.8777,
  "timestamp": "ISO8601",
  "blockchain_hash": "sha256-hash"
}
```

### Alerts

#### GET `/alerts/`

* Fetch all alerts. Optional query: `?unresolved_only=true`

#### GET `/alerts/tourist/{temp_id}`

* Fetch alerts for a specific tourist temporary ID

#### PATCH `/alerts/{alert_uuid}/resolve`

* Mark an alert as resolved. Also appends **resolution block to blockchain**.
* Optional query param: `resolved_by=<admin-name>`

---

## Blockchain Integration

* Each alert is appended to `blockchain.json` with the following structure:

```json
{
  "index": 1,
  "timestamp": "ISO8601",
  "data": {
    "temp_id": "...",
    "alert_uuid": "...",
    "lat": ...,
    "lon": ...
  },
  "prev_hash": "...",
  "hash": "sha256-hash"
}
```

* Resolution blocks are added with:

```json
{
  "alert_uuid": "...",
  "temp_id": "...",
  "resolved": true,
  "resolved_by": "...",
  "resolved_at": "ISO8601"
}
```

* **Integrity** is ensured via SHA256 hash chaining.

---

## Workflow

1. Tourist registers → receives permanent ID + temporary ID → QR code generated.
2. Tourist updates itinerary → new temp ID is generated.
3. Tourist triggers panic → alert logged to blockchain with temp ID.
4. Admin views alerts → resolves alert → resolution logged to blockchain.
5. All blockchain entries are immutable and auditable.

---

## Notes

* **Temporary IDs** provide anonymity for alerts.
* **Blockchain** ensures that alerts and resolutions are tamper-proof.
* **DB** is used for quick query and resolution tracking.
* QR codes always encode **permanent ID**, while alerts use **temp ID**.
* Can be extended to a **full distributed blockchain** in future.

---
