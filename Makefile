RPY_WRAP = python
RPY_FLAGS =--output=bin/luna 
RPY = ~/projects/python/pypy/rpython/bin/rpython

all: clean luna

clean:
	rm -rf ./bin

luna: 
	mkdir -p ./bin
	PYTHONPATH="." $(RPY_WRAP) $(RPY) $(RPY_FLAGS) luna/main.py ../bin/luna
.PHONY: luna

test:
	python runtests.py