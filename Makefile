# This file is generated automatically from .metadata.org
# File edits may be overwritten!

upload: files package twine add clean

dev-shell:
	guix time-machine -C .channels.scm -- shell --container -D -f .guix.scm

ipython-shell:
	guix time-machine -C .channels.scm -- shell --container -D -f .guix.scm -- ipython

serial-shell:
	guix shell picocom -- picocom -b 9600 -f n -y n -d 8 -p 1 -c /dev/ttyUSB0

installed-shell:
	guix time-machine -C .channels.scm -- shell --container -f .guix.scm --rebuild-cache

edits:
	guix time-machine -C .channels.scm -- shell --container --preserve='^DISPLAY$$' --preserve='^TERM$$' -D -f .guix.scm -- sh -c "emacs -q --no-site-file --no-site-lisp --no-splash -l .init.el --file .metadata.org"

files:
	guix time-machine -C .channels.scm -- shell --container -D -f .guix.scm -- sh -c "emacs --batch -Q  -l .init.el --eval '(process-org \".metadata.org\")'"

package:
	guix time-machine -C .channels.scm -- shell --container -D -f .guix.scm -- sh -c "python3 setup.py sdist bdist_wheel"

twine:
	guix time-machine -C .channels.scm -- shell --container -D -f .guix.scm -- sh -c "twine upload dist/*"

add:
	guix time-machine -C .channels.scm -- shell --container -D -f .guix.scm -- sh -c "git add --all"

clean:
	guix time-machine -C .channels.scm -- shell --container -D -f .guix.scm -- sh -c "git clean -xdf"
