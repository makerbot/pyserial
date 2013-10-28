Name:		mb_pyserial
Version:	$pyserial
Release:	1%{?dist}
Summary:	Modified pyserial for MakerBot Conveyor

License:	BSD
URL:		http://github.com/makerbot/pyserial
Source:		pyserial-%{version}.tar.gz

BuildRequires:	python >= 2.7
Requires:	python >= 2.7

%description
Includes new logic for autodetecting usb serial devices.

%prep
%setup -q -n pyserial


%build
scons --install-prefix=%{buildroot}/%{_prefix} 

%install
rm -rf %{buildroot}
scons --install-prefix=%{buildroot}/%{_prefix} install


%files
%{_datarootdir}/makerbot/python/*


%changelog
