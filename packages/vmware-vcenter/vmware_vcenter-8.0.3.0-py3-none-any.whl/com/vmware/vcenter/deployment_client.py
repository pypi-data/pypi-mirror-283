# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.deployment.
#---------------------------------------------------------------------------

"""


"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from vmware.vapi.bindings import type
from vmware.vapi.bindings.converter import TypeConverter
from vmware.vapi.bindings.enum import Enum
from vmware.vapi.bindings.error import VapiError
from vmware.vapi.bindings.struct import VapiStruct
from vmware.vapi.bindings.stub import (
    ApiInterfaceStub, StubFactoryBase, VapiInterface)
from vmware.vapi.bindings.common import raise_core_exception
from vmware.vapi.data.validator import (UnionValidator, HasFieldsOfValidator)
from vmware.vapi.exception import CoreException
from vmware.vapi.lib.constants import TaskType
from vmware.vapi.lib.rest import OperationRestMetadata

class ApplianceType(Enum):
    """
    The ``ApplianceType`` class defines the vCenter appliance types. This
    enumeration was added in vSphere API 6.7.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    VCSA_EMBEDDED = None
    """
    vCenter Server Appliance with an embedded Platform Services Controller.
    This class attribute was added in vSphere API 6.7.

    """
    VCSA_EXTERNAL = None
    """
    vCenter Server Appliance with an external Platform Services Controller.
    This class attribute was added in vSphere API 6.7.

    """
    PSC_EXTERNAL = None
    """
    An external Platform Services Controller. This class attribute was added in
    vSphere API 6.7.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`ApplianceType` instance.
        """
        Enum.__init__(string)

ApplianceType._set_values({
    'VCSA_EMBEDDED': ApplianceType('VCSA_EMBEDDED'),
    'VCSA_EXTERNAL': ApplianceType('VCSA_EXTERNAL'),
    'PSC_EXTERNAL': ApplianceType('PSC_EXTERNAL'),
})
ApplianceType._set_binding_type(type.EnumType(
    'com.vmware.vcenter.deployment.appliance_type',
    ApplianceType))



class ApplianceState(Enum):
    """
    The ``ApplianceState`` class defines the various states the vCenter
    Appliance can be in. This enumeration was added in vSphere API 6.7.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    NOT_INITIALIZED = None
    """
    The appliance is in the process of being initialized and not ready for
    configuration. This class attribute was added in vSphere API 6.7.

    """
    INITIALIZED = None
    """
    The appliance is initialized and ready to be configured. This class
    attribute was added in vSphere API 6.7.

    """
    CONFIG_IN_PROGRESS = None
    """
    The appliance is in the process of being configured. This class attribute
    was added in vSphere API 6.7.

    """
    QUESTION_RAISED = None
    """
    The deployment script has raised a question and is waiting for an answer to
    continue with the appliance configuration. This class attribute was added
    in vSphere API 6.7.

    """
    FAILED = None
    """
    The appliance configuration has failed. This class attribute was added in
    vSphere API 6.7.

    """
    CONFIGURED = None
    """
    The appliance has been configured. This class attribute was added in
    vSphere API 6.7.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`ApplianceState` instance.
        """
        Enum.__init__(string)

ApplianceState._set_values({
    'NOT_INITIALIZED': ApplianceState('NOT_INITIALIZED'),
    'INITIALIZED': ApplianceState('INITIALIZED'),
    'CONFIG_IN_PROGRESS': ApplianceState('CONFIG_IN_PROGRESS'),
    'QUESTION_RAISED': ApplianceState('QUESTION_RAISED'),
    'FAILED': ApplianceState('FAILED'),
    'CONFIGURED': ApplianceState('CONFIGURED'),
})
ApplianceState._set_binding_type(type.EnumType(
    'com.vmware.vcenter.deployment.appliance_state',
    ApplianceState))



class ApplianceSize(Enum):
    """
    The ``ApplianceSize`` class defines the vCenter Server Appliance sizes.
    This enumeration was added in vSphere API 7.0.0.0.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    TINY = None
    """
    Appliance size of 'tiny'. This class attribute was added in vSphere API
    7.0.0.0.

    """
    SMALL = None
    """
    Appliance size of 'small'. This class attribute was added in vSphere API
    7.0.0.0.

    """
    MEDIUM = None
    """
    Appliance size of 'medium'. This class attribute was added in vSphere API
    7.0.0.0.

    """
    LARGE = None
    """
    Appliance size of 'large'. This class attribute was added in vSphere API
    7.0.0.0.

    """
    XLARGE = None
    """
    Appliance size of 'extra large'. This class attribute was added in vSphere
    API 7.0.0.0.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`ApplianceSize` instance.
        """
        Enum.__init__(string)

ApplianceSize._set_values({
    'TINY': ApplianceSize('TINY'),
    'SMALL': ApplianceSize('SMALL'),
    'MEDIUM': ApplianceSize('MEDIUM'),
    'LARGE': ApplianceSize('LARGE'),
    'XLARGE': ApplianceSize('XLARGE'),
})
ApplianceSize._set_binding_type(type.EnumType(
    'com.vmware.vcenter.deployment.appliance_size',
    ApplianceSize))



class Operation(Enum):
    """
    The ``Operation`` class defines the supported vCenter appliance deployment
    operations. This enumeration was added in vSphere API 6.7.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    INSTALL = None
    """
    The appliance installation is in progress. This class attribute was added
    in vSphere API 6.7.

    """
    UPGRADE = None
    """
    The appliance upgrade is in progress. This class attribute was added in
    vSphere API 6.7.

    """
    MIGRATE = None
    """
    The appliance migration is in progress. This class attribute was added in
    vSphere API 6.7.

    """
    RESTORE = None
    """
    The appliance restoration is in progress. This class attribute was added in
    vSphere API 6.7.

    """
    ROLLBACK = None
    """
    The appliance is being rolled back to an unconfigured state. This class
    attribute was added in vSphere API 6.7.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`Operation` instance.
        """
        Enum.__init__(string)

Operation._set_values({
    'INSTALL': Operation('INSTALL'),
    'UPGRADE': Operation('UPGRADE'),
    'MIGRATE': Operation('MIGRATE'),
    'RESTORE': Operation('RESTORE'),
    'ROLLBACK': Operation('ROLLBACK'),
})
Operation._set_binding_type(type.EnumType(
    'com.vmware.vcenter.deployment.operation',
    Operation))



class VerificationMode(Enum):
    """
    The ``VerificationMode`` class defines the verification modes for SSL
    certificates or SSH connections. This enumeration was added in vSphere API
    6.7.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    NONE = None
    """
    No verification will be performed. This class attribute was added in
    vSphere API 6.7.

    """
    THUMBPRINT = None
    """
    Passed thumbprint will be used for verification. This class attribute was
    added in vSphere API 6.7.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`VerificationMode` instance.
        """
        Enum.__init__(string)

VerificationMode._set_values({
    'NONE': VerificationMode('NONE'),
    'THUMBPRINT': VerificationMode('THUMBPRINT'),
})
VerificationMode._set_binding_type(type.EnumType(
    'com.vmware.vcenter.deployment.verification_mode',
    VerificationMode))



class CheckStatus(Enum):
    """
    The ``CheckStatus`` class defines the status of the checks. This
    enumeration was added in vSphere API 6.7.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    SUCCESS = None
    """
    All checks have completed successfully. This class attribute was added in
    vSphere API 6.7.

    """
    FAILED = None
    """
    A fatal error was encountered when running the sanity checks. This class
    attribute was added in vSphere API 6.7.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`CheckStatus` instance.
        """
        Enum.__init__(string)

CheckStatus._set_values({
    'SUCCESS': CheckStatus('SUCCESS'),
    'FAILED': CheckStatus('FAILED'),
})
CheckStatus._set_binding_type(type.EnumType(
    'com.vmware.vcenter.deployment.check_status',
    CheckStatus))



class HistoryMigrationOption(Enum):
    """
    The ``HistoryMigrationOption`` class defines the vCenter history migration
    option choices. This enumeration was added in vSphere API 6.7.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    EVENTS_TASKS = None
    """
    Only event data and task data will be migrated along with the core data.
    This class attribute was added in vSphere API 6.7.

    """
    ALL = None
    """
    All history data will be migrated along with the core data. This class
    attribute was added in vSphere API 6.7.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`HistoryMigrationOption` instance.
        """
        Enum.__init__(string)

HistoryMigrationOption._set_values({
    'EVENTS_TASKS': HistoryMigrationOption('EVENTS_TASKS'),
    'ALL': HistoryMigrationOption('ALL'),
})
HistoryMigrationOption._set_binding_type(type.EnumType(
    'com.vmware.vcenter.deployment.history_migration_option',
    HistoryMigrationOption))




class Notification(VapiStruct):
    """
    The ``Notification`` class contains attributes to describe any
    info/warning/error messages that Tasks can raise. This class was added in
    vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 id=None,
                 time=None,
                 message=None,
                 resolution=None,
                ):
        """
        :type  id: :class:`str`
        :param id: The notification id. This attribute was added in vSphere API 6.7.
        :type  time: :class:`datetime.datetime` or ``None``
        :param time: The time the notification was raised/found. This attribute was
            added in vSphere API 6.7.
            Only :class:`set` if the time information is available.
        :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param message: The notification message. This attribute was added in vSphere API
            6.7.
        :type  resolution: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
        :param resolution: The resolution message, if any. This attribute was added in vSphere
            API 6.7.
            Only :class:`set` for warnings and errors.
        """
        self.id = id
        self.time = time
        self.message = message
        self.resolution = resolution
        VapiStruct.__init__(self)


Notification._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.notification', {
        'id': type.StringType(),
        'time': type.OptionalType(type.DateTimeType()),
        'message': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'resolution': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
    },
    Notification,
    False,
    None))



class Notifications(VapiStruct):
    """
    The ``Notifications`` class contains info/warning/error messages that can
    be reported be the task. This class was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 info=None,
                 warnings=None,
                 errors=None,
                ):
        """
        :type  info: :class:`list` of :class:`Notification` or ``None``
        :param info: Info notification messages reported. This attribute was added in
            vSphere API 6.7.
            Only :class:`set` if an info was reported by the task.
        :type  warnings: :class:`list` of :class:`Notification` or ``None``
        :param warnings: Warning notification messages reported. This attribute was added in
            vSphere API 6.7.
            Only :class:`set` if an warning was reported by the task.
        :type  errors: :class:`list` of :class:`Notification` or ``None``
        :param errors: Error notification messages reported. This attribute was added in
            vSphere API 6.7.
            Only :class:`set` if an error was reported by the task.
        """
        self.info = info
        self.warnings = warnings
        self.errors = errors
        VapiStruct.__init__(self)


Notifications._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.notifications', {
        'info': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'warnings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
    },
    Notifications,
    False,
    None))



class StandaloneSpec(VapiStruct):
    """
    The ``StandaloneSpec`` class contains information used to configure a
    standalone embedded vCenter Server appliance. This class was added in
    vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 sso_admin_password=None,
                 sso_domain_name=None,
                ):
        """
        :type  sso_admin_password: :class:`str`
        :param sso_admin_password: The SSO administrator account password. This attribute was added in
            vSphere API 6.7.
        :type  sso_domain_name: :class:`str` or ``None``
        :param sso_domain_name: The SSO domain name to be used to configure this appliance. This
            attribute was added in vSphere API 6.7.
            If None, vsphere.local will be used.
        """
        self.sso_admin_password = sso_admin_password
        self.sso_domain_name = sso_domain_name
        VapiStruct.__init__(self)


StandaloneSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.standalone_spec', {
        'sso_admin_password': type.StringType(),
        'sso_domain_name': type.OptionalType(type.StringType()),
    },
    StandaloneSpec,
    False,
    None))



class StandalonePscSpec(VapiStruct):
    """
    The ``StandalonePscSpec`` class contains information used to configure a
    standalone PSC appliance. This class was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 sso_site_name=None,
                 sso_admin_password=None,
                 sso_domain_name=None,
                ):
        """
        :type  sso_site_name: :class:`str` or ``None``
        :param sso_site_name: The SSO site name used for this PSC. This attribute was added in
            vSphere API 6.7.
            If None, default-first-site will be used.
        :type  sso_admin_password: :class:`str`
        :param sso_admin_password: The SSO administrator account password. This attribute was added in
            vSphere API 6.7.
        :type  sso_domain_name: :class:`str` or ``None``
        :param sso_domain_name: The SSO domain name to be used to configure this appliance. This
            attribute was added in vSphere API 6.7.
            If None, vsphere.local will be used.
        """
        self.sso_site_name = sso_site_name
        self.sso_admin_password = sso_admin_password
        self.sso_domain_name = sso_domain_name
        VapiStruct.__init__(self)


StandalonePscSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.standalone_psc_spec', {
        'sso_site_name': type.OptionalType(type.StringType()),
        'sso_admin_password': type.StringType(),
        'sso_domain_name': type.OptionalType(type.StringType()),
    },
    StandalonePscSpec,
    False,
    None))



class ReplicatedSpec(VapiStruct):
    """
    The ``ReplicatedSpec`` class contains information used to check if the
    configuring vCenter Server can be replicated to the remote PSC. This class
    was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 partner_hostname=None,
                 https_port=None,
                 sso_admin_password=None,
                 ssl_thumbprint=None,
                 ssl_verify=None,
                ):
        """
        :type  partner_hostname: :class:`str`
        :param partner_hostname: The IP address or DNS resolvable name of the partner PSC appliance.
            This attribute was added in vSphere API 6.7.
        :type  https_port: :class:`long` or ``None``
        :param https_port: The HTTPS port of the external PSC appliance. This attribute was
            added in vSphere API 6.7.
            If None, port 443 will be used.
        :type  sso_admin_password: :class:`str`
        :param sso_admin_password: The SSO administrator account password. This attribute was added in
            vSphere API 6.7.
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SHA1 thumbprint of the server SSL certificate will be used for
            verification. This attribute was added in vSphere API 6.7.
            This attribute is only relevant if ``sslVerify`` is None or has the
            value true.
        :type  ssl_verify: :class:`bool` or ``None``
        :param ssl_verify: SSL verification should be enabled or disabled. This attribute was
            added in vSphere API 6.7.
            If None, ssl_verify true will be used.
        """
        self.partner_hostname = partner_hostname
        self.https_port = https_port
        self.sso_admin_password = sso_admin_password
        self.ssl_thumbprint = ssl_thumbprint
        self.ssl_verify = ssl_verify
        VapiStruct.__init__(self)


ReplicatedSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.replicated_spec', {
        'partner_hostname': type.StringType(),
        'https_port': type.OptionalType(type.IntegerType()),
        'sso_admin_password': type.StringType(),
        'ssl_thumbprint': type.OptionalType(type.StringType()),
        'ssl_verify': type.OptionalType(type.BooleanType()),
    },
    ReplicatedSpec,
    False,
    None))



class ReplicatedPscSpec(VapiStruct):
    """
    The ``ReplicatedPscSpec`` class contains information used to check if the
    configuring PSC can be replicated to the remote PSC. This class was added
    in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 sso_site_name=None,
                 partner_hostname=None,
                 https_port=None,
                 sso_admin_password=None,
                 ssl_thumbprint=None,
                 ssl_verify=None,
                ):
        """
        :type  sso_site_name: :class:`str` or ``None``
        :param sso_site_name: The SSO sitename that will be used in PSC replication. This
            attribute was added in vSphere API 6.7.
            If None, default-first-site will be used.
        :type  partner_hostname: :class:`str`
        :param partner_hostname: The IP address or DNS resolvable name of the partner PSC appliance.
            This attribute was added in vSphere API 6.7.
        :type  https_port: :class:`long` or ``None``
        :param https_port: The HTTPS port of the external PSC appliance. This attribute was
            added in vSphere API 6.7.
            If None, port 443 will be used.
        :type  sso_admin_password: :class:`str`
        :param sso_admin_password: The SSO administrator account password. This attribute was added in
            vSphere API 6.7.
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SHA1 thumbprint of the server SSL certificate will be used for
            verification. This attribute was added in vSphere API 6.7.
            This attribute is only relevant if ``sslVerify`` is None or has the
            value true.
        :type  ssl_verify: :class:`bool` or ``None``
        :param ssl_verify: SSL verification should be enabled or disabled. This attribute was
            added in vSphere API 6.7.
            If None, ssl_verify true will be used.
        """
        self.sso_site_name = sso_site_name
        self.partner_hostname = partner_hostname
        self.https_port = https_port
        self.sso_admin_password = sso_admin_password
        self.ssl_thumbprint = ssl_thumbprint
        self.ssl_verify = ssl_verify
        VapiStruct.__init__(self)


ReplicatedPscSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.replicated_psc_spec', {
        'sso_site_name': type.OptionalType(type.StringType()),
        'partner_hostname': type.StringType(),
        'https_port': type.OptionalType(type.IntegerType()),
        'sso_admin_password': type.StringType(),
        'ssl_thumbprint': type.OptionalType(type.StringType()),
        'ssl_verify': type.OptionalType(type.BooleanType()),
    },
    ReplicatedPscSpec,
    False,
    None))



class RemotePscSpec(VapiStruct):
    """
    The ``RemotePscSpec`` class contains information used to configure an
    external vCenter Server that registers with a remote PSC. This class was
    added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 psc_hostname=None,
                 https_port=None,
                 sso_admin_password=None,
                 ssl_thumbprint=None,
                 ssl_verify=None,
                ):
        """
        :type  psc_hostname: :class:`str`
        :param psc_hostname: The IP address or DNS resolvable name of the remote PSC to which
            this configuring vCenter Server will be registered to. This
            attribute was added in vSphere API 6.7.
        :type  https_port: :class:`long` or ``None``
        :param https_port: The HTTPS port of the external PSC appliance. This attribute was
            added in vSphere API 6.7.
            If None, port 443 will be used.
        :type  sso_admin_password: :class:`str`
        :param sso_admin_password: The SSO administrator account password. This attribute was added in
            vSphere API 6.7.
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SHA1 thumbprint of the server SSL certificate will be used for
            verification when ssl_verify field is set to true. This attribute
            was added in vSphere API 6.7.
            This attribute is only relevant if ``sslVerify`` is None or has the
            value true.
        :type  ssl_verify: :class:`bool` or ``None``
        :param ssl_verify: SSL verification should be enabled or disabled. If ``sslVerify`` is
            true and and ``sslThumbprint`` is None, the CA certificate will be
            used for verification. If ``sslVerify`` is true and
            ``sslThumbprint`` is set then the thumbprint will be used for
            verification. No verification will be performed if ``sslVerify``
            value is set to false. This attribute was added in vSphere API 6.7.
            If None, ``sslVerify`` true will be used.
        """
        self.psc_hostname = psc_hostname
        self.https_port = https_port
        self.sso_admin_password = sso_admin_password
        self.ssl_thumbprint = ssl_thumbprint
        self.ssl_verify = ssl_verify
        VapiStruct.__init__(self)


RemotePscSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.remote_psc_spec', {
        'psc_hostname': type.StringType(),
        'https_port': type.OptionalType(type.IntegerType()),
        'sso_admin_password': type.StringType(),
        'ssl_thumbprint': type.OptionalType(type.StringType()),
        'ssl_verify': type.OptionalType(type.BooleanType()),
    },
    RemotePscSpec,
    False,
    None))



class DataMigrationEstimate(VapiStruct):
    """
    The ``DataMigrationEstimate`` {class contains estimated time and disk space
    required for the vCenter Server database migration. This class was added in
    vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 estimated_export_time=None,
                 estimated_import_time=None,
                 required_free_disk_space_on_source=None,
                ):
        """
        :type  estimated_export_time: :class:`long`
        :param estimated_export_time: The time estimated to export data from the source vCenter Server.
            This attribute was added in vSphere API 7.0.0.0.
        :type  estimated_import_time: :class:`long`
        :param estimated_import_time: The time estimated to import data to the upgraded vCenter Server.
            This attribute was added in vSphere API 7.0.0.0.
        :type  required_free_disk_space_on_source: :class:`float`
        :param required_free_disk_space_on_source: The extra free space required on source vCenter Server. This
            attribute was added in vSphere API 7.0.0.0.
        """
        self.estimated_export_time = estimated_export_time
        self.estimated_import_time = estimated_import_time
        self.required_free_disk_space_on_source = required_free_disk_space_on_source
        VapiStruct.__init__(self)


DataMigrationEstimate._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.data_migration_estimate', {
        'estimated_export_time': type.IntegerType(),
        'estimated_import_time': type.IntegerType(),
        'required_free_disk_space_on_source': type.DoubleType(),
    },
    DataMigrationEstimate,
    False,
    None))



class DataMigrationInfo(VapiStruct):
    """
    The ``DataMigrationInfo`` {class contains the disk space requirements and
    time estimates for the different choices available to migrate the vCenter
    Server data. This class was added in vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 core=None,
                 core_events_tasks=None,
                 all=None,
                 core_events_tasks_with_deferred=None,
                 all_with_deferred=None,
                ):
        """
        :type  core: :class:`DataMigrationEstimate`
        :param core: Migrate only core data and configuration from vCenter Server.
            Events, tasks, and stats will not be migrated. This attribute was
            added in vSphere API 7.0.0.0.
        :type  core_events_tasks: :class:`DataMigrationEstimate`
        :param core_events_tasks: Migrate core, events, and tasks from vCenter Server. Stats will not
            be migrated. This attribute was added in vSphere API 7.0.0.0.
        :type  all: :class:`DataMigrationEstimate`
        :param all: Migrate all data from vCenter Server. This attribute was added in
            vSphere API 7.0.0.0.
        :type  core_events_tasks_with_deferred: :class:`DataMigrationEstimate` or ``None``
        :param core_events_tasks_with_deferred: Migrate core, events, and tasks from vCenter Server. Events and
            tasks will be migrated after the upgrade. Stats will not be
            migrated. This attribute was added in vSphere API 7.0.0.0.
            This attribute will be available only if the source database is
            using an external database.
        :type  all_with_deferred: :class:`DataMigrationEstimate` or ``None``
        :param all_with_deferred: Migrate all data from vCenter Server. Events, tasks, and stats will
            be migrated after the upgrade. This attribute was added in vSphere
            API 7.0.0.0.
            This attribute will be available only if the source database is
            using an external database.
        """
        self.core = core
        self.core_events_tasks = core_events_tasks
        self.all = all
        self.core_events_tasks_with_deferred = core_events_tasks_with_deferred
        self.all_with_deferred = all_with_deferred
        VapiStruct.__init__(self)


DataMigrationInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.data_migration_info', {
        'core': type.ReferenceType(__name__, 'DataMigrationEstimate'),
        'core_events_tasks': type.ReferenceType(__name__, 'DataMigrationEstimate'),
        'all': type.ReferenceType(__name__, 'DataMigrationEstimate'),
        'core_events_tasks_with_deferred': type.OptionalType(type.ReferenceType(__name__, 'DataMigrationEstimate')),
        'all_with_deferred': type.OptionalType(type.ReferenceType(__name__, 'DataMigrationEstimate')),
    },
    DataMigrationInfo,
    False,
    None))



class SourceInfo(VapiStruct):
    """
    The ``SourceInfo`` {class contains information about the source vCenter
    Server system and the database migration options. This class was added in
    vSphere API 7.0.0.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 hostname=None,
                 version=None,
                 deployment_type=None,
                 deployment_size=None,
                 sso_domain_name=None,
                 active_directory_domain=None,
                 dns_servers=None,
                 data_migration_info=None,
                ):
        """
        :type  hostname: :class:`str`
        :param hostname: The IP address or DNS resolvable name of the source vCenter Server.
            This attribute was added in vSphere API 7.0.0.0.
        :type  version: :class:`str`
        :param version: Source vCenter Server version. This attribute was added in vSphere
            API 7.0.0.0.
        :type  deployment_type: :class:`ApplianceType`
        :param deployment_type: Deployment type of the source vCenter Server. This attribute was
            added in vSphere API 7.0.0.0.
        :type  deployment_size: :class:`ApplianceSize`
        :param deployment_size: Deployment size of the source vCenter Server. This attribute was
            added in vSphere API 7.0.0.0.
        :type  sso_domain_name: :class:`str`
        :param sso_domain_name: The SSO domain name of the source vCenter Server. This attribute
            was added in vSphere API 7.0.0.0.
        :type  active_directory_domain: :class:`str`
        :param active_directory_domain: The domain name of the Active Directory server to which the source
            vCenter Server is joined. This attribute was added in vSphere API
            7.0.0.0.
        :type  dns_servers: :class:`list` of :class:`str`
        :param dns_servers: IP addresses of the DNS servers of the Active Directory server.
            This attribute was added in vSphere API 7.0.0.0.
        :type  data_migration_info: :class:`DataMigrationInfo` or ``None``
        :param data_migration_info: Contains all the available migrate options, estimated export and
            import time and the space required to migrate the data. This
            attribute was added in vSphere API 7.0.0.0.
            This attribute will be available if estimate data is available for
            the appliance.
        """
        self.hostname = hostname
        self.version = version
        self.deployment_type = deployment_type
        self.deployment_size = deployment_size
        self.sso_domain_name = sso_domain_name
        self.active_directory_domain = active_directory_domain
        self.dns_servers = dns_servers
        self.data_migration_info = data_migration_info
        VapiStruct.__init__(self)


SourceInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.source_info', {
        'hostname': type.StringType(),
        'version': type.StringType(),
        'deployment_type': type.ReferenceType(__name__, 'ApplianceType'),
        'deployment_size': type.ReferenceType(__name__, 'ApplianceSize'),
        'sso_domain_name': type.StringType(),
        'active_directory_domain': type.StringType(),
        'dns_servers': type.ListType(type.StringType()),
        'data_migration_info': type.OptionalType(type.ReferenceType(__name__, 'DataMigrationInfo')),
    },
    SourceInfo,
    False,
    None))



class CheckInfo(VapiStruct):
    """
    The ``CheckInfo`` class describes the result of the appliance deployment
    check. This class was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 status=None,
                 result=None,
                 source_info=None,
                ):
        """
        :type  status: :class:`CheckStatus`
        :param status: Status of the check. This attribute was added in vSphere API 6.7.
        :type  result: :class:`Notifications` or ``None``
        :param result: Result of the check. This attribute was added in vSphere API 6.7.
            This attribute will be None if result is not available at the
            current step of the task.
        :type  source_info: :class:`SourceInfo` or ``None``
        :param source_info: Information collected from the source machine. This attribute was
            added in vSphere API 7.0.0.0.
            This attribute is used only for upgrade and migrate.
        """
        self.status = status
        self.result = result
        self.source_info = source_info
        VapiStruct.__init__(self)


CheckInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.check_info', {
        'status': type.ReferenceType(__name__, 'CheckStatus'),
        'result': type.OptionalType(type.ReferenceType(__name__, 'Notifications')),
        'source_info': type.OptionalType(type.ReferenceType(__name__, 'SourceInfo')),
    },
    CheckInfo,
    False,
    None))



class HistoryMigrationSpec(VapiStruct):
    """
    The ``HistoryMigrationSpec`` class defines how vCenter history data will be
    migrated. vCenter History data includes 
    
    * Statistics
    * Events
    * Tasks
    
    . This class was added in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 data_set=None,
                 defer_import=None,
                ):
        """
        :type  data_set: :class:`HistoryMigrationOption`
        :param data_set: Defines what part of vCenter historical data will be migrated along
            with core data. This attribute was added in vSphere API 6.7.
        :type  defer_import: :class:`bool` or ``None``
        :param defer_import: Defines how vCenter history will be migrated. If set to true,
            vCenter history will be migrated separately after successful
            upgrade(supported scenarios are upgrade from 6.0 or 6.5 to 6.7) or
            migration, otherwise it will be migrated along with core data
            during the upgrade or migration process. vCSA upgrade with deferred
            import is no longer supported for target version 7.0 and later.
            This attribute was added in vSphere API 6.7.
            If None, vCenter historical data won't be deferred and will be
            migrated along with core data.
        """
        self.data_set = data_set
        self.defer_import = defer_import
        VapiStruct.__init__(self)


HistoryMigrationSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.history_migration_spec', {
        'data_set': type.ReferenceType(__name__, 'HistoryMigrationOption'),
        'defer_import': type.OptionalType(type.BooleanType()),
    },
    HistoryMigrationSpec,
    False,
    None))



class LocationSpec(VapiStruct):
    """
    The ``LocationSpec`` class is used to pass the container ESXi or vCenter
    server of the VM to patch the size of this appliance. This class was added
    in vSphere API 6.7.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 hostname=None,
                 https_port=None,
                 ssl_thumbprint=None,
                 ssl_verify=None,
                 username=None,
                 password=None,
                ):
        """
        :type  hostname: :class:`str`
        :param hostname: The IP address or DNS resolvable name of the container. This
            attribute was added in vSphere API 6.7.
        :type  https_port: :class:`long` or ``None``
        :param https_port: The HTTPS port of the container. This attribute was added in
            vSphere API 6.7.
            If None, port 443 will be used.
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SHA1 thumbprint of the server SSL certificate will be used for
            verification. This attribute was added in vSphere API 6.7.
            This attribute is only relevant if ``sslVerify`` is None or has the
            value true.
        :type  ssl_verify: :class:`bool` or ``None``
        :param ssl_verify: SSL verification should be enabled or disabled. If ``sslVerify`` is
            true and and ``sslThumbprint`` is None, the CA certificate will be
            used for verification. If ``sslVerify`` is true and
            ``sslThumbprint`` is set then the thumbprint will be used for
            verification. No verification will be performed if ``sslVerify``
            value is set to false. This attribute was added in vSphere API 6.7.
            If None, ssl_verify true will be used.
        :type  username: :class:`str`
        :param username: The administrator account on the host. This attribute was added in
            vSphere API 6.7.
        :type  password: :class:`str`
        :param password: The administrator account password. This attribute was added in
            vSphere API 6.7.
        """
        self.hostname = hostname
        self.https_port = https_port
        self.ssl_thumbprint = ssl_thumbprint
        self.ssl_verify = ssl_verify
        self.username = username
        self.password = password
        VapiStruct.__init__(self)


LocationSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.deployment.location_spec', {
        'hostname': type.StringType(),
        'https_port': type.OptionalType(type.IntegerType()),
        'ssl_thumbprint': type.OptionalType(type.StringType()),
        'ssl_verify': type.OptionalType(type.BooleanType()),
        'username': type.StringType(),
        'password': type.SecretType(),
    },
    LocationSpec,
    False,
    None))



class Install(VapiInterface):
    """
    The ``Install`` class provides methods to configure the installation of the
    appliance. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.deployment.install'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _InstallStub)
        self._VAPI_OPERATION_IDS = {}

    class VcsaEmbeddedSpec(VapiStruct):
        """
        The ``Install.VcsaEmbeddedSpec`` class contains information used to
        configure an embedded standalone or replicated vCenter Server. This class
        was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     standalone=None,
                     replicated=None,
                     ceip_enabled=None,
                    ):
            """
            :type  standalone: :class:`StandaloneSpec` or ``None``
            :param standalone: Spec used to configure a standalone embedded vCenter Server. This
                field describes how the standalone vCenter Server appliance should
                be configured. This attribute was added in vSphere API 6.7.
                If None, will default to None.
            :type  replicated: :class:`ReplicatedSpec` or ``None``
            :param replicated: Spec used to configure a replicated embedded vCenter Server. This
                field describes how the replicated vCenter Server appliance should
                be configured. This attribute was added in vSphere API 6.7.
                If None, will default to None.
            :type  ceip_enabled: :class:`bool`
            :param ceip_enabled: Whether CEIP should be enabled or disabled. This attribute was
                added in vSphere API 6.7.
            """
            self.standalone = standalone
            self.replicated = replicated
            self.ceip_enabled = ceip_enabled
            VapiStruct.__init__(self)


    VcsaEmbeddedSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.install.vcsa_embedded_spec', {
            'standalone': type.OptionalType(type.ReferenceType(__name__, 'StandaloneSpec')),
            'replicated': type.OptionalType(type.ReferenceType(__name__, 'ReplicatedSpec')),
            'ceip_enabled': type.BooleanType(),
        },
        VcsaEmbeddedSpec,
        False,
        None))


    class InstallSpec(VapiStruct):
        """
        The ``Install.InstallSpec`` class contains information used to configure
        the appliance installation. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vcsa_embedded=None,
                     auto_answer=None,
                    ):
            """
            :type  vcsa_embedded: :class:`Install.VcsaEmbeddedSpec`
            :param vcsa_embedded: Spec used to configure an embedded vCenter Server. This field
                describes how the embedded vCenter Server appliance should be
                configured. This attribute was added in vSphere API 6.7.
            :type  auto_answer: :class:`bool` or ``None``
            :param auto_answer: Use the default option for any questions that may come up during
                appliance configuration. This attribute was added in vSphere API
                6.7.
                If None, will default to false.
            """
            self.vcsa_embedded = vcsa_embedded
            self.auto_answer = auto_answer
            VapiStruct.__init__(self)


    InstallSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.install.install_spec', {
            'vcsa_embedded': type.ReferenceType(__name__, 'Install.VcsaEmbeddedSpec'),
            'auto_answer': type.OptionalType(type.BooleanType()),
        },
        InstallSpec,
        False,
        None))



    def get(self):
        """
        Get the parameters used to configure the ongoing appliance
        installation. This method was added in vSphere API 6.7.


        :rtype: :class:`Install.InstallSpec`
        :return: InstallSpec parameters being used to configure appliance install.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if appliance is not in INSTALL_PROGRESS state.
        """
        return self._invoke('get', None)

    def check(self,
              spec,
              ):
        """
        Run sanity checks using the InstallSpec parameters passed. This method
        was added in vSphere API 6.7.

        :type  spec: :class:`Install.InstallSpec`
        :param spec: InstallSpec parameters to run sanity check with.
        :rtype: :class:`CheckInfo`
        :return: CheckInfo containing the check results.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if external PSC credentials are not valid when configuring PSC to
            replicate with an external existing PSC.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if external PSC credentials are not valid when configuring a
            VCSA_EXTERNAL appliance.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in INITIALIZED state.
        """
        return self._invoke('check',
                            {
                            'spec': spec,
                            })

    def start(self,
              spec,
              ):
        """
        Start the appliance installation. This method was added in vSphere API
        6.7.

        :type  spec: :class:`Install.InstallSpec`
        :param spec: InstallSpec parameters to configure the appliance install.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the partner PSC credentials are not valid when configuring PSC
            to replicate with partner PSC.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if external PSC credentials are not valid when configuring a
            VCSA_EXTERNAL appliance.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in INITIALIZED state.
        """
        return self._invoke('start',
                            {
                            'spec': spec,
                            })

    def cancel(self):
        """
        Cancel the appliance installation that is in progress. This method was
        added in vSphere API 6.7.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in CONFIG_IN_PROGRESS state and if the
            operation is not INSTALL.
        """
        return self._invoke('cancel', None)
class Upgrade(VapiInterface):
    """
    The ``Upgrade`` class provides methods to configure the upgrade of this
    appliance from an existing vCenter appliance. This class was added in
    vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.deployment.upgrade'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UpgradeStub)
        self._VAPI_OPERATION_IDS = {}

    class VcsaEmbeddedSpec(VapiStruct):
        """
        The ``Upgrade.VcsaEmbeddedSpec`` class contains information used to upgrade
        a Embedded vCenter Server appliance. This class was added in vSphere API
        6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ceip_enabled=None,
                    ):
            """
            :type  ceip_enabled: :class:`bool`
            :param ceip_enabled: Customer experience improvement program should be enabled or
                disabled for this embedded vCenter Server upgrade. This attribute
                was added in vSphere API 6.7.
            """
            self.ceip_enabled = ceip_enabled
            VapiStruct.__init__(self)


    VcsaEmbeddedSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.upgrade.vcsa_embedded_spec', {
            'ceip_enabled': type.BooleanType(),
        },
        VcsaEmbeddedSpec,
        False,
        None))


    class PscSpec(VapiStruct):
        """
        The ``Upgrade.PscSpec`` class contains information used to upgrade a
        Platform Service Controller appliance. This class was added in vSphere API
        6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ceip_enabled=None,
                    ):
            """
            :type  ceip_enabled: :class:`bool`
            :param ceip_enabled: Customer experience improvement program should be enabled or
                disabled for this Platform Services Controller upgrade. This
                attribute was added in vSphere API 6.7.
            """
            self.ceip_enabled = ceip_enabled
            VapiStruct.__init__(self)


    PscSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.upgrade.psc_spec', {
            'ceip_enabled': type.BooleanType(),
        },
        PscSpec,
        False,
        None))


    class SourceApplianceSpec(VapiStruct):
        """
        The ``Upgrade.SourceApplianceSpec`` class contains information used to
        connect to the appliance used as the source for an upgrade. This class was
        added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hostname=None,
                     https_port=None,
                     ssl_thumbprint=None,
                     ssl_verify=None,
                     sso_admin_username=None,
                     sso_admin_password=None,
                     root_password=None,
                     ssh_verify=None,
                     ssh_thumbprint=None,
                    ):
            """
            :type  hostname: :class:`str`
            :param hostname: The IP address or DNS resolvable name of the source appliance. This
                attribute was added in vSphere API 6.7.
            :type  https_port: :class:`long` or ``None``
            :param https_port: The HTTPS port of the source appliance. This attribute was added in
                vSphere API 6.7.
                If None, port 443 will be used.
            :type  ssl_thumbprint: :class:`str` or ``None``
            :param ssl_thumbprint: SHA1 thumbprint of the server SSL certificate will be used for
                verification. This attribute was added in vSphere API 6.7.
                This attribute is only relevant if ``sslVerify`` is None or has the
                value true.
            :type  ssl_verify: :class:`bool` or ``None``
            :param ssl_verify: SSL verification should be enabled or disabled for the source
                appliance validations. By default it is enabled and will use SSL
                certificate for verification. If thumbprint is provided, will use
                thumbprint for the verification. This attribute was added in
                vSphere API 6.7.
                If None, ssl_verify true will be used.
            :type  sso_admin_username: :class:`str`
            :param sso_admin_username: The SSO administrator account on the source appliance. This
                attribute was added in vSphere API 6.7.
            :type  sso_admin_password: :class:`str`
            :param sso_admin_password: The SSO administrator account password. This attribute was added in
                vSphere API 6.7.
            :type  root_password: :class:`str`
            :param root_password: The password of the root user on the source appliance. This
                attribute was added in vSphere API 6.7.
            :type  ssh_verify: :class:`bool` or ``None``
            :param ssh_verify: Appliance SSH verification should be enabled or disabled. By
                default it is disabled and will not use any verification. If
                thumbprint is provided, thumbprint verification will be performed.
                This attribute was added in vSphere API 6.7.
                If None, ssh_verify true will be used.
            :type  ssh_thumbprint: :class:`str` or ``None``
            :param ssh_thumbprint: MD5 thumbprint of the server SSH key will be used for verification.
                This attribute was added in vSphere API 6.7.
                This attribute is only relevant if ``sshVerify`` is None or has the
                value true.
            """
            self.hostname = hostname
            self.https_port = https_port
            self.ssl_thumbprint = ssl_thumbprint
            self.ssl_verify = ssl_verify
            self.sso_admin_username = sso_admin_username
            self.sso_admin_password = sso_admin_password
            self.root_password = root_password
            self.ssh_verify = ssh_verify
            self.ssh_thumbprint = ssh_thumbprint
            VapiStruct.__init__(self)


    SourceApplianceSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.upgrade.source_appliance_spec', {
            'hostname': type.StringType(),
            'https_port': type.OptionalType(type.IntegerType()),
            'ssl_thumbprint': type.OptionalType(type.StringType()),
            'ssl_verify': type.OptionalType(type.BooleanType()),
            'sso_admin_username': type.StringType(),
            'sso_admin_password': type.SecretType(),
            'root_password': type.SecretType(),
            'ssh_verify': type.OptionalType(type.BooleanType()),
            'ssh_thumbprint': type.OptionalType(type.StringType()),
        },
        SourceApplianceSpec,
        False,
        None))


    class UpgradeSpec(VapiStruct):
        """
        The ``Upgrade.UpgradeSpec`` class contains information used to configure
        the appliance upgrade. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     source_appliance=None,
                     source_location=None,
                     history=None,
                     vcsa_embedded=None,
                     psc=None,
                     auto_answer=None,
                     skip_products_prechecks=None,
                    ):
            """
            :type  source_appliance: :class:`Upgrade.SourceApplianceSpec`
            :param source_appliance: Source appliance spec. This attribute was added in vSphere API 6.7.
            :type  source_location: :class:`LocationSpec`
            :param source_location: Source location spec. This attribute was added in vSphere API 6.7.
            :type  history: :class:`HistoryMigrationSpec` or ``None``
            :param history: Determines how vCenter history will be migrated during the upgrade
                process. vCenter history consists of: 
                
                * Statistics
                * Events
                * Tasks
                
                By default only core data will be migrated. Use this spec to define
                which part of vCenter history data will be migrated and when. This
                attribute was added in vSphere API 6.7.
                If None, only core database content will be migrated.
            :type  vcsa_embedded: :class:`Upgrade.VcsaEmbeddedSpec` or ``None``
            :param vcsa_embedded: Information that are specific to this embedded vCenter Server. This
                attribute was added in vSphere API 6.7.
                If None, ceip_enabled for embedded vcenter server upgrade will
                default to enabled.
            :type  psc: :class:`Upgrade.PscSpec` or ``None``
            :param psc: Information that are specific to this Platform Services Controller.
                This attribute was added in vSphere API 6.7.
                If None, ceip_enabled for psc upgrade will default to enabled.
            :type  auto_answer: :class:`bool` or ``None``
            :param auto_answer: Use the default option for any questions that may come up during
                appliance configuration. This attribute was added in vSphere API
                6.7.
                If None, will default to false.
            :type  skip_products_prechecks: :class:`bool` or ``None``
            :param skip_products_prechecks: Use the option to skip products interoperability checks during
                upgrade prechecks. This attribute was added in vSphere API 8.0.3.0.
                If None, will default to false.
            """
            self.source_appliance = source_appliance
            self.source_location = source_location
            self.history = history
            self.vcsa_embedded = vcsa_embedded
            self.psc = psc
            self.auto_answer = auto_answer
            self.skip_products_prechecks = skip_products_prechecks
            VapiStruct.__init__(self)


    UpgradeSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.upgrade.upgrade_spec', {
            'source_appliance': type.ReferenceType(__name__, 'Upgrade.SourceApplianceSpec'),
            'source_location': type.ReferenceType(__name__, 'LocationSpec'),
            'history': type.OptionalType(type.ReferenceType(__name__, 'HistoryMigrationSpec')),
            'vcsa_embedded': type.OptionalType(type.ReferenceType(__name__, 'Upgrade.VcsaEmbeddedSpec')),
            'psc': type.OptionalType(type.ReferenceType(__name__, 'Upgrade.PscSpec')),
            'auto_answer': type.OptionalType(type.BooleanType()),
            'skip_products_prechecks': type.OptionalType(type.BooleanType()),
        },
        UpgradeSpec,
        False,
        None))



    def get(self):
        """
        Get the UpgradeSpec parameters used to configure the ongoing appliance
        upgrade. This method was added in vSphere API 6.7.


        :rtype: :class:`Upgrade.UpgradeSpec`
        :return: UpgradeSpec parameters being used to configure appliance upgrade.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if appliance is not in UPGRADE_PROGRESS state.
        """
        return self._invoke('get', None)

    def check(self,
              spec,
              ):
        """
        Run sanity checks using the UpgradeSpec parameters passed. This method
        was added in vSphere API 6.7.

        :type  spec: :class:`Upgrade.UpgradeSpec`
        :param spec: UpgradeSpec parameters to run sanity check on.
        :rtype: :class:`CheckInfo`
        :return: CheckInfo containing the check results.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if source credentials are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if source container credentials are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in INITIALIZED state.
        """
        return self._invoke('check',
                            {
                            'spec': spec,
                            })

    def start(self,
              spec,
              ):
        """
        Start the appliance installation. This method was added in vSphere API
        6.7.

        :type  spec: :class:`Upgrade.UpgradeSpec`
        :param spec: UpgradeSpec parameters to configure the appliance upgrade.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if source credentials are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if source container credentials are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in INITIALIZED state.
        """
        return self._invoke('start',
                            {
                            'spec': spec,
                            })

    def cancel(self):
        """
        Cancel the appliance upgrade that is in progress. This method was added
        in vSphere API 6.7.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in CONFIG_IN_PROGRESS state and if the
            operation is not INSTALL.
        """
        return self._invoke('cancel', None)
class Migrate(VapiInterface):
    """
    The ``Migrate`` class provides methods to configure the migration of this
    appliance from an existing vCenter for Windows. This class was added in
    vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.deployment.migrate'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _MigrateStub)
        self._VAPI_OPERATION_IDS = {}

    class VcsaEmbeddedSpec(VapiStruct):
        """
        The ``Migrate.VcsaEmbeddedSpec`` class contains information used to migrate
        an embedded vCenter Server for Windows to embedded vCenter Server
        appliance. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ceip_enabled=None,
                    ):
            """
            :type  ceip_enabled: :class:`bool`
            :param ceip_enabled: Customer experience improvement program should be enabled or
                disabled for this embedded vCenter Server migration. This attribute
                was added in vSphere API 7.0.0.0.
            """
            self.ceip_enabled = ceip_enabled
            VapiStruct.__init__(self)


    VcsaEmbeddedSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.migrate.vcsa_embedded_spec', {
            'ceip_enabled': type.BooleanType(),
        },
        VcsaEmbeddedSpec,
        False,
        None))


    class PscSpec(VapiStruct):
        """
        The ``Migrate.PscSpec`` class contains information used to migrate a
        windows Platform Service Controller to Platform Service Controller
        appliance. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ceip_enabled=None,
                    ):
            """
            :type  ceip_enabled: :class:`bool`
            :param ceip_enabled: Customer experience improvement program should be enabled or
                disabled for this Platform Services Controller migration. This
                attribute was added in vSphere API 7.0.0.0.
            """
            self.ceip_enabled = ceip_enabled
            VapiStruct.__init__(self)


    PscSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.migrate.psc_spec', {
            'ceip_enabled': type.BooleanType(),
        },
        PscSpec,
        False,
        None))


    class SourceVcWindows(VapiStruct):
        """
        The ``Migrate.SourceVcWindows`` class contains information about the
        windows vCenter Server that is going to be migrated. This class was added
        in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hostname=None,
                     username=None,
                     password=None,
                    ):
            """
            :type  hostname: :class:`str`
            :param hostname: The IP address or DNS resolvable name of the source Windows
                machine. This attribute was added in vSphere API 7.0.0.0.
            :type  username: :class:`str`
            :param username: The SSO account with administrative privilege to perform the
                migration operation. This attribute was added in vSphere API
                7.0.0.0.
            :type  password: :class:`str`
            :param password: The SSO administrator account password. This attribute was added in
                vSphere API 7.0.0.0.
            """
            self.hostname = hostname
            self.username = username
            self.password = password
            VapiStruct.__init__(self)


    SourceVcWindows._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.migrate.source_vc_windows', {
            'hostname': type.StringType(),
            'username': type.StringType(),
            'password': type.SecretType(),
        },
        SourceVcWindows,
        False,
        None))


    class MigrationAssistantSpec(VapiStruct):
        """
        The ``Migrate.MigrationAssistantSpec`` class contains the information
        needed to connect to the Migration Assistant that is running on the source
        windows vCenter Server machine. This class was added in vSphere API
        7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     https_port=None,
                     ssl_thumbprint=None,
                    ):
            """
            :type  https_port: :class:`long` or ``None``
            :param https_port: The HTTPS port being used by Migration Assistant. This attribute
                was added in vSphere API 7.0.0.0.
                If None, port 9123 will be used.
            :type  ssl_thumbprint: :class:`str`
            :param ssl_thumbprint: SHA1 thumbprint of the Migration Assistant SSL certificate that
                will be used for verification. This attribute was added in vSphere
                API 7.0.0.0.
            """
            self.https_port = https_port
            self.ssl_thumbprint = ssl_thumbprint
            VapiStruct.__init__(self)


    MigrationAssistantSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.migrate.migration_assistant_spec', {
            'https_port': type.OptionalType(type.IntegerType()),
            'ssl_thumbprint': type.StringType(),
        },
        MigrationAssistantSpec,
        False,
        None))


    class MigrateSpec(VapiStruct):
        """
        The ``Migrate.MigrateSpec`` class contains the fields to migrate an
        existing vCenter Server for Windows to an appliance. This class was added
        in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     source_vc_windows=None,
                     existing_migration_assistant=None,
                     history=None,
                     vcsa_embedded=None,
                     psc=None,
                     active_directory=None,
                     auto_answer=None,
                    ):
            """
            :type  source_vc_windows: :class:`Migrate.SourceVcWindows`
            :param source_vc_windows: Information specific to the Windows vCenter Server. This attribute
                was added in vSphere API 7.0.0.0.
            :type  existing_migration_assistant: :class:`Migrate.MigrationAssistantSpec`
            :param existing_migration_assistant: Information specific to the Migration Assistant that is running on
                the Windows vCenter Server. This attribute was added in vSphere API
                7.0.0.0.
            :type  history: :class:`HistoryMigrationSpec` or ``None``
            :param history: Determines how vCenter history will be migrated during the
                migration process. vCenter history consists of: 
                
                * Statistics
                * Events
                * Tasks
                
                By default only core data will be migrated. Use this spec to define
                which part of vCenter history data will be migrated and when. This
                attribute was added in vSphere API 7.0.0.0.
                If None, only core database content will be migrated.
            :type  vcsa_embedded: :class:`Migrate.VcsaEmbeddedSpec` or ``None``
            :param vcsa_embedded: Information specific to an embedded vCenter Server. This attribute
                was added in vSphere API 7.0.0.0.
                Only required if the vCenter Server that is going to be migrated is
                an embedded vCenter Server.
            :type  psc: :class:`Migrate.PscSpec` or ``None``
            :param psc: Information specific to a Platform Services Controller. This
                attribute was added in vSphere API 7.0.0.0.
                Only required if the vCenter Server that is going to be migrated is
                a Platform Services Controller.
            :type  active_directory: :class:`com.vmware.vcenter.deployment.migrate_client.ActiveDirectorySpec` or ``None``
            :param active_directory: Information specific to the Active Directory server to which the
                source windows vCenter Server is joined. This attribute was added
                in vSphere API 7.0.0.0.
                If None, existing appliance will not be joined to an Active
                Directory.
            :type  auto_answer: :class:`bool` or ``None``
            :param auto_answer: Use the default option for any questions that may come up during
                appliance configuration. This attribute was added in vSphere API
                7.0.0.0.
                If None, will default to false.
            """
            self.source_vc_windows = source_vc_windows
            self.existing_migration_assistant = existing_migration_assistant
            self.history = history
            self.vcsa_embedded = vcsa_embedded
            self.psc = psc
            self.active_directory = active_directory
            self.auto_answer = auto_answer
            VapiStruct.__init__(self)


    MigrateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.migrate.migrate_spec', {
            'source_vc_windows': type.ReferenceType(__name__, 'Migrate.SourceVcWindows'),
            'existing_migration_assistant': type.ReferenceType(__name__, 'Migrate.MigrationAssistantSpec'),
            'history': type.OptionalType(type.ReferenceType(__name__, 'HistoryMigrationSpec')),
            'vcsa_embedded': type.OptionalType(type.ReferenceType(__name__, 'Migrate.VcsaEmbeddedSpec')),
            'psc': type.OptionalType(type.ReferenceType(__name__, 'Migrate.PscSpec')),
            'active_directory': type.OptionalType(type.ReferenceType('com.vmware.vcenter.deployment.migrate_client', 'ActiveDirectorySpec')),
            'auto_answer': type.OptionalType(type.BooleanType()),
        },
        MigrateSpec,
        False,
        None))



    def get(self):
        """
        Get the MigrateSpec parameters used to configure the ongoing appliance
        migration. This method was added in vSphere API 7.0.0.0.


        :rtype: :class:`Migrate.MigrateSpec`
        :return: MigrateSpec parameters being used to configure appliance migration.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if appliance is not in MIGRATE_PROGRESS state.
        """
        return self._invoke('get', None)

    def check(self,
              spec,
              ):
        """
        Run sanity checks using the MigrateSpec parameters passed. This method
        was added in vSphere API 7.0.0.0.

        :type  spec: :class:`Migrate.MigrateSpec`
        :param spec: MigrateSpec parameters to run sanity check on.
        :rtype: :class:`CheckInfo`
        :return: CheckInfo containing the check results.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if migration assistant credentials are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in INITIALIZED state.
        """
        return self._invoke('check',
                            {
                            'spec': spec,
                            })

    def start(self,
              spec,
              ):
        """
        Start the appliance migration. This method was added in vSphere API
        7.0.0.0.

        :type  spec: :class:`Migrate.MigrateSpec`
        :param spec: MigrateSpec parameters to configure the appliance migration.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if migration assistant credentials are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in INITIALIZED state.
        """
        return self._invoke('start',
                            {
                            'spec': spec,
                            })

    def cancel(self):
        """
        Cancel the appliance migration that is in progress. This method was
        added in vSphere API 7.0.0.0.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in CONFIG_IN_PROGRESS state and if the
            operation is not INSTALL.
        """
        return self._invoke('cancel', None)
class Question(VapiInterface):
    """
    The ``Question`` class provides methods to get the question raised during
    deployment and to answer them. This class was added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.deployment.question'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _QuestionStub)
        self._VAPI_OPERATION_IDS = {}

    class QuestionType(Enum):
        """
        The ``Question.QuestionType`` class defines the type of the question
        raised. This enumeration was added in vSphere API 6.7.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        YES_NO = None
        """
        Question with answer values Yes/No. This class attribute was added in
        vSphere API 6.7.

        """
        OK_CANCEL = None
        """
        Question with answer values Ok/Cancel. This class attribute was added in
        vSphere API 6.7.

        """
        ABORT_RETRY_IGNORE = None
        """
        Question with answer values Abort/Retry/Ignore. This class attribute was
        added in vSphere API 6.7.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`QuestionType` instance.
            """
            Enum.__init__(string)

    QuestionType._set_values({
        'YES_NO': QuestionType('YES_NO'),
        'OK_CANCEL': QuestionType('OK_CANCEL'),
        'ABORT_RETRY_IGNORE': QuestionType('ABORT_RETRY_IGNORE'),
    })
    QuestionType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.deployment.question.question_type',
        QuestionType))


    class Question(VapiStruct):
        """
        The ``Question.Question`` class contains attributes to describe a
        deployment question. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     question=None,
                     type=None,
                     default_answer=None,
                     possible_answers=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Id of the question raised. This attribute was added in vSphere API
                6.7.
            :type  question: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param question: Message describing the question. This attribute was added in
                vSphere API 6.7.
            :type  type: :class:`Question.QuestionType`
            :param type: Type of the question raised. This attribute was added in vSphere
                API 6.7.
            :type  default_answer: :class:`str`
            :param default_answer: Default answer value. This attribute was added in vSphere API 6.7.
            :type  possible_answers: :class:`list` of :class:`str`
            :param possible_answers: Possible answers values. This attribute was added in vSphere API
                6.7.
            """
            self.id = id
            self.question = question
            self.type = type
            self.default_answer = default_answer
            self.possible_answers = possible_answers
            VapiStruct.__init__(self)


    Question._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.question.question', {
            'id': type.StringType(),
            'question': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
            'type': type.ReferenceType(__name__, 'Question.QuestionType'),
            'default_answer': type.StringType(),
            'possible_answers': type.ListType(type.StringType()),
        },
        Question,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Question.Info`` class contains attributes to describe questions
        raised during the deployment process. This class was added in vSphere API
        6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     questions=None,
                    ):
            """
            :type  questions: :class:`list` of :class:`Question.Question`
            :param questions: One or more questions raised during the deployment. This attribute
                was added in vSphere API 6.7.
            """
            self.questions = questions
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.question.info', {
            'questions': type.ListType(type.ReferenceType(__name__, 'Question.Question')),
        },
        Info,
        False,
        None))


    class AnswerSpec(VapiStruct):
        """
        The ``Question.AnswerSpec`` class contains attributes to describe the
        answer to a raised question. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     question_id=None,
                     answer_val=None,
                    ):
            """
            :type  question_id: :class:`str`
            :param question_id: Id of the question being answered. This attribute was added in
                vSphere API 6.7.
            :type  answer_val: :class:`str`
            :param answer_val: The answer value. This attribute was added in vSphere API 6.7.
            """
            self.question_id = question_id
            self.answer_val = answer_val
            VapiStruct.__init__(self)


    AnswerSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.question.answer_spec', {
            'question_id': type.StringType(),
            'answer_val': type.StringType(),
        },
        AnswerSpec,
        False,
        None))



    def get(self):
        """
        Get the question that was raised during the configuration. This method
        was added in vSphere API 6.7.


        :rtype: :class:`Question.Info`
        :return: Info structure containing the question.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is not in QUESTION_RAISED state.
        :raise: :class:`com.vmware.vapi.std.errors_client.InternalServerError` 
            if questions could not be retrieved although the appliance is in
            QUESTION_RAISED state.
        """
        return self._invoke('get', None)

    def answer(self,
               spec,
               ):
        """
        Supply answer to the raised question. This method was added in vSphere
        API 6.7.

        :type  spec: :class:`Question.AnswerSpec`
        :param spec: AnswerSpec with the answer to the raised question.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance is NOT in QUESTION_RAISED state.
        :raise: :class:`com.vmware.vapi.std.errors_client.InternalServerError` 
            if answer file could not be created.
        """
        return self._invoke('answer',
                            {
                            'spec': spec,
                            })
class ImportHistory(VapiInterface):
    """
    The ``ImportHistory`` class provides methods for managing the import of
    vCenter historical data, e.g. Tasks, Events and Statistics, when is is
    imported separately from the upgrade or migration process. This class was
    added in vSphere API 6.7.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.deployment.import_history'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ImportHistoryStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``ImportHistory.Info`` class contains attributes to describe the state
        of vCenter history import task. This class was added in vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'RUNNING' : [('progress', True), ('result', False), ('start_time', True)],
                    'FAILED' : [('progress', True), ('result', False), ('error', False), ('start_time', True), ('end_time', True)],
                    'BLOCKED' : [('progress', True), ('result', False), ('start_time', True)],
                    'SUCCEEDED' : [('progress', True), ('result', False), ('start_time', True), ('end_time', True)],
                    'PENDING' : [],
                }
            ),
        ]



        def __init__(self,
                     progress=None,
                     result=None,
                     description=None,
                     service=None,
                     operation=None,
                     parent=None,
                     target=None,
                     status=None,
                     cancelable=None,
                     error=None,
                     start_time=None,
                     end_time=None,
                     user=None,
                    ):
            """
            :type  progress: :class:`com.vmware.cis.task_client.Progress`
            :param progress: The progress info of this task. This attribute was added in vSphere
                API 6.7.
                This attribute is optional and it is only relevant when the value
                of ``CommonInfo#status`` is one of
                :attr:`com.vmware.cis.task_client.Status.RUNNING`,
                :attr:`com.vmware.cis.task_client.Status.FAILED`,
                :attr:`com.vmware.cis.task_client.Status.BLOCKED`, or
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`.
            :type  result: :class:`Notifications` or ``None``
            :param result: Result of the operation. If an operation reports partial results
                before it completes, this attribute could be :class:`set` before
                the :attr:`com.vmware.cis.task_client.CommonInfo.status` has the
                value :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`. The
                value could change as the operation progresses. This attribute was
                added in vSphere API 6.7.
                This attribute will be None if result is not available at the
                current step of the operation.
            :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param description: Description of the operation associated with the task.
            :type  service: :class:`str`
            :param service: Identifier of the service containing the operation.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.service``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.service``.
            :type  operation: :class:`str`
            :param operation: Identifier of the operation associated with the task.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.operation``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.operation``.
            :type  parent: :class:`str` or ``None``
            :param parent: Parent of the current task.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.task``. When methods return a value of this class
                as a return value, the attribute will be an identifier for the
                resource type: ``com.vmware.cis.task``.
                This attribute will be None if the task has no parent.
            :type  target: :class:`com.vmware.vapi.std_client.DynamicID` or ``None``
            :param target: Identifier of the target created by the operation or an existing
                one the operation performed on.
                This attribute will be None if the operation has no target or
                multiple targets.
            :type  status: :class:`com.vmware.cis.task_client.Status`
            :param status: Status of the operation associated with the task.
            :type  cancelable: :class:`bool`
            :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
                value may change as the operation progresses.
            :type  error: :class:`Exception` or ``None``
            :param error: Description of the error if the operation status is "FAILED".
                If None the description of why the operation failed will be
                included in the result of the operation (see
                :attr:`com.vmware.cis.task_client.Info.result`).
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Time when the operation is started.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.cis.task_client.Status.RUNNING`,
                :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  end_time: :class:`datetime.datetime`
            :param end_time: Time when the operation is completed.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED` or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  user: :class:`str` or ``None``
            :param user: Name of the user who performed the operation.
                This attribute will be None if the operation is performed by the
                system.
            """
            self.progress = progress
            self.result = result
            self.description = description
            self.service = service
            self.operation = operation
            self.parent = parent
            self.target = target
            self.status = status
            self.cancelable = cancelable
            self.error = error
            self.start_time = start_time
            self.end_time = end_time
            self.user = user
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.import_history.info', {
            'progress': type.OptionalType(type.ReferenceType('com.vmware.cis.task_client', 'Progress')),
            'result': type.OptionalType(type.ReferenceType(__name__, 'Notifications')),
            'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
            'service': type.IdType(resource_types='com.vmware.vapi.service'),
            'operation': type.IdType(resource_types='com.vmware.vapi.operation'),
            'parent': type.OptionalType(type.IdType()),
            'target': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID')),
            'status': type.ReferenceType('com.vmware.cis.task_client', 'Status'),
            'cancelable': type.BooleanType(),
            'error': type.OptionalType(type.AnyErrorType()),
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
            'user': type.OptionalType(type.StringType()),
        },
        Info,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``ImportHistory.CreateSpec`` class contains information to create and
        start vCenter historical data deferred import. This class was added in
        vSphere API 6.7.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     description=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the vCenter history import task. This attribute was added
                in vSphere API 6.7.
            :type  description: :class:`str`
            :param description: Description of the vCenter history import task. This attribute was
                added in vSphere API 6.7.
            """
            self.name = name
            self.description = description
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.import_history.create_spec', {
            'name': type.StringType(),
            'description': type.StringType(),
        },
        CreateSpec,
        False,
        None))



    def get(self):
        """
        Get the current status of the vCenter historical data import. This
        method was added in vSphere API 6.7.


        :rtype: :class:`ImportHistory.Info`
        :return: Info structure containing the status information about the
            historical data import status.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized to perform the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)

    def start(self,
              spec=None,
              ):
        """
        Creates and starts task for importing vCenter historical data. This
        method was added in vSphere API 6.7.

        :type  spec: :class:`ImportHistory.CreateSpec` or ``None``
        :param spec: An optional ``ImportHistory.CreateSpec`` info that can be passed
            for creating a new historical data import task and starts it.
            If None, default value will be: 
            
            * name : vcenter.deployment.history.import
            * description : vCenter Server history import
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized to perform the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if vCenter historical data import task cannot be started at this
            time. This can happen in the following cases: 
            
            * If historical data import has already been canceled because a
              canceled task cannot be re-started
            * If historical data import has already been completed because a
              completed task cannot be re-started
            * If historical data import has already been paused because a
              paused task can only be resumed or canceled
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if vCenter historical data import task has already being started.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('start',
                            {
                            'spec': spec,
                            })

    def pause(self):
        """
        Pauses the task for importing vCenter historical data. This method was
        added in vSphere API 6.7.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized to perform the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if vCenter historical data import task cannot be paused at this
            time. Pause can be accepted only in
            :attr:`com.vmware.cis.task_client.Status.RUNNING` state.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if vCenter historical data import task is already paused
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('pause', None)

    def resume(self):
        """
        Resumes the task for importing vCenter historical data. This method was
        added in vSphere API 6.7.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized to perform the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if vCenter historical data import task cannot be resumed at this
            state. Resume can be accepted only in
            :attr:`com.vmware.cis.task_client.Status.BLOCKED` state
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if vCenter historical data import task is already resumed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('resume', None)

    def cancel(self):
        """
        Cancels the task for importing vCenter historical data. This method was
        added in vSphere API 6.7.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized to perform the method.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if vCenter historical data import task cannot be canceled at this
            state. This can happen in the following cases: 
            
            * If historical data import has not been started yet because a not
              running task cannot be canceled
            * If historical data import has already been completed because a
              completed task cannot be canceled
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if vCenter historical data import task is already canceled.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error.
        """
        return self._invoke('cancel', None)
class _InstallStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/deployment/install',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Install.InstallSpec'),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/install?action=check',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for start operation
        start_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Install.InstallSpec'),
        })
        start_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        start_input_value_validator_list = [
        ]
        start_output_validator_list = [
        ]
        start_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/install?action=start',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for cancel operation
        cancel_input_type = type.StructType('operation-input', {})
        cancel_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        cancel_input_value_validator_list = [
        ]
        cancel_output_validator_list = [
        ]
        cancel_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/install?action=cancel',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Install.InstallSpec'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check': {
                'input_type': check_input_type,
                'output_type': type.ReferenceType(__name__, 'CheckInfo'),
                'errors': check_error_dict,
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': check_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'start': {
                'input_type': start_input_type,
                'output_type': type.VoidType(),
                'errors': start_error_dict,
                'input_value_validator_list': start_input_value_validator_list,
                'output_validator_list': start_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel': {
                'input_type': cancel_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_error_dict,
                'input_value_validator_list': cancel_input_value_validator_list,
                'output_validator_list': cancel_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'check': check_rest_metadata,
            'start': start_rest_metadata,
            'cancel': cancel_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.deployment.install',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _UpgradeStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/deployment/upgrade',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Upgrade.UpgradeSpec'),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/upgrade?action=check',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for start operation
        start_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Upgrade.UpgradeSpec'),
        })
        start_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        start_input_value_validator_list = [
        ]
        start_output_validator_list = [
        ]
        start_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/upgrade?action=start',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for cancel operation
        cancel_input_type = type.StructType('operation-input', {})
        cancel_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        cancel_input_value_validator_list = [
        ]
        cancel_output_validator_list = [
        ]
        cancel_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/upgrade?action=cancel',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Upgrade.UpgradeSpec'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check': {
                'input_type': check_input_type,
                'output_type': type.ReferenceType(__name__, 'CheckInfo'),
                'errors': check_error_dict,
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': check_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'start': {
                'input_type': start_input_type,
                'output_type': type.VoidType(),
                'errors': start_error_dict,
                'input_value_validator_list': start_input_value_validator_list,
                'output_validator_list': start_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel': {
                'input_type': cancel_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_error_dict,
                'input_value_validator_list': cancel_input_value_validator_list,
                'output_validator_list': cancel_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'check': check_rest_metadata,
            'start': start_rest_metadata,
            'cancel': cancel_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.deployment.upgrade',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _MigrateStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/deployment/migrate',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Migrate.MigrateSpec'),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/migrate?action=check',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for start operation
        start_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Migrate.MigrateSpec'),
        })
        start_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        start_input_value_validator_list = [
        ]
        start_output_validator_list = [
        ]
        start_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/migrate?action=start',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for cancel operation
        cancel_input_type = type.StructType('operation-input', {})
        cancel_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        cancel_input_value_validator_list = [
        ]
        cancel_output_validator_list = [
        ]
        cancel_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/migrate?action=cancel',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Migrate.MigrateSpec'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check': {
                'input_type': check_input_type,
                'output_type': type.ReferenceType(__name__, 'CheckInfo'),
                'errors': check_error_dict,
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': check_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'start': {
                'input_type': start_input_type,
                'output_type': type.VoidType(),
                'errors': start_error_dict,
                'input_value_validator_list': start_input_value_validator_list,
                'output_validator_list': start_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel': {
                'input_type': cancel_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_error_dict,
                'input_value_validator_list': cancel_input_value_validator_list,
                'output_validator_list': cancel_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'check': check_rest_metadata,
            'start': start_rest_metadata,
            'cancel': cancel_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.deployment.migrate',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _QuestionStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.internal_server_error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InternalServerError'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/deployment/question',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for answer operation
        answer_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Question.AnswerSpec'),
        })
        answer_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.internal_server_error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InternalServerError'),

        }
        answer_input_value_validator_list = [
        ]
        answer_output_validator_list = [
        ]
        answer_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/question?action=answer',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Question.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'answer': {
                'input_type': answer_input_type,
                'output_type': type.VoidType(),
                'errors': answer_error_dict,
                'input_value_validator_list': answer_input_value_validator_list,
                'output_validator_list': answer_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'answer': answer_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.deployment.question',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ImportHistoryStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/deployment/history',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for start operation
        start_input_type = type.StructType('operation-input', {
            'spec': type.OptionalType(type.ReferenceType(__name__, 'ImportHistory.CreateSpec')),
        })
        start_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        start_input_value_validator_list = [
        ]
        start_output_validator_list = [
        ]
        start_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/history?action=start',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for pause operation
        pause_input_type = type.StructType('operation-input', {})
        pause_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        pause_input_value_validator_list = [
        ]
        pause_output_validator_list = [
        ]
        pause_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/history?action=pause',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for resume operation
        resume_input_type = type.StructType('operation-input', {})
        resume_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        resume_input_value_validator_list = [
        ]
        resume_output_validator_list = [
        ]
        resume_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/history?action=resume',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for cancel operation
        cancel_input_type = type.StructType('operation-input', {})
        cancel_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        cancel_input_value_validator_list = [
        ]
        cancel_output_validator_list = [
        ]
        cancel_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment/history?action=cancel',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'ImportHistory.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'start': {
                'input_type': start_input_type,
                'output_type': type.VoidType(),
                'errors': start_error_dict,
                'input_value_validator_list': start_input_value_validator_list,
                'output_validator_list': start_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'pause': {
                'input_type': pause_input_type,
                'output_type': type.VoidType(),
                'errors': pause_error_dict,
                'input_value_validator_list': pause_input_value_validator_list,
                'output_validator_list': pause_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'resume': {
                'input_type': resume_input_type,
                'output_type': type.VoidType(),
                'errors': resume_error_dict,
                'input_value_validator_list': resume_input_value_validator_list,
                'output_validator_list': resume_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel': {
                'input_type': cancel_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_error_dict,
                'input_value_validator_list': cancel_input_value_validator_list,
                'output_validator_list': cancel_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'start': start_rest_metadata,
            'pause': pause_rest_metadata,
            'resume': resume_rest_metadata,
            'cancel': cancel_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.deployment.import_history',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Install': Install,
        'Upgrade': Upgrade,
        'Migrate': Migrate,
        'Question': Question,
        'ImportHistory': ImportHistory,
        'install': 'com.vmware.vcenter.deployment.install_client.StubFactory',
        'migrate': 'com.vmware.vcenter.deployment.migrate_client.StubFactory',
    }

