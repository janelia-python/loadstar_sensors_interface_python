dev-shell:
	guix time-machine -C .channels.scm -- shell --pure -D -f .guix.scm

ipython-shell:
	guix time-machine -C .channels.scm -- shell --pure -D -f .guix.scm -- ipython

serial-shell:
	guix shell picocom -- picocom -b 9600 -f n -y n -d 8 -p 1 -c /dev/ttyUSB0

installed-shell:
	guix time-machine -C .channels.scm -- shell --pure -f .guix.scm --rebuild-cache

upload: files package twine add clean

edits:
	emacs -q --no-site-file --no-site-lisp --no-splash -l .emacs --file .single-source-of-truth.org

files:
	emacs --batch -Q  -l .emacs --eval '(process-org ".single-source-of-truth.org")'

package:
	python3 setup.py sdist bdist_wheel

twine:
	twine upload dist/*

add:
	git add --all

clean:
	git clean -xdf
