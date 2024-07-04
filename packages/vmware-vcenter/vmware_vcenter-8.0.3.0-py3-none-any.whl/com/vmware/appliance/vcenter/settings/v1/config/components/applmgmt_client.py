# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.
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


class ApplianceManagement(VapiStruct):
    """
    ``ApplianceManagement`` class This structure contains the Spec required for
    Appliance Management configurations.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 software_update_policy=None,
                 backup_schedules=None,
                 access_settings=None,
                 datetime_config=None,
                 syslog=None,
                 user_account_settings=None,
                 smtp=None,
                 network=None,
                 ceip=None,
                ):
        """
        :type  software_update_policy: :class:`SoftwareUpdatePolicy` or ``None``
        :param software_update_policy: Policy to update vCenter.
            Only :class:`set` if the SoftwareUpdatePolicy is set inside
            vCenter.
        :type  backup_schedules: :class:`list` of :class:`BackupSchedule` or ``None``
        :param backup_schedules: Backup schedule of vCenter.
            Only :class:`set` if the Backup is schedule for vCenter
        :type  access_settings: :class:`AccessSettings` or ``None``
        :param access_settings: AccessSettings of vCenter. if access settings are set for vCenter
        :type  datetime_config: :class:`DatetimeConfig` or ``None``
        :param datetime_config: Date Time Configuration of vCenter.
            Only :class:`set` if access settings are set for vCenter
        :type  syslog: :class:`list` of :class:`LogForwarding` or ``None``
        :param syslog: The ``syslog`` class provides methods to manage forwarding of log
            messages to remote logging servers.
            Only :class:`set` if log forwarding to remote server are set in
            vCenter.
        :type  user_account_settings: :class:`UserAccountSettings` or ``None``
        :param user_account_settings: User Account Settings of vCenter. if user account settings are set
            for vCenter
        :type  smtp: :class:`Smtp` or ``None``
        :param smtp: The ``LocalAccounts`` class provides methods to manage local user
            account.
        :type  network: :class:`ApplianceNetwork` or ``None``
        :param network: Network configurations to be applied.
            Only :class:`set` if the network configurations are set in vCenter.
        :type  ceip: :class:`Ceip` or ``None``
        :param ceip: CEIP (Customer Experience Improvement Program) enabled state.
            Only :class:`set` if ceip are set in vcenter.
        """
        self.software_update_policy = software_update_policy
        self.backup_schedules = backup_schedules
        self.access_settings = access_settings
        self.datetime_config = datetime_config
        self.syslog = syslog
        self.user_account_settings = user_account_settings
        self.smtp = smtp
        self.network = network
        self.ceip = ceip
        VapiStruct.__init__(self)


ApplianceManagement._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.appliance_management', {
        'software_update_policy': type.OptionalType(type.ReferenceType(__name__, 'SoftwareUpdatePolicy')),
        'backup_schedules': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'BackupSchedule'))),
        'access_settings': type.OptionalType(type.ReferenceType(__name__, 'AccessSettings')),
        'datetime_config': type.OptionalType(type.ReferenceType(__name__, 'DatetimeConfig')),
        'syslog': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'LogForwarding'))),
        'user_account_settings': type.OptionalType(type.ReferenceType(__name__, 'UserAccountSettings')),
        'smtp': type.OptionalType(type.ReferenceType(__name__, 'Smtp')),
        'network': type.OptionalType(type.ReferenceType(__name__, 'ApplianceNetwork')),
        'ceip': type.OptionalType(type.ReferenceType(__name__, 'Ceip')),
    },
    ApplianceManagement,
    False,
    None))



class DatetimeConfig(VapiStruct):
    """
    This ``DatetimeConfig`` class to set/get date time settings.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 time_zone=None,
                 time_sync=None,
                 ntp=None,
                ):
        """
        :type  time_zone: :class:`Timezone` or ``None``
        :param time_zone: The ``Timezone`` class provides methods to get and set the
            appliance timezone.
            Only :class:`set` if the Timezone is set in vCenter
        :type  time_sync: :class:`Timesync` or ``None``
        :param time_sync: ``Timesync`` class provides methods Performs time synchronization
            configuration.
            Only :class:`set` if the time sync mode is set in vCenter
        :type  ntp: :class:`Ntp` or ``None``
        :param ntp: ``Ntp`` class provides methods Gets NTP configuration status and
            tests connection to ntp servers.
            Only :class:`set` if the ntp server are set in vCenter.
        """
        self.time_zone = time_zone
        self.time_sync = time_sync
        self.ntp = ntp
        VapiStruct.__init__(self)


DatetimeConfig._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.datetime_config', {
        'time_zone': type.OptionalType(type.ReferenceType(__name__, 'Timezone')),
        'time_sync': type.OptionalType(type.ReferenceType(__name__, 'Timesync')),
        'ntp': type.OptionalType(type.ReferenceType(__name__, 'Ntp')),
    },
    DatetimeConfig,
    False,
    None))



class AccessSettings(VapiStruct):
    """
    This ``AccessSettings`` class to set/get access settings.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 ssh=None,
                 dcui=None,
                 console_cli=None,
                 shell=None,
                ):
        """
        :type  ssh: :class:`Ssh` or ``None``
        :param ssh: Get/Set enabled state of SSH-based controlled CLI. ``Ssh`` class
            provides methods
        :type  dcui: :class:`Dcui` or ``None``
        :param dcui: Get/Set enabled of Direct Console User Interface (DCUI TTY2).
            ``Dcui`` class provides methods
        :type  console_cli: :class:`Consolecli` or ``None``
        :param console_cli: Get/Set enabled state of the console-based controlled CLI.
            ``Consolecli`` class provides methods
        :type  shell: :class:`Shell` or ``None``
        :param shell: Get/Set enabled state of BASH. ``Shell`` class provides methods
        """
        self.ssh = ssh
        self.dcui = dcui
        self.console_cli = console_cli
        self.shell = shell
        VapiStruct.__init__(self)


AccessSettings._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.access_settings', {
        'ssh': type.OptionalType(type.ReferenceType(__name__, 'Ssh')),
        'dcui': type.OptionalType(type.ReferenceType(__name__, 'Dcui')),
        'console_cli': type.OptionalType(type.ReferenceType(__name__, 'Consolecli')),
        'shell': type.OptionalType(type.ReferenceType(__name__, 'Shell')),
    },
    AccessSettings,
    False,
    None))



class UserAccountSettings(VapiStruct):
    """
    This ``UserAccountSettings`` class to set/get user account settings.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 local_accounts_policy=None,
                 root_account_policy=None,
                ):
        """
        :type  local_accounts_policy: :class:`LocalAccountsPolicy` or ``None``
        :param local_accounts_policy: The ``localAccountsPolicy`` class provides methods to manage local
            user accounts.
            Only :class:`set` if Password Policy is set to manage local user
            accounts.
        :type  root_account_policy: :class:`LocalAccounts` or ``None``
        :param root_account_policy: The ``LocalAccounts`` class provides methods to manage local user
            account.
        """
        self.local_accounts_policy = local_accounts_policy
        self.root_account_policy = root_account_policy
        VapiStruct.__init__(self)


UserAccountSettings._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.user_account_settings', {
        'local_accounts_policy': type.OptionalType(type.ReferenceType(__name__, 'LocalAccountsPolicy')),
        'root_account_policy': type.OptionalType(type.ReferenceType(__name__, 'LocalAccounts')),
    },
    UserAccountSettings,
    False,
    None))



class SoftwareUpdatePolicy(VapiStruct):
    """
    This ``SoftwareUpdatePolicy`` class to set/get background check for the new
    updates.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'default_URL': 'default_url',
                            'enable_SSL_cert_validation': 'enable_ssl_cert_validation',
                            }

    def __init__(self,
                 url=None,
                 default_url=None,
                 auto_stage=None,
                 check_schedule=None,
                 username=None,
                 password=None,
                 enable_ssl_cert_validation=None,
                ):
        """
        :type  url: :class:`str` or ``None``
        :param url: Current appliance update repository URL. Enter "default" to reset
            the url to the default url.
            Only :class:`set` if custom URL required
        :type  default_url: :class:`str` or ``None``
        :param default_url: Default appliance update repository URL.
            Only :class:`set` if default URL required
        :type  auto_stage: :class:`bool` or ``None``
        :param auto_stage: Check for update at the pre-configured repository URL.
            Only :class:`set` if auto stage is enable.
        :type  check_schedule: :class:`list` of :class:`Time` or ``None``
        :param check_schedule: The ``Time`` class defines day and time the automatic check for new
            updates will be run.
            Only :class:`set` if Time required.
        :type  username: :class:`str` or ``None``
        :param username: Username for the url update repository
            Only :class:`set` if SoftwareUpdatePolicy requires username.
        :type  password: :class:`str` or ``None``
        :param password: Password for the url update repository
            Only :class:`set` if SoftwareUpdatePolicy requires password.
        :type  enable_ssl_cert_validation: :class:`bool` or ``None``
        :param enable_ssl_cert_validation: Indicates whether certificates will be checked during patching. 
            
            Warning: If this attribute is set to false, an insecure connection
            is made to the update repository which can potentially put the
            appliance security at risk.
        """
        self.url = url
        self.default_url = default_url
        self.auto_stage = auto_stage
        self.check_schedule = check_schedule
        self.username = username
        self.password = password
        self.enable_ssl_cert_validation = enable_ssl_cert_validation
        VapiStruct.__init__(self)


    class AutoUpdateNotification(Enum):
        """
        Defines state for automatic update notification.
        ``SoftwareUpdatePolicy.AutoUpdateNotification`` class

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DISABLED = None
        """
        Automatic update notification is disabled. Disable periodically query the
        configured url for updates.

        """
        ENABLED = None
        """
        Automatic update notification is enabled. Enable periodically query the
        configured url for updates.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`AutoUpdateNotification` instance.
            """
            Enum.__init__(string)

    AutoUpdateNotification._set_values({
        'DISABLED': AutoUpdateNotification('DISABLED'),
        'ENABLED': AutoUpdateNotification('ENABLED'),
    })
    AutoUpdateNotification._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.software_update_policy.auto_update_notification',
        AutoUpdateNotification))

SoftwareUpdatePolicy._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.software_update_policy', {
        'url': type.OptionalType(type.StringType()),
        'default_URL': type.OptionalType(type.StringType()),
        'auto_stage': type.OptionalType(type.BooleanType()),
        'check_schedule': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Time'))),
        'username': type.OptionalType(type.StringType()),
        'password': type.OptionalType(type.SecretType()),
        'enable_SSL_cert_validation': type.OptionalType(type.BooleanType()),
    },
    SoftwareUpdatePolicy,
    False,
    None))



class Time(VapiStruct):
    """
    The ``Time`` class defines weekday and time the automatic check for new
    updates will be run

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 hour=None,
                 minute=None,
                 day=None,
                ):
        """
        :type  hour: :class:`str` or ``None``
        :param hour: Time to query for updates Format: HH:MM:SS Military (24 hour) Time
            Format
            Only :class:`set` if hour is present in SoftwareUpdatePolicy
        :type  minute: :class:`str` or ``None``
        :param minute: Time to query for updates Format: HH:MM:SS Military (24 hour) Time
            Format
            Only :class:`set` if minute is present in SoftwareUpdatePolicy
        :type  day: :class:`Time.UpdateDay` or ``None``
        :param day: Day to query for updates
            Only :class:`set` if minute is present in SoftwareUpdatePolicy
        """
        self.hour = hour
        self.minute = minute
        self.day = day
        VapiStruct.__init__(self)


    class UpdateDay(Enum):
        """
        ``Time.UpdateDay`` class Defines days to query for updates.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        MONDAY = None
        """
        Query for updates on Monday.

        """
        TUESDAY = None
        """
        Query for updates on Tuesday.

        """
        FRIDAY = None
        """
        Query for updates on Friday.

        """
        WEDNESDAY = None
        """
        Query for updates on Wednesday.

        """
        THURSDAY = None
        """
        Query for updates on Thursday.

        """
        SATURDAY = None
        """
        Query for updates on Saturday.

        """
        SUNDAY = None
        """
        Query for updates on Sunday.

        """
        EVERYDAY = None
        """
        Query for updates everyday.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`UpdateDay` instance.
            """
            Enum.__init__(string)

    UpdateDay._set_values({
        'MONDAY': UpdateDay('MONDAY'),
        'TUESDAY': UpdateDay('TUESDAY'),
        'FRIDAY': UpdateDay('FRIDAY'),
        'WEDNESDAY': UpdateDay('WEDNESDAY'),
        'THURSDAY': UpdateDay('THURSDAY'),
        'SATURDAY': UpdateDay('SATURDAY'),
        'SUNDAY': UpdateDay('SUNDAY'),
        'EVERYDAY': UpdateDay('EVERYDAY'),
    })
    UpdateDay._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.time.update_day',
        UpdateDay))

Time._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.time', {
        'hour': type.OptionalType(type.StringType()),
        'minute': type.OptionalType(type.StringType()),
        'day': type.OptionalType(type.ReferenceType(__name__, 'Time.UpdateDay')),
    },
    Time,
    False,
    None))



class RetentionInfo(VapiStruct):
    """
    The ``RetentionInfo`` class contains retention information associated with
    a schedule.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 max_count=None,
                ):
        """
        :type  max_count: :class:`long`
        :param max_count: Number of backups which should be retained. If retention is not
            set, all the backups will be retained forever.
        """
        self.max_count = max_count
        VapiStruct.__init__(self)


RetentionInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.retention_info', {
        'max_count': type.IntegerType(),
    },
    RetentionInfo,
    False,
    None))



class RecurrenceInfo(VapiStruct):
    """
    The ``RecurrenceInfo`` class contains the recurrence information associated
    with a schedule.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 minute=None,
                 hour=None,
                 days=None,
                ):
        """
        :type  minute: :class:`long`
        :param minute: Minute when backup should run.
        :type  hour: :class:`long`
        :param hour: Hour when backup should run. The hour should be specified in
            24-hour clock format.
        :type  days: :class:`list` of :class:`RecurrenceInfo.DayOfWeek` or ``None``
        :param days: Day of week when the backup should be run. Days can be specified as
            list of days.
            If None the backup will be run everyday.
        """
        self.minute = minute
        self.hour = hour
        self.days = days
        VapiStruct.__init__(self)


    class DayOfWeek(Enum):
        """
        The ``RecurrenceInfo.DayOfWeek`` class defines the set of days when backup
        can be scheduled. The days can be specified as a list of individual days.
        You specify the days when you set the recurrence for a schedule. See
        :attr:`RecurrenceInfo.days`.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        MONDAY = None
        """
        Monday

        """
        TUESDAY = None
        """
        Tuesday

        """
        WEDNESDAY = None
        """
        Wednesday

        """
        THURSDAY = None
        """
        Thursday

        """
        FRIDAY = None
        """
        Friday

        """
        SATURDAY = None
        """
        Saturday

        """
        SUNDAY = None
        """
        Sunday

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`DayOfWeek` instance.
            """
            Enum.__init__(string)

    DayOfWeek._set_values({
        'MONDAY': DayOfWeek('MONDAY'),
        'TUESDAY': DayOfWeek('TUESDAY'),
        'WEDNESDAY': DayOfWeek('WEDNESDAY'),
        'THURSDAY': DayOfWeek('THURSDAY'),
        'FRIDAY': DayOfWeek('FRIDAY'),
        'SATURDAY': DayOfWeek('SATURDAY'),
        'SUNDAY': DayOfWeek('SUNDAY'),
    })
    DayOfWeek._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.recurrence_info.day_of_week',
        DayOfWeek))

RecurrenceInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.recurrence_info', {
        'minute': type.IntegerType(),
        'hour': type.IntegerType(),
        'days': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'RecurrenceInfo.DayOfWeek'))),
    },
    RecurrenceInfo,
    False,
    None))



class BackupSchedule(VapiStruct):
    """
    The ``BackupSchedule`` class contains fields to be specified for creating a
    new schedule. The structure includes parts, location information,
    encryption password and enable flag.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 parts=None,
                 backup_password=None,
                 location=None,
                 location_user=None,
                 location_password=None,
                 enable=None,
                 recurrence_info=None,
                 retention_info=None,
                 schedule_id=None,
                ):
        """
        :type  parts: :class:`list` of :class:`str` or ``None``
        :param parts: List of optional parts to be backed up. Use the
            com.vmware.appliance.recovery.backup.Parts#list method to get
            information about the supported parts.
            If None all the optional parts will not be backed up.
        :type  backup_password: :class:`str` or ``None``
        :param backup_password: Password for a backup piece. The backupPassword must adhere to the
            following password requirements: At least 8 characters, cannot be
            more than 20 characters in length. At least 1 uppercase letter. At
            least 1 lowercase letter. At least 1 numeric digit. At least 1
            special character (i.e. any character not in [0-9,a-z,A-Z]). Only
            visible ASCII characters (for example, no space).
            If None the backup piece will not be encrypted.
        :type  location: :class:`str`
        :param location: URL of the backup location.
        :type  location_user: :class:`str` or ``None``
        :param location_user: Username for the given location.
            If None authentication will not be used for the specified location.
        :type  location_password: :class:`str` or ``None``
        :param location_password: Password for the given location.
            If None authentication will not be used for the specified location.
        :type  enable: :class:`bool` or ``None``
        :param enable: Enable or disable a schedule.
            If None the schedule will be enabled.
        :type  recurrence_info: :class:`RecurrenceInfo` or ``None``
        :param recurrence_info: Recurrence information for the schedule.
            If None backup job will not be scheduled. See
            :class:`RecurrenceInfo`
        :type  retention_info: :class:`RetentionInfo` or ``None``
        :param retention_info: Retention information for the schedule.
            If None all the completed backup jobs will be retained forever. See
            :class:`RetentionInfo`
        :type  schedule_id: :class:`str`
        :param schedule_id: Identifier of the schedule.
        """
        self.parts = parts
        self.backup_password = backup_password
        self.location = location
        self.location_user = location_user
        self.location_password = location_password
        self.enable = enable
        self.recurrence_info = recurrence_info
        self.retention_info = retention_info
        self.schedule_id = schedule_id
        VapiStruct.__init__(self)


BackupSchedule._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.backup_schedule', {
        'parts': type.OptionalType(type.ListType(type.StringType())),
        'backup_password': type.OptionalType(type.SecretType()),
        'location': type.URIType(),
        'location_user': type.OptionalType(type.StringType()),
        'location_password': type.OptionalType(type.SecretType()),
        'enable': type.OptionalType(type.BooleanType()),
        'recurrence_info': type.OptionalType(type.ReferenceType(__name__, 'RecurrenceInfo')),
        'retention_info': type.OptionalType(type.ReferenceType(__name__, 'RetentionInfo')),
        'schedule_id': type.StringType(),
    },
    BackupSchedule,
    False,
    None))



class Ssh(VapiStruct):
    """
    ``Ssh`` class provides methods to Get/Set enabled state of SSH-based
    controlled CLI.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Set enabled state of the SSH-based controlled CLI.
        """
        self.enabled = enabled
        VapiStruct.__init__(self)


Ssh._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.ssh', {
        'enabled': type.OptionalType(type.BooleanType()),
    },
    Ssh,
    False,
    None))



class Consolecli(VapiStruct):
    """
    Get/Set of the console-based controlled CLI. ``Consolecli`` class provides
    methods

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Set enabled state of the console-based controlled CLI (TTY1).
        """
        self.enabled = enabled
        VapiStruct.__init__(self)


Consolecli._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.consolecli', {
        'enabled': type.OptionalType(type.BooleanType()),
    },
    Consolecli,
    False,
    None))



class Dcui(VapiStruct):
    """
    Get/Set enabled state of Direct Console User Interface (DCUI TTY2).
    ``Dcui`` class provides methods

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Set enabled state of Direct Console User Interface (DCUI).
        """
        self.enabled = enabled
        VapiStruct.__init__(self)


Dcui._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.dcui', {
        'enabled': type.OptionalType(type.BooleanType()),
    },
    Dcui,
    False,
    None))



class Shell(VapiStruct):
    """
    Get/Set enabled state of BASH, that is, access to BASH from within the
    controlled CLI. ``Shell`` class provides methods.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                 timeout=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Enabled can be set to true or false
        :type  timeout: :class:`long`
        :param timeout: The timeout (in seconds) specifies how long you enable the Shell
            access. The maximum timeout is 86400 seconds(1 day).
        """
        self.enabled = enabled
        self.timeout = timeout
        VapiStruct.__init__(self)


Shell._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.shell', {
        'enabled': type.OptionalType(type.BooleanType()),
        'timeout': type.IntegerType(),
    },
    Shell,
    False,
    None))



class Timezone(VapiStruct):
    """
    The ``Timezone`` class provides methods to get and set the appliance
    timezone.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Set time zone.
        """
        self.name = name
        VapiStruct.__init__(self)


Timezone._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.timezone', {
        'name': type.OptionalType(type.StringType()),
    },
    Timezone,
    False,
    None))



class Timesync(VapiStruct):
    """
    ``Timesync`` class provides methods Performs time synchronization
    configuration.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 mode=None,
                ):
        """
        :type  mode: :class:`Timesync.TimeSyncMode`
        :param mode: 
        """
        self.mode = mode
        VapiStruct.__init__(self)


    class TimeSyncMode(Enum):
        """
        The ``Timesync.TimeSyncMode`` class defines time synchronization modes

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DISABLED = None
        """
        Time synchronization is disabled.

        """
        NTP = None
        """
        NTP-based time synchronization.

        """
        HOST = None
        """
        VMware Tool-based time synchronization.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`TimeSyncMode` instance.
            """
            Enum.__init__(string)

    TimeSyncMode._set_values({
        'DISABLED': TimeSyncMode('DISABLED'),
        'NTP': TimeSyncMode('NTP'),
        'HOST': TimeSyncMode('HOST'),
    })
    TimeSyncMode._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.timesync.time_sync_mode',
        TimeSyncMode))

Timesync._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.timesync', {
        'mode': type.ReferenceType(__name__, 'Timesync.TimeSyncMode'),
    },
    Timesync,
    False,
    None))



class Ntp(VapiStruct):
    """
    ``Ntp`` class provides methods Get/Set NTP configuration status and tests
    connection to ntp servers.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 servers=None,
                ):
        """
        :type  servers: :class:`list` of :class:`str`
        :param servers: Set NTP servers. This variable updates old NTP servers from
            configuration and sets the input NTP servers in the configuration.
        """
        self.servers = servers
        VapiStruct.__init__(self)


Ntp._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.ntp', {
        'servers': type.ListType(type.StringType()),
    },
    Ntp,
    False,
    None))



class LogForwarding(VapiStruct):
    """
    The ``LogForwarding`` class provides methods to manage forwarding of log
    messages to remote logging servers.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 hostname=None,
                 port=None,
                 protocol=None,
                ):
        """
        :type  hostname: :class:`str` or ``None``
        :param hostname: FQDN or IP address of the logging server to which messages are
            forwarded.
        :type  port: :class:`long` or ``None``
        :param port: The port on which the remote logging server is listening for
            forwarded log messages.
        :type  protocol: :class:`LogForwarding.Protocol` or ``None``
        :param protocol: Transport protocol used to forward log messages.
        """
        self.hostname = hostname
        self.port = port
        self.protocol = protocol
        VapiStruct.__init__(self)


    class Protocol(Enum):
        """
        The ``LogForwarding.Protocol`` class defines transport protocols for
        outbound log messages.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        TLS = None
        """
        Log messages will be forwarded to the remote host by using the TLS
        protocol.

        """
        UDP = None
        """
        Log messages will be forwarded to the remote host using the UDP protocol.

        """
        TCP = None
        """
        Log messages will be forwarded to the remote host using the TCP protocol.

        """
        RELP = None
        """
        Log messages will be forwarded to the remote host using the RELP protocol.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Protocol` instance.
            """
            Enum.__init__(string)

    Protocol._set_values({
        'TLS': Protocol('TLS'),
        'UDP': Protocol('UDP'),
        'TCP': Protocol('TCP'),
        'RELP': Protocol('RELP'),
    })
    Protocol._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.log_forwarding.protocol',
        Protocol))

LogForwarding._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.log_forwarding', {
        'hostname': type.OptionalType(type.StringType()),
        'port': type.OptionalType(type.IntegerType()),
        'protocol': type.OptionalType(type.ReferenceType(__name__, 'LogForwarding.Protocol')),
    },
    LogForwarding,
    False,
    None))



class LocalAccountsPolicy(VapiStruct):
    """
    The ``LocalAccountsPolicy`` class provides methods to manage local user
    accounts password lifecycle.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 max_days=None,
                 min_days=None,
                 warn_days=None,
                ):
        """
        :type  max_days: :class:`long` or ``None``
        :param max_days: Maximum number of days a password may be used. If the password is
            older than this, a password change will be forced.
            If None then the restriction will be ignored.
        :type  min_days: :class:`long` or ``None``
        :param min_days: Minimum number of days allowed between password changes. Any
            password changes attempted sooner than this will be rejected.
            If None then the restriction will be ignored.
        :type  warn_days: :class:`long` or ``None``
        :param warn_days: Number of days warning given before a password expires. A zero
            means warning is given only upon the day of expiration.
            If None then no warning will be provided.
        """
        self.max_days = max_days
        self.min_days = min_days
        self.warn_days = warn_days
        VapiStruct.__init__(self)


LocalAccountsPolicy._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.local_accounts_policy', {
        'max_days': type.OptionalType(type.IntegerType()),
        'min_days': type.OptionalType(type.IntegerType()),
        'warn_days': type.OptionalType(type.IntegerType()),
    },
    LocalAccountsPolicy,
    False,
    None))



class LocalAccounts(VapiStruct):
    """
    The ``LocalAccounts`` class provides methods to manage local user account.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 fullname=None,
                 roles=None,
                 enabled=None,
                 has_password=None,
                 min_days_between_password_change=None,
                 max_days_between_password_change=None,
                 warn_days_before_password_expiration=None,
                 password=None,
                 email=None,
                ):
        """
        :type  fullname: :class:`str` or ``None``
        :param fullname: Full name of the user
            If None, the value was never set.
        :type  roles: :class:`list` of :class:`str` or ``None``
        :param roles: User roles
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Flag indicating if the account is enabled
        :type  has_password: :class:`bool` or ``None``
        :param has_password: Is the user password set.
        :type  min_days_between_password_change: :class:`long` or ``None``
        :param min_days_between_password_change: Minimum number of days between password change
            If None, pasword can be changed any time.
        :type  max_days_between_password_change: :class:`long` or ``None``
        :param max_days_between_password_change: Maximum number of days between password change
            If None, password never expires.
        :type  warn_days_before_password_expiration: :class:`long` or ``None``
        :param warn_days_before_password_expiration: Number of days of warning before password expires
            If None, a user is never warned.
        :type  password: :class:`str` or ``None``
        :param password: Password
            If None, value will not be changed
        :type  email: :class:`str` or ``None``
        :param email: Email address of the local account
            If None, value will not be changed
        """
        self.fullname = fullname
        self.roles = roles
        self.enabled = enabled
        self.has_password = has_password
        self.min_days_between_password_change = min_days_between_password_change
        self.max_days_between_password_change = max_days_between_password_change
        self.warn_days_before_password_expiration = warn_days_before_password_expiration
        self.password = password
        self.email = email
        VapiStruct.__init__(self)


LocalAccounts._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.local_accounts', {
        'fullname': type.OptionalType(type.StringType()),
        'roles': type.OptionalType(type.ListType(type.StringType())),
        'enabled': type.OptionalType(type.BooleanType()),
        'has_password': type.OptionalType(type.BooleanType()),
        'min_days_between_password_change': type.OptionalType(type.IntegerType()),
        'max_days_between_password_change': type.OptionalType(type.IntegerType()),
        'warn_days_before_password_expiration': type.OptionalType(type.IntegerType()),
        'password': type.OptionalType(type.SecretType()),
        'email': type.OptionalType(type.StringType()),
    },
    LocalAccounts,
    False,
    None))



class Smtp(VapiStruct):
    """
    The ``Smtp`` class provides methods to manage send mail configuration.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 mail_server=None,
                 relay_port=None,
                ):
        """
        :type  mail_server: :class:`str` or ``None``
        :param mail_server: Mail server IP address.
            If None then the value will be ignored.
        :type  relay_port: :class:`str` or ``None``
        :param relay_port: Relay port number.
            If None then the value will be ignored.
        """
        self.mail_server = mail_server
        self.relay_port = relay_port
        VapiStruct.__init__(self)


Smtp._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.smtp', {
        'mail_server': type.OptionalType(type.StringType()),
        'relay_port': type.OptionalType(type.StringType()),
    },
    Smtp,
    False,
    None))



class Ceip(VapiStruct):
    """
    ``Ceip`` class provides methods to Get/Set enabled state of CEIP (Customer
    Experience Improvement Program) value.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Set enabled state of the CEIP.
        """
        self.enabled = enabled
        VapiStruct.__init__(self)


Ceip._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.ceip', {
        'enabled': type.OptionalType(type.BooleanType()),
    },
    Ceip,
    False,
    None))



class ApplianceNetwork(VapiStruct):
    """
    ``ApplianceNetwork`` class This structure contains the Spec required for
    Appliance Network configurations.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 firewall_rule_policies=None,
                 dns_server_configuration=None,
                 proxy_configuration=None,
                 interfaces=None,
                ):
        """
        :type  firewall_rule_policies: :class:`list` of :class:`FirewallRulePolicy` or ``None``
        :param firewall_rule_policies: List of Firewall Rules to be applied.
            Only :class:`set` if the FirewallRulePolicy is set in vCenter.
        :type  dns_server_configuration: :class:`DnsServerConfiguration` or ``None``
        :param dns_server_configuration: DNS configuration to be applied.
            Only :class:`set` if the DnsServerConfiguration is set in vCenter.
        :type  proxy_configuration: :class:`list` of :class:`ProxyConfiguration` or ``None``
        :param proxy_configuration: Proxy configuration to be applied.
            Only :class:`set` if the Proxy server configuration is set in
            vCenter.
        :type  interfaces: :class:`list` of :class:`Interface` or ``None``
        :param interfaces: Interfaces configuration to be applied.
            Only :class:`set` if the Interfaces configuration is set in
            vCenter.
        """
        self.firewall_rule_policies = firewall_rule_policies
        self.dns_server_configuration = dns_server_configuration
        self.proxy_configuration = proxy_configuration
        self.interfaces = interfaces
        VapiStruct.__init__(self)


ApplianceNetwork._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.appliance_network', {
        'firewall_rule_policies': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FirewallRulePolicy'))),
        'dns_server_configuration': type.OptionalType(type.ReferenceType(__name__, 'DnsServerConfiguration')),
        'proxy_configuration': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ProxyConfiguration'))),
        'interfaces': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Interface'))),
    },
    ApplianceNetwork,
    False,
    None))



class DnsServerConfiguration(VapiStruct):
    """
    ``DnsServerConfiguration`` class This structure represents the
    configuration state used to determine DNS servers.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 mode=None,
                 servers=None,
                 domains=None,
                ):
        """
        :type  mode: :class:`DnsServerConfiguration.DNSServerMode`
        :param mode: Define how to determine the DNS servers. Leave the servers argument
            empty if the mode argument is "DHCP". Set the servers argument to a
            comma-separated list of DNS servers if the mode argument is
            "static". The DNS server are assigned from the specified list.
        :type  servers: :class:`list` of :class:`str`
        :param servers: List of the currently used DNS servers. DNS server configuration.
        :type  domains: :class:`list` of :class:`str` or ``None``
        :param domains: List of the search domains. DNS Search Domains.
        """
        self.mode = mode
        self.servers = servers
        self.domains = domains
        VapiStruct.__init__(self)


    class DNSServerMode(Enum):
        """
        ``DnsServerConfiguration.DNSServerMode`` class Describes DNS Server source
        (DHCP,static).

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DHCP = None
        """
        DNS address is automatically assigned by a DHCP server.

        """
        IS_STATIC = None
        """
        DNS address is static.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`DNSServerMode` instance.
            """
            Enum.__init__(string)

    DNSServerMode._set_values({
        'DHCP': DNSServerMode('DHCP'),
        'IS_STATIC': DNSServerMode('IS_STATIC'),
    })
    DNSServerMode._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.dns_server_configuration.DNS_server_mode',
        DNSServerMode))

DnsServerConfiguration._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.dns_server_configuration', {
        'mode': type.ReferenceType(__name__, 'DnsServerConfiguration.DNSServerMode'),
        'servers': type.ListType(type.StringType()),
        'domains': type.OptionalType(type.ListType(type.StringType())),
    },
    DnsServerConfiguration,
    False,
    None))



class FirewallRulePolicy(VapiStruct):
    """
    ``FirewallRulePolicy`` class Structure that defines a single address-based
    firewall rule.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 address=None,
                 prefix=None,
                 policy=None,
                 interface_name=None,
                ):
        """
        :type  address: :class:`str`
        :param address: IPv4 or IPv6 address.
        :type  prefix: :class:`long`
        :param prefix: CIDR prefix used to mask address. For example, an IPv4 prefix of 24
            ignores the low-order 8 bits of address.
        :type  policy: :class:`FirewallRulePolicy.Policy`
        :param policy: The allow or deny policy of this rule.
        :type  interface_name: :class:`str` or ``None``
        :param interface_name: The interface to which this rule applies. An empty string indicates
            that the rule applies to all interfaces.
            Only :class:`set` if interface name required
        """
        self.address = address
        self.prefix = prefix
        self.policy = policy
        self.interface_name = interface_name
        VapiStruct.__init__(self)


    class Policy(Enum):
        """
        ``FirewallRulePolicy.Policy`` class Defines firewall rule policies.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        IGNORE = None
        """
        Drop packet with correpsonding address.

        """
        ACCEPT = None
        """
        Allow packet with corresponding address.

        """
        REJECT = None
        """
        Drop packet with corresponding address sending destination is not
        reachable.

        """
        RETURN = None
        """
        Apply default or port-specific rules to packet with corresponding address.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Policy` instance.
            """
            Enum.__init__(string)

    Policy._set_values({
        'IGNORE': Policy('IGNORE'),
        'ACCEPT': Policy('ACCEPT'),
        'REJECT': Policy('REJECT'),
        'RETURN': Policy('RETURN'),
    })
    Policy._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.firewall_rule_policy.policy',
        Policy))

FirewallRulePolicy._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.firewall_rule_policy', {
        'address': type.StringType(),
        'prefix': type.IntegerType(),
        'policy': type.ReferenceType(__name__, 'FirewallRulePolicy.Policy'),
        'interface_name': type.OptionalType(type.StringType()),
    },
    FirewallRulePolicy,
    False,
    None))



class ProxyConfiguration(VapiStruct):
    """
    The ``ProxyConfiguration`` class defines proxy configuration.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 protocol=None,
                 server=None,
                 port=None,
                 username=None,
                 password=None,
                 enabled=None,
                ):
        """
        :type  protocol: :class:`ProxyConfiguration.Protocol`
        :param protocol: The protocol for which proxy should be set.
        :type  server: :class:`str` or ``None``
        :param server: URL of the proxy server
            Only :class:`set` if server set in ProxyConfiguration.
        :type  port: :class:`long`
        :param port: Port to connect to the proxy server. In a 'get' call, indicates the
            port connected to the proxy server. In a 'set' call, specifies the
            port to connect to the proxy server. A value of -1 indicates the
            default port.
        :type  username: :class:`str` or ``None``
        :param username: Username for proxy server.
            Only :class:`set` if proxy requires username.
        :type  password: :class:`str` or ``None``
        :param password: Password for proxy server.
            Only :class:`set` if proxy requires password.
        :type  enabled: :class:`bool` or ``None``
        :param enabled: In the result of the ``#get`` and ``#list`` methods this attribute
            indicates whether proxying is enabled for a particular protocol. In
            the input to the ``test`` and ``set`` methods this attribute
            specifies whether proxying should be enabled for a particular
            protocol.
        """
        self.protocol = protocol
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.enabled = enabled
        VapiStruct.__init__(self)


    class Protocol(Enum):
        """
        ``ProxyConfiguration.Protocol`` class defines the protocols for which
        proxying is supported.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        HTTP = None
        """
        Proxy configuration for http.

        """
        HTTPS = None
        """
        Proxy configuration for https.

        """
        FTP = None
        """
        Proxy configuration for ftp.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Protocol` instance.
            """
            Enum.__init__(string)

    Protocol._set_values({
        'HTTP': Protocol('HTTP'),
        'HTTPS': Protocol('HTTPS'),
        'FTP': Protocol('FTP'),
    })
    Protocol._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.proxy_configuration.protocol',
        Protocol))

ProxyConfiguration._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.proxy_configuration', {
        'protocol': type.ReferenceType(__name__, 'ProxyConfiguration.Protocol'),
        'server': type.OptionalType(type.StringType()),
        'port': type.IntegerType(),
        'username': type.OptionalType(type.StringType()),
        'password': type.OptionalType(type.SecretType()),
        'enabled': type.OptionalType(type.BooleanType()),
    },
    ProxyConfiguration,
    False,
    None))



class Interface(VapiStruct):
    """
    ``Interfaces`` class Provides information about network interface.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 status=None,
                 mac=None,
                 ipv4=None,
                 ipv6=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Interface name, for example, "nic0", "nic1".
            If :class:`set`, the name was never set
        :type  status: :class:`Interface.InterfaceStatus` or ``None``
        :param status: Interface status.
            If :class:`set`, the name was never set
        :type  mac: :class:`str` or ``None``
        :param mac: MAC address. For example 00:0C:29:94:BB:5A.
            If :class:`set`, the mac was never set
        :type  ipv4: :class:`Ipv4` or ``None``
        :param ipv4: IPv4 Address information.
            ipv4 This :class:`set` IPv4 is not set.
        :type  ipv6: :class:`Ipv6` or ``None``
        :param ipv6: IPv6 Address information.
            ipv6 This :class:`set` IPv6 is not set.
        """
        self.name = name
        self.status = status
        self.mac = mac
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        VapiStruct.__init__(self)


    class InterfaceStatus(Enum):
        """
        ``Interface.InterfaceStatus`` class Defines interface status

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DOWN = None
        """
        The interface is down.

        """
        UP = None
        """
        The interface is up.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`InterfaceStatus` instance.
            """
            Enum.__init__(string)

    InterfaceStatus._set_values({
        'DOWN': InterfaceStatus('DOWN'),
        'UP': InterfaceStatus('UP'),
    })
    InterfaceStatus._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.interface.interface_status',
        InterfaceStatus))

Interface._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.interface', {
        'name': type.OptionalType(type.StringType()),
        'status': type.OptionalType(type.ReferenceType(__name__, 'Interface.InterfaceStatus')),
        'mac': type.OptionalType(type.StringType()),
        'ipv4': type.OptionalType(type.ReferenceType(__name__, 'Ipv4')),
        'ipv6': type.OptionalType(type.ReferenceType(__name__, 'Ipv6')),
    },
    Interface,
    False,
    None))



class Ipv4(VapiStruct):
    """
    The ``IPv4`` class defines IPv4 configuration. to perform IPv4 network
    configuration for interfaces.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 mode=None,
                 address=None,
                 prefix=None,
                 default_gateway=None,
                 configurable=None,
                ):
        """
        :type  mode: :class:`Ipv4.Mode`
        :param mode: The Address assignment mode.
        :type  address: :class:`str`
        :param address: The IPv4 address, for example, "10.20.80.191".
        :type  prefix: :class:`long`
        :param prefix: The IPv4 CIDR prefix, for example, 24. See
            http://www.oav.net/mirrors/cidr.html for netmask-to-prefix
            conversion.
        :type  default_gateway: :class:`str` or ``None``
        :param default_gateway: The IPv4 address of the default gateway. This configures the global
            default gateway on the appliance with the specified gateway address
            and interface. This gateway replaces the existing default gateway
            configured on the appliance. However, if the gateway address is
            link-local, then it is added for that interface. This does not
            support configuration of multiple global default gateways through
            different interfaces.
            If :class:`set`, the defaultGateway was never set.
        :type  configurable: :class:`bool` or ``None``
        :param configurable: The IPv4 is configured or not.
        """
        self.mode = mode
        self.address = address
        self.prefix = prefix
        self.default_gateway = default_gateway
        self.configurable = configurable
        VapiStruct.__init__(self)


    class Mode(Enum):
        """
        The ``Ipv4.Mode`` class defines different IPv4 address assignment modes.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DHCP = None
        """
        The IPv4 address is automatically assigned by a DHCP server.

        """
        STATIC = None
        """
        The IPv4 address is static.

        """
        UNCONFIGURED = None
        """
        The IPv4 protocol is not configured.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Mode` instance.
            """
            Enum.__init__(string)

    Mode._set_values({
        'DHCP': Mode('DHCP'),
        'STATIC': Mode('STATIC'),
        'UNCONFIGURED': Mode('UNCONFIGURED'),
    })
    Mode._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.ipv4.mode',
        Mode))

Ipv4._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.ipv4', {
        'mode': type.ReferenceType(__name__, 'Ipv4.Mode'),
        'address': type.StringType(),
        'prefix': type.IntegerType(),
        'default_gateway': type.OptionalType(type.StringType()),
        'configurable': type.OptionalType(type.BooleanType()),
    },
    Ipv4,
    False,
    None))



class Ipv6(VapiStruct):
    """
    The ``Ipv6`` class defines Ipv6 configuration. to perform Ipv6 network
    configuration for interfaces.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 dhcp=None,
                 autoconf=None,
                 configurable=None,
                 addresses=None,
                 default_gateway=None,
                ):
        """
        :type  dhcp: :class:`bool`
        :param dhcp: An address will be assigned by a DHCP server.
        :type  autoconf: :class:`bool`
        :param autoconf: An address will be assigned by Stateless Address Autoconfiguration
            (SLAAC).
        :type  configurable: :class:`bool`
        :param configurable: The IPv6 is configured or not.
        :type  addresses: :class:`list` of :class:`Address` or ``None``
        :param addresses: The list of addresses to be statically assigned.
            If :class:`set`, the addresses were never set.
        :type  default_gateway: :class:`str`
        :param default_gateway: The default gateway for static IP address assignment. This
            configures the global IPv6 default gateway on the appliance with
            the specified gateway address and interface. This gateway replaces
            the existing default gateway configured on the appliance. However,
            if the gateway address is link-local, then it is added for that
            interface. This does not support configuration of multiple global
            default gateways through different interfaces.
        """
        self.dhcp = dhcp
        self.autoconf = autoconf
        self.configurable = configurable
        self.addresses = addresses
        self.default_gateway = default_gateway
        VapiStruct.__init__(self)


Ipv6._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.ipv6', {
        'dhcp': type.BooleanType(),
        'autoconf': type.BooleanType(),
        'configurable': type.BooleanType(),
        'addresses': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Address'))),
        'default_gateway': type.StringType(),
    },
    Ipv6,
    False,
    None))



class Address(VapiStruct):
    """
    The ``Address`` class provides the structure used to name an IPv6 address.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 address=None,
                 origin=None,
                 prefix=None,
                 status=None,
                ):
        """
        :type  address: :class:`str` or ``None``
        :param address: The IPv6 address, for example, fc00:10:20:83:20c:29ff:fe94:bb5a.
            If :class:`set`, the address was never set.
        :type  origin: :class:`Address.Origin` or ``None``
        :param origin: The Origin of the IPv6 address. For more information, see RFC 4293.
            If :class:`set`, the origin was never set.
        :type  prefix: :class:`long` or ``None``
        :param prefix: The IPv6 CIDR prefix, for example, 64.
            If :class:`set`, the prefix was never set.
        :type  status: :class:`Address.Status` or ``None``
        :param status: The Status of the IPv6 address. For more information, see RFC 4293.
            If :class:`set`, the status was never set.
        """
        self.address = address
        self.origin = origin
        self.prefix = prefix
        self.status = status
        VapiStruct.__init__(self)


    class Origin(Enum):
        """
        The ``Address.Origin`` class defines IPv6 address origin values.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DHCP = None
        """
        The IPv6 address is assigned by a DHCP server. See RFC 4293.

        """
        RANDOM = None
        """
        The IPv6 address is assigned randomly by the system. See RFC 4293.

        """
        MANUAL = None
        """
        The IPv6 address was manually configured to a specified address, for
        example, by user configuration. See RFC 4293.

        """
        LINKLAYER = None
        """
        The IPv6 address is assigned by IPv6 Stateless Address Auto-configuration
        (SLAAC). See RFC 4293.

        """
        OTHER = None
        """
        The IPv6 address is assigned by a mechanism other than manual, DHCP, SLAAC,
        or random. See RFC 4293.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Origin` instance.
            """
            Enum.__init__(string)

    Origin._set_values({
        'DHCP': Origin('DHCP'),
        'RANDOM': Origin('RANDOM'),
        'MANUAL': Origin('MANUAL'),
        'LINKLAYER': Origin('LINKLAYER'),
        'OTHER': Origin('OTHER'),
    })
    Origin._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.address.origin',
        Origin))

    class Status(Enum):
        """
        The ``Address.Status`` class defines IPv6 address status values. See RFC
        4293.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        TENTATIVE = None
        """
        The IPv6 address is in the process of being verified as unique. An address
        in this state cannot be used for general communication. It can be used to
        determine the uniqueness of the address.

        """
        UNKNOWN = None
        """
        The status of this address cannot be determined.

        """
        INACCESSIBLE = None
        """
        The IPv6 address is inaccessible because the interface to which this
        address is assigned is not operational.

        """
        INVALID = None
        """
        The IPv6 address is not a valid address. It should not appear as the
        destination or source address of a packet.

        """
        DUPLICATE = None
        """
        The IPv6 address is not unique on the link and cannot be used.

        """
        PREFERRED = None
        """
        This is a valid IPv6 address that can appear as the destination or source
        address of a packet.

        """
        DEPRECATED = None
        """
        The is a valid but deprecated IPv6 address. This address cannot be used as
        a source address in new communications, although packets addressed to such
        an address are processed as expected.

        """
        OPTIMISTIC = None
        """
        The IPv6 address is available for use, subject to restrictions, while its
        uniqueness on a link is being verified.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Status` instance.
            """
            Enum.__init__(string)

    Status._set_values({
        'TENTATIVE': Status('TENTATIVE'),
        'UNKNOWN': Status('UNKNOWN'),
        'INACCESSIBLE': Status('INACCESSIBLE'),
        'INVALID': Status('INVALID'),
        'DUPLICATE': Status('DUPLICATE'),
        'PREFERRED': Status('PREFERRED'),
        'DEPRECATED': Status('DEPRECATED'),
        'OPTIMISTIC': Status('OPTIMISTIC'),
    })
    Status._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.address.status',
        Status))

Address._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.applmgmt.address', {
        'address': type.OptionalType(type.StringType()),
        'origin': type.OptionalType(type.ReferenceType(__name__, 'Address.Origin')),
        'prefix': type.OptionalType(type.IntegerType()),
        'status': type.OptionalType(type.ReferenceType(__name__, 'Address.Status')),
    },
    Address,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

