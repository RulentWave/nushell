# Building Nushell with COPR

This directory supports COPR SCM builds from the Nushell repository without
requiring network access during the RPM build itself.

## COPR setup

1. Create a COPR project with a chroot that provides Rust `1.95.0` or newer.
2. Add an SCM package using this repository's clone URL.
3. Select the **make srpm** source method and set the spec file to
   `rust-nu.spec`.
4. Select the tag, branch, or commit to build and start the build.

COPR calls `.copr/Makefile`'s `srpm` target. Because this stage runs before
RPM `BuildRequires` are installed, the target installs `cargo` with `dnf` when
needed. It then vendors the exact `Cargo.lock` dependency set, archives the
checked-out source, and writes the SRPM to COPR's supplied output directory. The RPM spec then invokes Cargo in
`--offline --locked` mode, making the binary RPM build independent of network
access and of distribution-packaged Rust crates.

To create an SRPM locally, run:

```bash
make -f .copr/Makefile srpm outdir="$PWD"
```

The command requires `cargo`, `rpmbuild`, and `rpmspec`. It creates the
vendored files only temporarily and leaves the resulting SRPM in `outdir`.
