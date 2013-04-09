RPY_WRAP = python
RPY_FLAGS =--output=bin/pylua 
RPY = ~/projects/python/pypy/rpython/bin/rpython

all: clean pylua

clean:
	rm -rf ./bin

pylua: 
	mkdir -p ./bin
	PYTHONPATH="." $(RPY_WRAP) $(RPY) $(RPY_FLAGS) pylua/main.py ../bin/pylua
.PHONY: pylua

test:
	python runtests.py