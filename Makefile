
tlf2cosb.pyz: src/*.py
	python3 -m zipapp src -o tlf2cosb.pyz -c -m main:main -p /usr/bin/python3

release: tlf2cosb.pyz

test:
	bats test/test.bats

clean:
	rm -f *.pyz

.PHONY: clean release test
