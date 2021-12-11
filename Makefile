VENV := venv
FLASK_ARGS := --port 5000 --host 0.0.0.0 --reload

.PHONY: clean db server

server: $(VENV) | db
	@(. $(VENV)/bin/activate && flask run $(FLASK_ARGS))

clean:
	rm -rf $(VENV)

$(VENV):
	python3 -m venv $(VENV)
	@(. $(VENV)/bin/activate && pip install -r requirements.txt)

db:
	@(. $(VENV)/bin/activate && python3 migrate_db.py)
