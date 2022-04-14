PYTHON=python3
VENV=venv
ACTIVATE=$(VENV)/bin/activate
XMAP=$(VENV)/bin/xmap

$(XMAP): $(ACTIVATE)
	source $(ACTIVATE) && pip install -e .

$(ACTIVATE):
	$(PYTHON) -m venv $(VENV)

clean:
	$(RM) -r $(VENV)

doc:
	make

.PHONY: clean
