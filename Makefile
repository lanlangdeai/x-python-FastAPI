.PHONY: help pf run

help:
	@echo "pf: put python dependence to requirements.txt"
	@echo "run: run web server"


pf:
	@pip freeze > requirements.txt

run:
	@uvicorn main:app --host 0.0.0.0 --port 8040 --reload
