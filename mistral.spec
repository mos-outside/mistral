%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%global release_name liberty
%global release_ver liberty-rc1

Name:           openstack-mistral
Version:        XXX
Release:        XXX
Summary:        Task Orchestration and Scheduling service for OpenStack cloud
Group:          Development/Libraries
License:        Apache License, Version 2.0
URL:            https://launchpad.net/mistral
Source0:        https://launchpad.net/mistral/%{release_name}/%{release_ver}/+download/mistral-%{version}.tar.gz
Source1:        mistral-api.init
Source2:        mistral-engine.init
Source3:        mistral-executor.init
# Systemd scripts
Source10:       mistral-api.service
Source11:       mistral-engine.service
Source12:	      mistral-executor.service

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-oslo-config >= 2:2.3.0
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 1.6
BuildRequires:  systemd

%description
System package - mistral
Python package - mistral

%package -n     python-%{name}

Summary:        Mistral Python libraries

Requires:       python-alembic >= 0.8.0
Requires:       python-babel >= 1.3
Requires:       python-croniter >= 0.3.4
Requires:       python-eventlet >= 0.17.4
Requires:       python-iso8601 >= 0.1.9
Requires:       python-jsonschema >= 2.0.0
Requires:       python-keystonemiddleware >= 2.0.0
Requires:       python-kombu >= 3.0.7
Requires:       python-mock >= 1.2
Requires:       python-networkx >= 1.10
Requires:       python-oslo-concurrency >= 2.3.0
Requires:       python-oslo-config >= 2:2.3.0
Requires:       python-oslo-db >= 2.4.1
Requires:       python-oslo-messaging >= 1.16.0
Requires:       python-oslo-utils >= 2.0.0
Requires:       python-oslo-log >= 1.8.0
Requires:       python-oslo-serialization >= 1.4.0
Requires:       python-oslo-service >= 0.7.0
Requires:       python-paramiko >= 1.13.0
Requires:       python-pbr >= 1.6
Requires:       python-pecan >= 1.0.0
Requires:       python-cinderclient >= 1.3.1
Requires:       python-glanceclient >= 1:0.18.0
Requires:       python-heatclient >= 0.3.0
Requires:       python-keystoneclient >= 1:1.6.0
Requires:       python-neutronclient >= 2.6.0
Requires:       python-novaclient >= 1:2.28.1
Requires:       PyYAML >= 3.1.0
Requires:       python-requests >= 2.5.2
Requires:       python-retrying >= 1.2.3
Requires:       python-six >= 1.9.0
Requires:       python-sqlalchemy >= 0.9.9 , python-sqlalchemy < 1.1.0
Requires:       python-stevedore >= 1.5.0
Requires:       python-wsme >= 0.7
Requires:       python-yaql >= 1.0.0
Requires:       python-tooz >= 1.19.0

%description -n python-%{name}
Mistral is a workflow service.
Most business processes consist of multiple distinct interconnected steps that need to be executed in a particular order
in a distributed environment. One can describe such process as a set of tasks and task relations and upload such description
to Mistral so that it takes care of state management, correct execution order, parallelism, synchronization and high availability.
.
This package contains the Python libraries.

%package        common

Summary: Components common for OpenStack Mistral

Requires:       python-%{name} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description    common
Mistral is a workflow service.
Most business processes consist of multiple distinct interconnected steps that need to be executed in a particular order
in a distributed environment. One can describe such process as a set of tasks and task relations and upload such description
to Mistral so that it takes care of state management, correct execution order, parallelism, synchronization and high availability.
.
This package contains the common files.

%package        api

Summary: OpenStack Mistral API daemon

Requires:       %{name}-common = %{version}-%{release}

%description    api
OpenStack rest API to the Mistral Engine.
.
This package contains the ReST API.

%package        engine

Summary: OpenStack Mistral Engine daemon

Requires:       %{name}-common = %{version}-%{release}

%description    engine
OpenStack Mistral Engine service.
.
This package contains the mistral engine, which is one of core services of mistral.

%package        executor

Summary: OpenStack Mistral Executor daemon

Requires:       %{name}-common = %{version}-%{release}

%description    executor
OpenStack Mistral Executor service.
.
This package contains the mistral executor, which is one of core services of mistral, and
which the API servers will use.


%package        doc

Summary:        Documentation for OpenStack Workflow Service

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-sphinxcontrib-httpdomain
BuildRequires:  python-sphinxcontrib-pecanwsme
BuildRequires:  python2-wsme
BuildRequires:  python-oslo-log
BuildRequires:  python-pecan
BuildRequires:  python-oslo-db
BuildRequires:  python-eventlet
BuildRequires:  python-keystoneclient
BuildRequires:  python-oslo-messaging
BuildRequires:  python-jsonschema
BuildRequires:  python-yaql
BuildRequires:  python-networkx

%description    doc
OpenStack Mistral documentaion.
.
This package contains the documentation

%prep
%setup -q -n mistral-%{upstream_version}
sed -i '1i #!/usr/bin/python' tools/sync_db.py

rm -rf mistral.egg-info
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python} setup.py build
oslo-config-generator --config-file tools/config/config-generator.mistral.conf \
                      --output-file etc/mistral.conf.sample

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd

mkdir -p %{buildroot}/etc/mistral/
mkdir -p %{buildroot}/var/log/mistral
mkdir -p %{buildroot}/var/run/mistral

%if 0%{?rhel} == 6
install -p -D -m 755 %SOURCE1 %{buildroot}%{_initrddir}/openstack-mistral-api
install -p -D -m 755 %SOURCE2 %{buildroot}%{_initrddir}/openstack-mistral-engine
install -p -D -m 755 %SOURCE3 %{buildroot}%{_initrddir}/openstack-mistral-executor
%else
install -p -D -m 644 %SOURCE10 %{buildroot}%{_unitdir}/openstack-mistral-api.service
install -p -D -m 644 %SOURCE11 %{buildroot}%{_unitdir}/openstack-mistral-engine.service
install -p -D -m 644 %SOURCE12 %{buildroot}%{_unitdir}/openstack-mistral-executor.service
%endif

install -p -D -m 640 etc/mistral.conf.sample \
                     %{buildroot}%{_sysconfdir}/mistral/mistral.conf
install -p -D -m 640 etc/logging.conf.sample \
                     %{buildroot}%{_sysconfdir}/mistral/logging.conf
install -p -D -m 640 etc/wf_trace_logging.conf.sample \
                     %{buildroot}%{_sysconfdir}/mistral/wf_trace_logging.conf
install -p -D -m 640 tools/sync_db.py \
                     %{buildroot}/usr/bin/mistral-db-sync
chmod +x %{buildroot}/usr/bin/mistral*

%if 0%{?rhel} == 6
chmod +x %{buildroot}%{_initrddir}/openstack-mistral-api
chmod +x %{buildroot}%{_initrddir}/openstack-mistral-engine
chmod +x %{buildroot}%{_initrddir}/openstack-mistral-executor
%endif

%pre common
USERNAME=mistral
GROUPNAME=$USERNAME
HOMEDIR=/home/$USERNAME
getent group $GROUPNAME >/dev/null || groupadd -r $GROUPNAME
getent passwd $USERNAME >/dev/null ||
    useradd -r -g $GROUPNAME -G $GROUPNAME -d $HOMEDIR -s /sbin/nologin \
            -c "Mistral Daemons" $USERNAME
exit 0


%clean
rm -rf %{buildroot}

%post api
%systemd_post openstack-mistral-api.service
%preun api
%systemd_preun openstack-mistral-api.service
%postun api
%systemd_postun_with_restart openstack-mistral-api.service

%post engine
%systemd_post openstack-mistral-engine.service
%preun engine
%systemd_preun openstack-mistral-engine.service
%postun engine
%systemd_postun_with_restart openstack-mistral-engine.service

%post executor
%systemd_post openstack-mistral-executor.service
%preun executor
%systemd_preun openstack-mistral-executor.service
%postun executor
%systemd_postun_with_restart openstack-mistral-executor.service

%files    api
%if 0%{?rhel} == 6
%config(noreplace) %attr(-, root, root) %{_initrddir}/openstack-mistral-api
%else
%config(noreplace) %attr(-, root, root) %{_unitdir}/openstack-mistral-api.service
%endif

%files   common
%dir %{_sysconfdir}/mistral
%config(noreplace) %attr(-, mistral, mistral) %{_sysconfdir}/mistral/*
%{_bindir}/mistral-*
%dir %attr(766, mistral, mistral) /var/run/mistral
%dir %attr(766, mistral, mistral) /var/log/mistral

%files doc
%doc doc/build/html

%files    engine
%if 0%{?rhel} == 6
%config(noreplace) %attr(-, root, root) %{_initrddir}/openstack-mistral-engine
%else
%config(noreplace) %attr(-, root, root) %{_unitdir}/openstack-mistral-engine.service
%endif

%files    executor
%if 0%{?rhel} == 6
%config(noreplace) %attr(-, root, root) %{_initrddir}/openstack-mistral-executor
%else
%config(noreplace) %attr(-, root, root) %{_unitdir}/openstack-mistral-executor.service
%endif

%files -n python-%{name}
%{python_sitelib}/

%changelog
