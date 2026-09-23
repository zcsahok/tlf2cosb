
tlf2cosb.pyz: src/*.py
	python3 -m zipapp src -o tlf2cosb.pyz -c -m main:main -p /usr/bin/python3

clean:
	rm -f *.pyz
