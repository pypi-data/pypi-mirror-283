all:	clean build

deps:
	#python3 -m pip install --upgrade build
	#python3 -m pip install --upgrade twine
	sudo apt install python3-build
	pipx install twine

clean:
	rm -rf dist

build:
	python3 -m build

upload_prod:
	twine upload dist/*

upload_test:
	twine upload --repository testpypi dist/*

.PHONY:	build
