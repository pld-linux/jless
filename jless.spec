%define		crates_ver	0.9.0

Summary:	A command-line JSON viewer
Name:		jless
Version:	0.9.0
Release:	1
License:	MIT
Group:		Applications
Source0:	https://github.com/PaulJuliusMartinez/jless/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5cb028a732112d87190cc48975d46761
# ./create-crates.sh
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	e8763af5ff6f763104076c3817eb8fae
URL:		https://jless.io/
BuildRequires:	cargo
BuildRequires:	libxcb-devel
BuildRequires:	python3
BuildRequires:	python3-modules
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JLess is a command-line JSON viewer designed for reading, exploring,
and searching through JSON data.

JLess will pretty print your JSON and apply syntax highlighting. Use
it when exploring external APIs, or debugging request payloads.

Expand and collapse Objects and Arrays to grasp the high- and
low-level structure of a JSON document. JLess has a large suite of
vim-inspired commands that make exploring data a breeze.

JLess supports full text regular-expression based search. Quickly find
the data you're looking for in long String values, or jump between
values for the same Object key.

%prep
%setup -q -a1

%{__mv} jless-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md SEARCH.md
%attr(755,root,root) %{_bindir}/jless
