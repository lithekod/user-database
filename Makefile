VENV := venv
FLASK_ARGS := --port 5000 --host 0.0.0.0 --reload

.PHONY: clean db emails server

server: $(VENV) | emails db
	@(. $(VENV)/bin/activate && flask run $(FLASK_ARGS))

clean:
	rm -rf $(VENV)

$(VENV):
	python3 -m venv $(VENV)
	@(. $(VENV)/bin/activate && pip install -r requirements.txt)

emails:
	@echo "Updating emails."
	@if [ -d emails ]; \
		then (cd emails && git pull); \
		else git clone https://github.com/lithekod/emails; \
	fi

db:
	@(. $(VENV)/bin/activate && python3 migrate_db.py)
