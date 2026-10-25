# EcoSphere — upgraded Django + React hackathon project

## Included
- Register/login using Django token authentication; user-owned records are scoped to the signed-in account.
- Waste photo upload and live camera capture, with a demo image classifier (rule-based filename/visual prompt fallback; replace with a trained model/API for reliable image recognition).
- AI Sustainability Advisor (rule-based local advisor, no external AI key required).
- GreenSteps challenge join/complete actions with per-user progress and points.
- Materials exchange listings with material type, weight, pickup/destination, approximate route distance/cost estimate, and delivery proof upload.
- Eco action logs, community reports, dashboard, Django admin.

## Requirements
Python 3.10+ and Node.js 18+.

### Backend (terminal 1)
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```
Optional admin: `python manage.py createsuperuser`, then visit http://127.0.0.1:8000/admin/.

### Frontend (terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173. Register a user first.

## Notes / limitations
- The waste classifier is a demonstrative starter and does not claim reliable AI vision. For real classification, connect a vision model/API or deploy a trained model and show confidence/uncertain results.
- Route distance uses the public OSRM demo routing service when available. Its estimate may be unavailable for locations that cannot be geocoded. Cost is an editable illustrative estimate, not a transport quote.
- Browser camera access requires localhost or HTTPS and permission. Delivery proof is stored as an uploaded image on the backend; configure durable object storage before production.
- This is a hackathon prototype. Before public production deployment, configure PostgreSQL, HTTPS, secure secrets, upload validation/storage, rate limits, moderation, privacy policy, and proper permissions.
- Vercel can host the React frontend; deploy Django separately to a Python-compatible host and set `VITE_API_URL` to its `/api` base URL.
