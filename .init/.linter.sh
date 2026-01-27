#!/bin/bash
cd /home/kavia/workspace/code-generation/event-booking-platform-310917/event_booking_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

