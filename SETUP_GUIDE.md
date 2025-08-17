# PolicyAthena Backend Setup Guide

This guide will help you set up the PolicyAthena backend to handle data from both UserInput and UserProfile frontend components.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A database (PostgreSQL recommended, SQLite for development)

## Installation

1. **Clone the repository and navigate to the backend directory:**
   ```bash
   cd PolicyAthena---backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the template
   cp env_template.txt .env
   
   # Edit .env with your database credentials
   nano .env  # or use your preferred editor
   ```

4. **Configure your database:**
   
   **Option A: PostgreSQL (Recommended for production)**
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/policyathena
   ```
   
   **Option B: SQLite (For development)**
   ```bash
   DATABASE_URL=sqlite:///./policyathena.db
   ```

## Database Setup

1. **Initialize the database tables:**
   ```bash
   python init_db.py
   ```
   
   This will create all necessary tables for:
   - UserProfile data (personal_info, employment_info, user_profiles)
   - UserInput data (current_insurance, coverage_needs, eligibility_info, documents, etc.)

2. **Verify database connection:**
   ```bash
   python app/db/session.py
   ```

## Running the Backend

1. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Verify the server is running:**
   - Open your browser to `http://localhost:8000/docs`
   - You should see the FastAPI interactive documentation

## Testing the Data Flow

1. **Run the test script:**
   ```bash
   python test_data_flow.py
   ```
   
   This will test both UserProfile and UserInput data submissions.

2. **Expected output:**
   ```
   Starting data flow tests...
   ==================================================
   Testing UserProfile data submission...
   Status Code: 200
   Response: {'success': True, 'file_saved': True, ...}
   
   Testing UserInput data submission...
   Status Code: 200
   Response: {'success': True, 'file_saved': True, ...}
   
   ==================================================
   Test Results:
   UserProfile: PASS
   UserInput: PASS
   
   ✅ All tests passed! Data flow is working correctly.
   ```

## API Endpoints

### POST /userInput/profile

**Purpose**: Receives data from both UserInput and UserProfile components

**Request Body**: JSON with `source` field indicating data type
- `source: "userprofile"` → Saves to personal_info and employment_info tables
- `source: "userinput"` → Saves to insurance, coverage, and eligibility tables

**Response**: Success/error status with database ID and file path

## Data Storage

### Database Tables
- **UserProfile Data**: Stored in `personal_info`, `employment_info`, and `user_profiles` tables
- **UserInput Data**: Stored in `current_insurance`, `coverage_needs`, `eligibility_info`, `documents`, and related tables

### File Storage
- **UserProfile**: Saved to `data/user_profiles/` directory
- **UserInput**: Saved to `data/user_inputs/` directory
- Files are timestamped for easy identification

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify DATABASE_URL in .env file
   - Ensure database server is running
   - Check database credentials

2. **Table Creation Error**
   - Run `python init_db.py` to create tables
   - Check database permissions

3. **Import Errors**
   - Ensure you're in the correct directory
   - Check Python path and imports

4. **CORS Issues**
   - Backend is configured to allow all origins for development
   - Adjust CORS settings in production

### Debug Mode

Enable debug logging by setting `DEBUG=true` in your .env file.

## Production Considerations

1. **Security**
   - Disable CORS for all origins
   - Implement authentication and authorization
   - Use HTTPS

2. **Database**
   - Use PostgreSQL for production
   - Implement connection pooling
   - Set up database backups

3. **File Storage**
   - Use cloud storage (AWS S3, Google Cloud Storage)
   - Implement file encryption
   - Set up file retention policies

## Support

If you encounter issues:
1. Check the logs for error messages
2. Verify database connectivity
3. Ensure all dependencies are installed
4. Check the test script output for clues

## Next Steps

After successful setup:
1. Test with the frontend components
2. Implement additional validation as needed
3. Add authentication and authorization
4. Set up monitoring and logging

