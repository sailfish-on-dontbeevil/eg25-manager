Name:       eg25-manager
Summary:    EG25 Modem Manager Daemon
Version:    0.3.1
Release:    1
License:    LICENSE
URL:        https://gitlab.com/mobian1/devices/eg25-manager
Source0:    %{name}-%{version}.tar.bz2
Source1:    %{name}.service
Patch7:     0008-gnss-add-GNSS-assistance-support.patch
Patch6:     0007-at-allow-custom-callbacks-for-AT-command-response-pr.patch
Patch5:     0006-at-log-expected-result-before-setting-it-to-NULL.patch
Patch4:     0005-at-make-next_at_command-send_at_command-process_at_r.patch
Patch3:     0004-at-g_free-doesn-t-require-NULL-checking.patch
Patch2:     0003-at-fast-poweroff-is-only-available-in-newer-firmware.patch
Patch1:     0002-config-synchronize-with-modem-power.patch
Patch0:     0001-mm-iface-clean-out-modem_iface-if-mm-disappears.patch

BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(libgpiod)
BuildRequires:  libgudev-devel
BuildRequires:  pkgconfig(libusb)
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  cmake
BuildRequires:  systemd
BuildRequires:  libcurl-devel

%description
eg25-manager is a daemon for managing the Quectel EG25 modem found on the Pine64 PinePhone.

%prep
%setup -q -n %{name}-%{version}/%{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

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
