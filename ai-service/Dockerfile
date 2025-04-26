# Step 1: Use an official lightweight Python image
FROM python:3.10-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the app code
COPY app/ app/
COPY app/tarot_prompt_template.txt app/


# Step 5: Expose the service port
EXPOSE 8000

# Step 6: Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
