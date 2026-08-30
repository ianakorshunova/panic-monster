# Panic Monster

Panic Monster is a small Streamlit self-help app for moments when your brain is being dramatic.

The app helps you slow down, identify what is happening, choose one tiny next step, and optionally save the moment for later reflection.

> Your brain is being dramatic. Let’s make the monster smaller for the next 5 minutes.

## Features

- Six common states:
  - I'm panicking
  - I feel overwhelmed
  - I'm avoiding a task
  - I need one tiny step
  - I need to send a scary message
  - I need aftercare
- Four monster characters representing different patterns:
  - Anxiety Monster
  - Procrastination Monster
  - Fear Monster
  - Negativity Monster
- Random supportive monster messages
- Small grounding and action steps
- Before / after intensity tracking
- Trigger tracking
- Notes and reflections
- Tiny-step completion tracking
- Personal insights and recent monster visits
- CSV export
- PostgreSQL storage with Neon
- Password-protected access

## Meet the Monsters

### Anxiety Monster

Anxiety Monster is tall, nervous, hyper-alert, and always carrying a flashlight.

It appears when everything feels urgent, uncertain, or potentially dangerous — even when nothing actually requires immediate action.

### Procrastination Monster

Procrastination Monster is charming, stylish, and extremely good at finding reasons to do literally anything except the task.

It appears when starting feels harder than avoiding.

### Fear Monster

Fear Monster is small, cautious, and would very much like to hide behind a folder forever.

It usually appears around difficult messages, uncomfortable decisions, and situations where pressing “Send” suddenly feels like a major life event.

### Negativity Monster

Negativity Monster is the grumpy internal critic.

It appears after difficult moments and helpfully explains why everything you did was probably wrong.

## How it works

1. Choose what is happening right now.
2. Let Panic Monster identify the visitor.
3. Try one small suggested action.
4. Mark the step as completed or ask for another one.
5. Record your intensity, trigger, and optional notes.
6. Save the moment.
7. Review patterns later in the Insights section.

## Tech stack

- Python
- Streamlit
- pandas
- SQLAlchemy
- PostgreSQL
- Neon

## Data storage

Panic Monster uses a Neon PostgreSQL database to store saved entries.

Database credentials and the app password are stored using Streamlit Secrets and are not included in the repository.

## Running locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
NEON_DATABASE_URL = "your_neon_connection_string"
APP_PASSWORD = "your_password"
```

Then run:

```bash
streamlit run app.py
```

## Privacy

This repository is public, but the deployed personal app is protected by a password.

Secrets such as the database connection string and app password are not stored in the repository.

## Disclaimer

Panic Monster is a small self-help tool for grounding, journaling, and choosing manageable next steps.

It is not a medical or mental health treatment tool and does not replace professional support.

## Status

MVP deployed and working.

Current version includes:

- password-protected access
- Neon database storage
- personal logging
- insights
- CSV export
- four monster characters

## Deployment

The app is deployed privately on Streamlit Community Cloud.