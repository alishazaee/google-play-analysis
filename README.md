# Google Play Store Analysis Project

## Overview
Welcome to the Google Play Store Analysis Project! This repository is dedicated to providing a thorough analysis of applications available on the Google Play Store. Our goal is to uncover trends, evaluate user preferences, and offer valuable insights that can guide app developers and digital marketers in making informed decisions.

## Key Features
- **Comprehensive Data Extraction**: Automated scripts to fetch the latest data from the Google Play Store.
- **Robust Data Cleaning & Preprocessing**: Ensuring data quality for accurate analysis.
- **In-depth User Ratings Analysis**: Dive into what users love and what they don't.
- **Dynamic Visualization Tools**: Interactive charts and graphs to represent data insights vividly.

## Quick Start Guide
### Prerequisites
Before you begin, ensure you have the following:
- Python version 3.6 or above.
- Libraries: celery,google-play-scraper , etc (Install using `requirements.txt`).

### Installation Steps
1. Clone this repository:
   ```shell
   git clone https://github.com/alishb80/google-play-analysis.git
    ```
2. compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
    ```shell
    cd gooanalysis
    ```

3. SetUp venv
    ```shell
    virtualenv -p python3.10 venv
    source venv/bin/activate
    ```

4. install Dependencies
    ```shell
    pip install -r requirements_dev.txt
    pip install -r requirements.txt
    ```

5. create your env
    ```
    cp .env.example .env
    ```

6. Create tables
    ```
    python manage.py migrate
    ```

7. spin off docker compose
    ```
    docker compose -f docker-compose.dev.yml up -d
    ```

8. run the project
    ```
    python manage.py runserver
    ```

9. start the worker and beats
    ```
    celery -A gooanalysis.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
    celery -A gooanalysis.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ```


