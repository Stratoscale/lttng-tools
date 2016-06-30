Name:           lttng-tools
Version:        2.8.0
Release:        1%{?dist}
Summary:        LTTng Trace Control
Requires:       popt >= 1.13, libuuid1, libxml2 >= 2.7.6, lttng-ust >= 2.8.0, lttng-ust < 2.9.0, liburcu >= 0.8.4

Group:          Development/Tools
License:        LGPLv2.1 and GPLv2
URL:            http://www.lttng.org
Source0:        http://lttng.org/files/lttng-tools/%{name}-%{version}.tar.bz2
Source1:        lttng-sessiond.service
Source2:        lttng-relayd.service
BuildRequires:  libtool, autoconf, automake, pkgconfig, liburcu-devel >= 0.8.4, libxml2-devel >= 2.7.6, libuuid-devel, lttng-ust-devel >= 2.8.0, lttng-ust-devel < 2.9.0, popt-devel >= 1.13, %{?systemd_requires}
%systemd_requires

%description
Utilities to control the LTTng kernel and userspace tracers.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing applications that use liblttng-ctl.

%package -n     python3-lttng
Summary:        Python bindings for lttng-tools
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}, python3
BuildRequires:  python3-devel, swig >= 2.0

%description -n python3-lttng
The python3-%{name} package contains the python bindings to lttng-tools.

%prep
%setup -q

%build
export PYTHON=python%{py3_ver}
export PYTHON_CONFIG=python%{py3_ver}-config
%configure --docdir=%{_docdir}/%{name} --enable-python-bindings
V=1 make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -vf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -vf $RPM_BUILD_ROOT%{python3_sitearch}/_lttng.a
rm -vf $RPM_BUILD_ROOT%{python3_sitearch}/_lttng.la
rm -vf $RPM_BUILD_ROOT%{python3_sitelib}/__pycache__/*
install -D -m644 extras/lttng-bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/lttng
install -D -m644 %{SOURCE1} %{buildroot}%{_unitdir}/lttng-sessiond.service
install -D -m644 %{SOURCE2} %{buildroot}%{_unitdir}/lttng-relayd.service

%pre
%service_add_pre lttng-sessiond.service lttng-relayd.service
getent group tracing >/dev/null || groupadd -r tracing
exit 0

%post
/sbin/ldconfig
%service_add_post lttng-sessiond.service lttng-relayd.service

%preun
%service_del_preun lttng-sessiond.service lttng-relayd.service

%postun
/sbin/ldconfig
%service_del_postun lttng-sessiond.service lttng-relayd.service

%files
%{_mandir}/man1/lttng.1.gz
%{_mandir}/man1/lttng-add-context.1.gz
%{_mandir}/man1/lttng-calibrate.1.gz
%{_mandir}/man1/lttng-crash.1.gz
%{_mandir}/man1/lttng-create.1.gz
%{_mandir}/man1/lttng-destroy.1.gz
%{_mandir}/man1/lttng-disable-channel.1.gz
%{_mandir}/man1/lttng-disable-event.1.gz
%{_mandir}/man1/lttng-enable-channel.1.gz
%{_mandir}/man1/lttng-enable-event.1.gz
%{_mandir}/man1/lttng-help.1.gz
%{_mandir}/man1/lttng-list.1.gz
%{_mandir}/man1/lttng-load.1.gz
%{_mandir}/man1/lttng-metadata.1.gz
%{_mandir}/man1/lttng-save.1.gz
%{_mandir}/man1/lttng-set-session.1.gz
%{_mandir}/man1/lttng-snapshot.1.gz
%{_mandir}/man1/lttng-start.1.gz
%{_mandir}/man1/lttng-status.1.gz
%{_mandir}/man1/lttng-stop.1.gz
%{_mandir}/man1/lttng-track.1.gz
%{_mandir}/man1/lttng-untrack.1.gz
%{_mandir}/man1/lttng-version.1.gz
%{_mandir}/man1/lttng-view.1.gz
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
%{_bindir}/lttng-crash
%{_bindir}/lttng-sessiond
%{_bindir}/lttng-relayd
%{_libdir}/lttng/libexec/lttng-consumerd
%{_libdir}/liblttng-ctl.so.*
%{_unitdir}/lttng-sessiond.service
%{_unitdir}/lttng-relayd.service
%{_sysconfdir}/bash_completion.d/
%{_datadir}/xml/lttng/session.xsd

%files devel
%{_mandir}/man3/lttng-health-check.3.gz
%{_defaultdocdir}/%{name}/python-howto.txt
%{_defaultdocdir}/%{name}/live-reading-protocol.txt
%{_defaultdocdir}/%{name}/valgrind-howto.txt
%{_includedir}/*
%{_libdir}/liblttng-ctl.a
%{_libdir}/liblttng-ctl.so
%{_libdir}/pkgconfig/lttng-ctl.pc

%files -n python3-lttng
%{python3_sitelib}/lttng.py
%{python3_sitearch}/_lttng.so*

%changelog
* Thu Jun 09 2016 Michael Jeanson <mjeanson@efficios.com> 2.8.0-1
    - Update to 2.8.0

* Fri Apr 22 2016 Michael Jeanson <mjeanson@efficios.com> 2.7.2-1
    - Update to 2.7.2

* Fri Jan 15 2016 Michael Jeanson <mjeanson@efficios.com> 2.7.1-1
    - Update to 2.7.1

* Fri Nov 13 2015 Michael Jeanson <mjeanson@efficios.com> 2.7.0-1
    - Update to 2.7.0

* Wed Jul 08 2015 Michael Jeanson <mjeanson@efficios.com> 2.6.0-1
    - Initial revision.
