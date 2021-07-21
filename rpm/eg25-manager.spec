Name:       eg25-manager
Summary:    EG25 Modem Manager Daemon
Version:    0.3.1
Release:    1
License:    LICENSE
URL:        https://gitlab.com/mobian1/devices/eg25-manager
Source0:    %{name}-%{version}.tar.bz2
Source1:    %{name}.service
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(libgpiod)
BuildRequires:  libgudev-devel
BuildRequires:  pkgconfig(libusb)
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  cmake
BuildRequires:  systemd

%description
eg25-manager is a daemon for managing the Quectel EG25 modem found on the Pine64 PinePhone.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
%meson
%meson_build

%install
rm -rf %{buildroot}
%meson_install
install -D -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/%{name}.service
mkdir -p %{buildroot}%{_udevrulesdir}/
mv %{buildroot}/usr/lib/udev/rules.d/80-modem-eg25.rules %{buildroot}%{_udevrulesdir}/80-modem-eg25.rules
mkdir -p %{buildroot}/%{_unitdir}/basic.target.wants
ln -s ../%{name}.service %{buildroot}/%{_unitdir}/basic.target.wants/%{name}.service

%preun
if [ "$1" -eq 0 ]; then
systemctl stop %{name}.service || :
fi

%post
/sbin/ldconfig
systemctl daemon-reload || :
systemctl reload-or-try-restart %{name}.service || :

%postun
/sbin/ldconfig
systemctl daemon-reload || :

%files
%defattr(-,root,root,-)
%{_bindir}/eg25manager
%{_udevrulesdir}/80-modem-eg25.rules
%{_unitdir}/%{name}.service
%{_unitdir}/basic.target.wants/%{name}.service
%{_datadir}/eg25-manager/pine64,pinephone-1.0.toml
%{_datadir}/eg25-manager/pine64,pinephone-1.1.toml
%{_datadir}/eg25-manager/pine64,pinephone-1.2.toml
