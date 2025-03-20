sudo docker compose down postgres
sudo rm -rf ./db/storage/
sudo docker compose up -d postgres
sleep 2
./venv/bin/alembic stamp base
./venv/bin/alembic upgrade head
