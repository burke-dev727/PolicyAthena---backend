# Data Flow Documentation

This document describes how data flows from the frontend (UserInput and UserProfile components) to the backend database.

## Overview

The system handles two types of user data:
1. **UserProfile**: Personal and employment information
2. **UserInput**: Insurance, coverage, eligibility, and document information

## Data Flow Architecture

```
Frontend (React) → Backend (FastAPI) → Database (SQLAlchemy) → File Storage
```

## Frontend Components

### UserProfile.jsx
- Collects personal information (name, age, email, phone, address, location, zipcode, SSN)
- Collects employment information (employment status, employer name, insurance offerings, annual income, household size)
- Sends data with `source: "userprofile"`

### UserInput.jsx
- Collects current insurance information (insurance status, provider, policy number, dates, source)
- Collects coverage needs (type, level, budget, preferred providers, conditions, prescriptions)
- Collects eligibility information (citizenship, Medicaid/Medicare eligibility, veteran status, student status, life events)
- Collects document preferences (insurance documents, proof of income)
- Sends data with `source: "userinput"`

## Backend API Endpoint

**Endpoint**: `POST /userInput/profile`

**Route**: `app/routers/input_route.py`

**Functionality**:
1. Receives JSON data from frontend
2. Determines data type based on `source` field
3. Saves data to appropriate database tables
4. Saves JSON file to disk for backup
5. Processes data through InputInterpreterAgent
6. Returns success/error response

## Database Models

### UserProfile Data
- `personal_info` table: Personal information
- `employment_info` table: Employment details
- `user_profiles` table: Links personal and employment info

### UserInput Data
- `current_insurance` table: Current insurance details
- `coverage_needs` table: Coverage requirements
- `eligibility_info` table: Eligibility information
- `documents` table: Document preferences
- `preferred_providers` table: Preferred insurance providers
- `preexisting_conditions` table: Medical conditions
- `current_prescriptions` table: Current medications
- `recent_life_events` table: Recent life events
- `user_inputs` table: Links all insurance-related data

## File Storage

Data is saved to disk in the following structure:
```
data/
├── user_profiles/
│   ├── userprofile_20250101_120000.json
│   └── ...
└── user_inputs/
    ├── userinput_20250101_120000.json
    └── ...
```

## Data Validation

### UserProfile Validation
- At least one section (personal or employment) must have data
- All fields are optional but validated for proper types

### UserInput Validation
- At least one section (insurance, coverage, or eligibility) must have data
- Boolean fields are properly handled for None vs False
- Array fields are converted from comma-separated strings

## Error Handling

- **400 Bad Request**: Invalid source field or malformed JSON
- **500 Internal Server Error**: Database or file system errors
- **Validation Errors**: Missing required data sections
- **Database Errors**: Transaction rollback on failure

## Testing

Use the `test_data_flow.py` script to verify the data flow:

```bash
cd PolicyAthena---backend
python test_data_flow.py
```

This script tests both UserProfile and UserInput data submissions.

## Security Considerations

- CORS is enabled for development
- Input validation prevents malicious data
- Database transactions ensure data integrity
- File storage is isolated to data directory

## Future Improvements

1. Add authentication and authorization
2. Implement data encryption
3. Add rate limiting
4. Implement data backup and recovery
5. Add data validation schemas (Pydantic models)
