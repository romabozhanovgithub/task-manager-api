echo "Waiting for postgres..."
python ./scripts/wait_for_postgres.py
echo "Postgres started"

echo "Migration started"
python -m alembic upgrade head
echo "Migration finished"

APP_PORT=${APP_PORT:-5000}
echo "Starting app on port $APP_PORT..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $APP_PORT --reload
