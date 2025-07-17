#!/usr/bin/env bash
set -e

PROJECT_DIR=/home/mathias/Dev/synapsyx/ePATH

# ─── LOAD .env INTO THE ENVIRONMENT ─────────────────────────────────────────
if [ -f "$PROJECT_DIR/.env" ]; then
  # export every variable in .env
  set -o allexport
  source "$PROJECT_DIR/.env"
  set +o allexport
fi

VENV=${PROJECT_DIR}/.venv/bin/activate

echo "Starting Docker Compose services…"
docker-compose up -d

SESSION="dev"

# kill any existing session
if tmux has-session -t $SESSION 2>/dev/null; then
  tmux kill-session -t $SESSION
fi

# new tmux session, start in project dir
tmux new-session -d -s $SESSION -n services -c $PROJECT_DIR

# pane 0: frontend
tmux send-keys -t $SESSION:0.0 'npm run dev' C-m

# split pane 0 side-by-side → pane 1
tmux split-window -h -t $SESSION:0.0 -c $PROJECT_DIR

# pane 1: activate venv then run Django
tmux send-keys -t $SESSION:0.1 "source $VENV && python manage.py runserver" C-m

# force even horizontal (side-by-side) layout
tmux select-layout -t $SESSION:0 even-horizontal

# attach
tmux attach -t $SESSION