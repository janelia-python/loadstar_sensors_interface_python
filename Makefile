# This file is generated automatically from .metadata.org
# File edits may be overwritten!

upload: metadata package twine add clean

GUIX-SHELL = guix time-machine -C .channels.scm -- shell
GUIX-CONTAINER = $(GUIX-SHELL) --container
PORT = /dev/ttyUSB0
EXPOSED-GUIX-CONTAINER = $(GUIX-CONTAINER) --expose=$(PORT)
DEVELOPMENT = -D -f .guix.scm

dev-shell:
	$(EXPOSED-GUIX-CONTAINER) $(DEVELOPMENT)

ipython-shell:
	$(EXPOSED-GUIX-CONTAINER) $(DEVELOPMENT) -- ipython

serial-shell:
	$(EXPOSED-GUIX-CONTAINER) picocom -- picocom -b 9600 -f n -y n -d 8 -p 1 -c $(PORT)

installed-shell:
	$(EXPOSED-GUIX-CONTAINER) -f .guix.scm --rebuild-cache

metadata-edits:
	$(GUIX-CONTAINER) --preserve='^DISPLAY$$' --preserve='^TERM$$' $(DEVELOPMENT) -- sh -c "emacs -q --no-site-file --no-site-lisp --no-splash -l .init.el --file .metadata.org"

metadata:
	$(GUIX-CONTAINER) $(DEVELOPMENT) -- sh -c "emacs --batch -Q  -l .init.el --eval '(process-org \".metadata.org\")'"

package:
	$(GUIX-CONTAINER) $(DEVELOPMENT) -- sh -c "python3 setup.py sdist bdist_wheel"

twine:
	$(GUIX-CONTAINER) $(DEVELOPMENT) -- sh -c "twine upload dist/*"

add:
	$(GUIX-CONTAINER) $(DEVELOPMENT) -- sh -c "git add --all"

clean:
	$(GUIX-CONTAINER) $(DEVELOPMENT) -- sh -c "git clean -xdf"
