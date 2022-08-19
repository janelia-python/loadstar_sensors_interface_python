shell:
	guix time-machine -C .channels.scm -- shell --pure -D -f .guix.scm

ipython:
	guix time-machine -C .channels.scm -- shell --pure -D -f .guix.scm -- ipython

picocom:
	guix shell picocom -- picocom -b 9600 -f n -y n -d 8 -p 1 -c /dev/ttyUSB0

all: files package upload add clean

edits:
	emacs -q --no-site-file --no-site-lisp --no-splash -l .emacs --file .single-source-of-truth.org

files:
	emacs --batch -Q  -l .emacs --eval '(process-org ".single-source-of-truth.org")'

package:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*

add:
	git add --all

clean:
	git clean -xdf
