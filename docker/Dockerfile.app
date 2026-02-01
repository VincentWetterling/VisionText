FROM visiontext:latest

# Only replace application code to avoid reinstalling heavy dependencies
WORKDIR /app
COPY app ./app
COPY static ./static
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
