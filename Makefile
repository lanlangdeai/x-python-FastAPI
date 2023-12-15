.PHONY: help pf

help:
	@echo "pf: put python dependence to requirements.txt"


pf:
	@pip freeze > requirements.txt
