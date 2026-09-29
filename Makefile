
tlf2cosb.pyz: src/*.py
	python3 -m zipapp src -o tlf2cosb.pyz -c -m main:main -p /usr/bin/python3

release: tlf2cosb.pyz test

test: tlf2cosb.pyz
	bats test/test.bats

clean:
	rm -f *.pyz

.PHONY: clean release test
