#!/bin/bash

SESSION_NAME="alerts"

APP_DIR="."
VENV_DIR="$APP_DIR/.venv"
ENV_FILE="../../.env-pushover"

# Check if the tmux session already exists
tmux has-session -t "$SESSION_NAME" 2>/dev/null

if [ $? != 0 ]; then
  echo "Creating new tmux session: $SESSION_NAME"
  tmux new-session -s "$SESSION_NAME" -d

  # Send commands to the new session
  echo "Navigating to application directory: $APP_DIR"
  tmux send-keys -t "$SESSION_NAME" "cd $APP_DIR" C-m

  echo "Activating Python virtual environment: $VENV_DIR"
  tmux send-keys -t "$SESSION_NAME" "source $VENV_DIR/bin/activate" C-m

  # Check if .env file exists before sourcing
  if [ -f "$ENV_FILE" ]; then
    echo "Sourcing environment variables from: $ENV_FILE"
    tmux send-keys -t "$SESSION_NAME" "source $ENV_FILE" C-m
  else
    echo "Warning: .env-pushover file not found at $ENV_FILE."
  fi

  echo "Starting application with Gunicorn..."
  tmux send-keys -t "$SESSION_NAME" "gunicorn --bind 0.0.0.0:3000 -w 1 -k uvicorn.workers.UvicornWorker main:app" C-m

  echo "Session created. You can attach to it: tmux attach -t $SESSION_NAME"
else
  echo "Session '$SESSION_NAME' already exists. Attaching to it."
  tmux attach -t "$SESSION_NAME"
fi
