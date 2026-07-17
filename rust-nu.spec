# This spec is intended for COPR's SCM "make srpm" build method.
# .copr/Makefile creates the source archive with a vendored Cargo dependency tree.
# Nushell's integration tests require plugin binaries from the complete workspace.
# Build the distributable `nu` package by default; test-capable builders may use
# `--with check` after arranging those additional test artifacts.
%bcond_with check

# Nushell's release profile strips debug information, so RPM would otherwise
# attempt to create an empty debug-source subpackage.
%global debug_package %{nil}

Name:           nushell
Version:        0.114.1
Release:        1%{?dist}
Summary:        A new type of shell

License:        MIT
URL:            https://www.nushell.sh
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  pkgconf-pkg-config
BuildRequires:  rust
BuildRequires:  sqlite-devel

%description
Nushell is a modern shell that treats data as structured values rather than
plain text. It provides a rich set of commands for working with files,
processes, and structured data.

%prep
%autosetup

%build
cargo --config .copr/cargo-vendor.toml build --offline --locked --release --package nu

%install
install -Dpm 0755 target/release/nu %{buildroot}%{_bindir}/nu

%check
%if %{with check}
cargo --config .copr/cargo-vendor.toml test --offline --locked --package nu
%endif

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md SECURITY.md
%{_bindir}/nu

%changelog
* Fri Jul 17 2026 The Nushell Project Developers <https://www.nushell.sh>
- Initial COPR package
