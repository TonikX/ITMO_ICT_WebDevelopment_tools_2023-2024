PYTHON=.venv/bin/python
PIP=.venv/bin/pip
ENV_FILE=.env
PYTHONPATH=src

.PHONY: install sum-threading sum-multiprocessing sum-async sum-all parse-threading parse-multiprocessing parse-async parse-all bench-all

install:
	python3 -m venv .venv
	$(PIP) install -r requirements.txt
	cp -n .env.example $(ENV_FILE) || true
	mkdir -p results

sum-threading:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m lr2.sum_bench.threading_sum

sum-multiprocessing:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m lr2.sum_bench.multiprocessing_sum

sum-async:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m lr2.sum_bench.async_sum

sum-all:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m lr2.sum_bench.run_sum_bench

parse-threading:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m lr2.parse_bench.threading_parse

parse-multiprocessing:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m lr2.parse_bench.multiprocessing_parse

parse-async:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m lr2.parse_bench.async_parse

parse-all:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m lr2.parse_bench.run_parse_bench

bench-all: sum-all parse-all
