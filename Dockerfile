FROM python:3.13.2

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy dbt project files
COPY rwa_dbt/ ./rwa_dbt/

# Set dbt profiles directory (optional - if you have profiles.yml)
ENV DBT_PROFILES_DIR=/root/.dbt

# Default command
CMD ["dbt", "run", "--project-dir", "/app/rwa_dbt"]