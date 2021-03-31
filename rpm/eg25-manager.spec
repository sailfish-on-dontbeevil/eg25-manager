Name:       eg25-manager
Summary:    EG25 Modem Manager Daemon
Version:    0.2.1
Release:    1
License:    LICENSE
URL:        https://gitlab.com/mobian1/devices/eg25-manager
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(libgpiod)
BuildRequires:  libgudev-devel
BuildRequires:  pkgconfig(libusb)
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  cmake

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

%files
%defattr(-,root,root,-)
%{_bindir}/eg25manager
%{_bindir}/eg25-configure-usb
%{_libdir}/udev/rules.d/80-modem-eg25.rules
%{_datadir}/eg25-manager/pine64,pinephone-1.0.toml
%{_datadir}/eg25-manager/pine64,pinephone-1.1.toml
%{_datadir}/eg25-manager/pine64,pinephone-1.2.toml
