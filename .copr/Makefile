# COPR invokes this target for SCM builds configured with the "make srpm"
# source method. It creates an SRPM from the exact checked-out commit and
# vendors Cargo dependencies before the isolated RPM build begins.

SHELL := /bin/bash
SPEC := $(if $(spec),$(spec),rust-nu.spec)
VERSION := $(shell rpmspec -q --qf '%{VERSION}' --srpm $(SPEC))
SOURCE_ARCHIVE := nushell-$(VERSION).tar.gz
VENDOR_DIR := .copr/vendor
VENDOR_CONFIG := .copr/cargo-vendor.toml

.PHONY: srpm
srpm:
	set -euo pipefail; \
	if ! command -v cargo >/dev/null; then dnf -y install cargo; fi; \
	archive="$$(mktemp --suffix=.tar.gz)"; \
	cleanup() { rm -rf "$(VENDOR_DIR)" "$(VENDOR_CONFIG)" "$(SOURCE_ARCHIVE)" "$$archive"; }; \
	trap cleanup EXIT; \
	cargo vendor --locked "$(VENDOR_DIR)" > "$(VENDOR_CONFIG)"; \
	tar --create --gzip --file "$$archive" \
		--exclude=./.git --exclude=./target \
		--transform "s,^,nushell-$(VERSION)/," .; \
	mv "$$archive" "$(SOURCE_ARCHIVE)"; \
	rpmbuild -bs \
		--define "_sourcedir $(CURDIR)" \
		--define "_srcrpmdir $(outdir)" \
		"$(SPEC)"
