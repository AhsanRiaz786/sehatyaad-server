# SehatYaad Backend

Flask backend for SehatYaad medication tracking app. Handles secure API calls to Gemini AI for prescription image processing.

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your Gemini API key:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Run Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "SehatYaad Backend",
  "version": "1.0.0"
}
```

### Process Medication Image
```
POST /api/process-medication-image
```

Request:
- Content-Type: `multipart/form-data`
- Body: `image` file (PNG, JPG, JPEG, GIF, HEIC)

Response:
```json
{
  "success": true,
  "data": {
    "medications": [
      {
        "name": "Medication Name",
        "dosage": "100",
        "dosageUnit": "mg",
        "frequency": "twice daily",
        "times": ["08:00", "20:00"],
        "instructions": "take with food",
        "confidence": "high"
      }
    ],
    "doctorName": "Dr. Name",
    "date": "2025-12-02",
    "pharmacyName": "Pharmacy Name"
  }
}
```

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Testing with curl
```bash
curl -X POST http://localhost:5000/api/process-medication-image \
  -F "image=@/path/to/prescription.jpg"
```

## Deployment

For production deployment, use gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Recommended Platforms
- Railway
- Render
- Heroku
- Google Cloud Run

## Configuration

Environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `FLASK_ENV` | Environment (development/production) | development |
| `PORT` | Server port | 5000 |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | * |
| `MAX_CONTENT_LENGTH` | Max upload size in bytes | 16777216 (16MB) |

## Security Notes

⚠️ **Never commit the `.env` file to version control**

The `.gitignore` file ensures `.env` is excluded, but always verify before pushing code.
