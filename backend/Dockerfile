FROM python:3.9-slim

WORKDIR /app

# Namestitev potrebnih sistemskih knjižnic za prevajanje in delovanje PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir psycopg2-binary

COPY . .

# Naredi skripto izvedljivo
RUN chmod +x start.sh

CMD ["./start.sh"]
