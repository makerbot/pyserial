Name:		mb_pyserial
Version:	2.0.0
Release:	1%{?dist}
Summary:	Modified pyserial for MakerBot Conveyor

License:	BSD
URL:		http://github.com/makerbot/pyserial
Source:		%{name}-%{version}.tar.gz

BuildRequires:	python >= 2.7
Requires:	python >= 2.7

%description
Includes new logic for autodetecting usb serial devices.

%prep
%setup -q -n pyserial


%build
scons install_prefix=%{buildroot}/%{_prefix} config_prefix=%{buildroot}/%{_sysconfdir}

%install
rm -rf %{buildroot}
scons install_prefix=%{buildroot}/%{_prefix} config_prefix=%{buildroot}/%{_sysconfdir} install


%files
%{_datarootdir}/makerbot/python/


%changelog
