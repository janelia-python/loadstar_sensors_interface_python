# This file is generated automatically from .metadata.org
# File edits may be overwritten!

.PHONY: upload
upload: metadata package twine add clean

GUIX-SHELL = guix time-machine -C .channels.scm -- shell
GUIX-CONTAINER = $(GUIX-SHELL) --container
PORT = /dev/ttyUSB0
GUIX-CONTAINER-EXPOSED = $(GUIX-CONTAINER) --expose=$(PORT)
DEVELOPMENT = -D -f .guix.scm
GUIX-CONTAINER-DEVELOPMENT = $(GUIX-CONTAINER) $(DEVELOPMENT)
GUIX-CONTAINER-GUI = $(GUIXCONTAINER-DEVELOPMENT) --preserve='^DISPLAY$$' --preserve='^TERM$$'

.PHONY: shell
shell:
	$(GUIX-SHELL)

.PHONY: container
container:
	$(GUIX-CONTAINER)

.PHONY: exposed-container
exposed-container:
	$(GUIX-CONTAINER-EXPOSED)

.PHONY: dev-container
dev-container:
	$(GUIX-CONTAINER-EXPOSED) $(DEVELOPMENT)

.PHONY: ipython-shell
ipython-shell:
	$(GUIX-CONTAINER-EXPOSED) $(DEVELOPMENT) -- ipython

.PHONY: serial-shell
serial-shell:
	$(GUIX-CONTAINER-EXPOSED) picocom -- picocom -b 9600 -f n -y n -d 8 -p 1 -c $(PORT)

.PHONY: installed-shell
installed-shell:
	$(GUIX-CONTAINER-EXPOSED) -f .guix.scm --rebuild-cache

.PHONY: metadata-edits
metadata-edits:
	$(GUIX-CONTAINER-GUI) -- sh -c "emacs -q --no-site-file --no-site-lisp --no-splash -l .init.el --file .metadata.org"

.PHONY: metadata
metadata:
	$(GUIX-CONTAINER-DEVELOPMENT) -- sh -c "emacs --batch -Q  -l .init.el --eval '(process-org \".metadata.org\")'"

.PHONY: package
package:
	$(GUIX-CONTAINER-DEVELOPMENT) -- sh -c "python3 setup.py sdist bdist_wheel"

.PHONY: twine
twine:
	$(GUIX-CONTAINER-DEVELOPMENT) -- sh -c "twine upload dist/*"

.PHONY: add
add:
	$(GUIX-CONTAINER-DEVELOPMENT) -- sh -c "git add --all"

.PHONY: clean
clean:
	$(GUIX-CONTAINER-DEVELOPMENT) -- sh -c "git clean -xdf"
