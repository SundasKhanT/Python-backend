# 1. Create virtual environment

python -m venv venv
venv\Scripts\activate # Windows

# 2. Install dependencies

pip install -r requirements.txt

# 3. Run database migrations

# 4. Start server

uvicorn backend.main:app --reload

# 5. Run tests

pytest
