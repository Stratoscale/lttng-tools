Name:           lttng-tools
Version:        2.6.0
Release:        1%{?dist}
Summary:        LTTng Trace Control
Requires:       popt >= 1.13, libuuid, libxml2 >= 2.7.6, lttng-ust >= 2.6.0, lttng-ust < 2.7.0, liburcu >= 0.8.0

Group:          Development/Tools
License:        LGPLv2.1 and GPLv2
URL:            http://www.lttng.org
Source0:        http://lttng.org/files/lttng-tools/%{name}-%{version}.tar.bz2
Source1:        lttng-sessiond.service
Source2:        lttng-relayd.service
Patch0:         missing-files.patch
BuildRequires:  libtool, autoconf, automake, pkgconfig, liburcu-devel >= 0.7.2, libxml2-devel >= 2.7.6, libuuid-devel, lttng-ust-devel >= 2.6.0, lttng-ust-devel < 2.7.0, popt-devel >= 1.13
Requires(pre):  shadow-utils
%systemd_requires

%description
Utilities to control the LTTng kernel and userspace tracers.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing applications that use liblttng-ctl.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static --docdir=%{_docdir}/%{name} --with-java-jdk=${JAVA_SDK_PATH}
V=1 make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -vf $RPM_BUILD_ROOT%{_libdir}/*.la
install -D -m644 extras/lttng-bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/lttng
install -D -m644 %{SOURCE1} %{buildroot}%{_unitdir}/lttng-sessiond.service
install -D -m644 %{SOURCE2} %{buildroot}%{_unitdir}/lttng-relayd.service

%pre
getent group tracing >/dev/null || groupadd -r tracing
exit 0

%post
/sbin/ldconfig

%systemd_post lttng-sessiond.service, lttng-relayd.service

%preun
%systemd_preun lttng-sessiond.service, lttng-relayd.service

%postun
/sbin/ldconfig
# Use %systemd_postun instead of %systemd_postun_with_restart
# since we don't want to automatically restard these daemons on
# upgrade (which would clear the currently active sessions).
%systemd_postun lttng-sessiond.service, lttng-relayd.service

%files
%{_mandir}/man1/lttng.1.gz
%{_mandir}/man8/lttng-relayd.8.gz
%{_mandir}/man8/lttng-sessiond.8.gz
%{_defaultdocdir}/%{name}/LICENSE
%{_defaultdocdir}/%{name}/README.md
%{_defaultdocdir}/%{name}/ChangeLog
%{_defaultdocdir}/%{name}/calibrate.txt
%{_defaultdocdir}/%{name}/live-reading-howto.txt
%{_defaultdocdir}/%{name}/quickstart.txt
%{_defaultdocdir}/%{name}/snapshot-howto.txt
%{_defaultdocdir}/%{name}/streaming-howto.txt
%{_bindir}/lttng
%{_bindir}/lttng-sessiond
%{_bindir}/lttng-relayd
%{_libdir}/lttng/libexec/lttng-consumerd
%{_libdir}/liblttng-ctl.so.*
%{_unitdir}/lttng-sessiond.service
%{_unitdir}/lttng-relayd.service
%{_sysconfdir}/bash_completion.d/
%{_datadir}/xml/lttng/session.xsd

%files devel
# Only include this file once we provide a -python package
%exclude %{_defaultdocdir}/%{name}/python-howto.txt
%{_defaultdocdir}/%{name}/live-reading-protocol.txt
%{_defaultdocdir}/%{name}/valgrind-howto.txt
%{_includedir}/*
%{_libdir}/liblttng-ctl.so
%{_libdir}/pkgconfig/lttng-ctl.pc

%changelog
* Mon Jun 22 2015 Michael Jeanson <mjeanson@efficios.com> 2.6.0-1
    - Initial revision.
