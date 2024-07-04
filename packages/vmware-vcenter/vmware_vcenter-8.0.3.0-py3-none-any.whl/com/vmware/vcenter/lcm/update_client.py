# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.lcm.update.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.lcm.update_client`` module provides classes for
updating vCenter Server to a newer version.

"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from com.vmware.cis_client import Tasks
from vmware.vapi.stdlib.client.task import Task
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


class Pending(VapiInterface):
    """
    The ``Pending`` class provides method for listing pending minor or major
    updates of vCenter Server.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.lcm.update.pending"
    """
    Resource type for pending update

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.lcm.update.pending'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PendingStub)
        self._VAPI_OPERATION_IDS = {}

    class SeverityType(Enum):
        """
        Level of severity for applying a given patch or update.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        CRITICAL = None
        """
        Vulnerabilities that can be exploited by an unauthenticated attacker from
        the Internet or those that break the guest/host Operating System isolation.

        """
        IMPORTANT = None
        """
        Vulnerabilities that are not rated critical but whose exploitation results
        in the complete compromise of confidentiality and/or integrity of user data
        and/or processing resources through user assistance or by authenticated
        attackers.

        """
        MODERATE = None
        """
        Vulnerabilities where the ability to exploit is mitigated to a significant
        degree by configuration or difficulty of exploitation, but in certain
        deployment scenarios could still lead to the compromise of confidentiality,
        integrity, or availability of user data and/or processing resources.

        """
        LOW = None
        """
        All other issues that may or maynot have a security impact. Vulnerabilities
        where exploitation is believed to be extremely difficult, or where
        successful exploitation would have minimal impact.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SeverityType` instance.
            """
            Enum.__init__(string)

    SeverityType._set_values({
        'CRITICAL': SeverityType('CRITICAL'),
        'IMPORTANT': SeverityType('IMPORTANT'),
        'MODERATE': SeverityType('MODERATE'),
        'LOW': SeverityType('LOW'),
    })
    SeverityType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.update.pending.severity_type',
        SeverityType))


    class Category(Enum):
        """
        The ``Pending.Category`` class defines the type of payload this release has
        on top of previous release

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        SECURITY = None
        """
        Fixes vulnerabilities, doesn't change functionality

        """
        FIX = None
        """
        Fixes bugs/vulnerabilities, doesn't change functionality

        """
        UPDATE = None
        """
        Changes product functionality

        """
        UPGRADE = None
        """
        Introduces new features, significantly changes product functionality

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Category` instance.
            """
            Enum.__init__(string)

    Category._set_values({
        'SECURITY': Category('SECURITY'),
        'FIX': Category('FIX'),
        'UPDATE': Category('UPDATE'),
        'UPGRADE': Category('UPGRADE'),
    })
    Category._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.update.pending.category',
        Category))


    class UpdateType(Enum):
        """
        The ``Pending.UpdateType`` class defines update type

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        PATCH = None
        """
        Fixes bugs/vulnerabilities, doesn't change functionality

        """
        UPDATE = None
        """
        Changes product functionality

        """
        UPGRADE = None
        """
        Introduces new features, significantly changes product functionality

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`UpdateType` instance.
            """
            Enum.__init__(string)

    UpdateType._set_values({
        'PATCH': UpdateType('PATCH'),
        'UPDATE': UpdateType('UPDATE'),
        'UPGRADE': UpdateType('UPGRADE'),
    })
    UpdateType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.update.pending.update_type',
        UpdateType))


    class Summary(VapiStruct):
        """
        The ``Pending.Summary`` class contains basic information about the vCenter
        patch/update/upgrade

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'execute_URL': 'execute_url',
                                }

        def __init__(self,
                     pending_update=None,
                     version=None,
                     release_date=None,
                     severity=None,
                     build=None,
                     update_type=None,
                     category=None,
                     reboot_required=None,
                     execute_url=None,
                     release_notes=None,
                    ):
            """
            :type  pending_update: :class:`str`
            :param pending_update: Identifier of the given vSphere update
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.lcm.update.pending``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.lcm.update.pending``.
            :type  version: :class:`str`
            :param version: Version of the vSphere update or patch
            :type  release_date: :class:`datetime.datetime`
            :param release_date: Release date of the vSphere update or patch
            :type  severity: :class:`Pending.SeverityType`
            :param severity: Severity of the issues fixed in the vSphere update or patch
            :type  build: :class:`str`
            :param build: Build number of the vCenter Release
            :type  update_type: :class:`Pending.UpdateType`
            :param update_type: Type of the Release based on the current vCenter version
            :type  category: :class:`Pending.Category`
            :param category: Category of the release based on features bundled on top of
                previous release
            :type  reboot_required: :class:`bool`
            :param reboot_required: Flag to suggest a reboot after the release is applied
            :type  execute_url: :class:`str`
            :param execute_url: VAMI or ISO URL for update or upgrade execute phase redirection
            :type  release_notes: :class:`list` of :class:`str`
            :param release_notes: List of URI pointing to patch or update release notes
            """
            self.pending_update = pending_update
            self.version = version
            self.release_date = release_date
            self.severity = severity
            self.build = build
            self.update_type = update_type
            self.category = category
            self.reboot_required = reboot_required
            self.execute_url = execute_url
            self.release_notes = release_notes
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.update.pending.summary', {
            'pending_update': type.IdType(resource_types='com.vmware.vcenter.lcm.update.pending'),
            'version': type.StringType(),
            'release_date': type.DateTimeType(),
            'severity': type.ReferenceType(__name__, 'Pending.SeverityType'),
            'build': type.StringType(),
            'update_type': type.ReferenceType(__name__, 'Pending.UpdateType'),
            'category': type.ReferenceType(__name__, 'Pending.Category'),
            'reboot_required': type.BooleanType(),
            'execute_URL': type.URIType(),
            'release_notes': type.ListType(type.URIType()),
        },
        Summary,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Pending.ListResult`` class contains information about the pending
        patch/updates for the given vCenter server.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     last_check_time=None,
                     update_count=None,
                     upgrade_count=None,
                     updates=None,
                     issues=None,
                    ):
            """
            :type  last_check_time: :class:`datetime.datetime`
            :param last_check_time: Time when the software depo was last checked.
            :type  update_count: :class:`long` or ``None``
            :param update_count: Number of pending updates
                Only :class:`set` if there are available updates
            :type  upgrade_count: :class:`long` or ``None``
            :param upgrade_count: Number of pending upgrades
                Only :class:`set` if there are available upgrades
            :type  updates: :class:`list` of :class:`Pending.Summary`
            :param updates: List of pending update details
            :type  issues: :class:`com.vmware.vcenter.lcm_client.Notifications` or ``None``
            :param issues: Lists of issues encountered during pending updates retrieval.
                :class:`set` if any issues encountered.
            """
            self.last_check_time = last_check_time
            self.update_count = update_count
            self.upgrade_count = upgrade_count
            self.updates = updates
            self.issues = issues
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.update.pending.list_result', {
            'last_check_time': type.DateTimeType(),
            'update_count': type.OptionalType(type.IntegerType()),
            'upgrade_count': type.OptionalType(type.IntegerType()),
            'updates': type.ListType(type.ReferenceType(__name__, 'Pending.Summary')),
            'issues': type.OptionalType(type.ReferenceType('com.vmware.vcenter.lcm_client', 'Notifications')),
        },
        ListResult,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Pending.Info`` class contains detailed information about the vCenter
        patch/update.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'execute_URL': 'execute_url',
                                }

        def __init__(self,
                     description=None,
                     pending_update=None,
                     version=None,
                     release_date=None,
                     severity=None,
                     build=None,
                     update_type=None,
                     category=None,
                     reboot_required=None,
                     execute_url=None,
                     release_notes=None,
                    ):
            """
            :type  description: :class:`str`
            :param description: Description of the vSphere update
            :type  pending_update: :class:`str`
            :param pending_update: Identifier of the given vSphere update
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.lcm.update.pending``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.lcm.update.pending``.
            :type  version: :class:`str`
            :param version: Version of the vSphere update or patch
            :type  release_date: :class:`datetime.datetime`
            :param release_date: Release date of the vSphere update or patch
            :type  severity: :class:`Pending.SeverityType`
            :param severity: Severity of the issues fixed in the vSphere update or patch
            :type  build: :class:`str`
            :param build: Build number of the vCenter Release
            :type  update_type: :class:`Pending.UpdateType`
            :param update_type: Type of the Release based on the current vCenter version
            :type  category: :class:`Pending.Category`
            :param category: Category of the release based on features bundled on top of
                previous release
            :type  reboot_required: :class:`bool`
            :param reboot_required: Flag to suggest a reboot after the release is applied
            :type  execute_url: :class:`str`
            :param execute_url: VAMI or ISO URL for update or upgrade execute phase redirection
            :type  release_notes: :class:`list` of :class:`str`
            :param release_notes: List of URI pointing to patch or update release notes
            """
            self.description = description
            self.pending_update = pending_update
            self.version = version
            self.release_date = release_date
            self.severity = severity
            self.build = build
            self.update_type = update_type
            self.category = category
            self.reboot_required = reboot_required
            self.execute_url = execute_url
            self.release_notes = release_notes
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.update.pending.info', {
            'description': type.StringType(),
            'pending_update': type.IdType(resource_types='com.vmware.vcenter.lcm.update.pending'),
            'version': type.StringType(),
            'release_date': type.DateTimeType(),
            'severity': type.ReferenceType(__name__, 'Pending.SeverityType'),
            'build': type.StringType(),
            'update_type': type.ReferenceType(__name__, 'Pending.UpdateType'),
            'category': type.ReferenceType(__name__, 'Pending.Category'),
            'reboot_required': type.BooleanType(),
            'execute_URL': type.URIType(),
            'release_notes': type.ListType(type.URIType()),
        },
        Info,
        False,
        None))



    def list(self):
        """
        Lists all available minor and major updates.


        :rtype: :class:`Pending.ListResult`
        :return: Information about the pending patch/updates for the given vCenter
            server
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is some unknown internal error. The accompanying error
            message will give more details about the error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('list', None)

    def get(self,
            version,
            ):
        """
        Gets detailed update information.

        :type  version: :class:`str`
        :param version: A version identified the update
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.lcm.update.pending``.
        :rtype: :class:`Pending.Info`
        :return: A detailed information about the particular vCenter patch/update
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no pending update assosiated with the ``version`` in
            the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is some unknown internal error. The accompanying error
            message will give more details about the error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('get',
                            {
                            'version': version,
                            })
class PrecheckReport(VapiInterface):
    """
    The ``PrecheckReport`` class generates precheck report for a vCenter Server
    instance against a target update version.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.lcm.report"
    """
    Resource type for precheck report

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.lcm.update.precheck_report'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PrecheckReportStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})

    class ReportSummary(VapiStruct):
        """
        The ``Summary`` Class contains the summary of precheck report.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     error_count=None,
                     warning_count=None,
                    ):
            """
            :type  error_count: :class:`long`
            :param error_count: Number of errors detected by precheck process
            :type  warning_count: :class:`long`
            :param warning_count: Number of warnings detected by precheck process
            """
            self.error_count = error_count
            self.warning_count = warning_count
            VapiStruct.__init__(self)


    ReportSummary._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.update.precheck_report.report_summary', {
            'error_count': type.IntegerType(),
            'warning_count': type.IntegerType(),
        },
        ReportSummary,
        False,
        None))


    class Report(VapiStruct):
        """
        The ``PrecheckReport.Report`` class contains estimates of how long it will
        take an update as well as a list of possible warnings and errors with
        applying the update.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     date_created=None,
                     estimated_time_to_update=None,
                     issues=None,
                     summary=None,
                    ):
            """
            :type  date_created: :class:`datetime.datetime`
            :param date_created: Time when this precheck report was generated
            :type  estimated_time_to_update: :class:`long` or ``None``
            :param estimated_time_to_update: Rough estimate of time to update vCenter Server in minutes.
                This attribute will be None if the precheck failed.
            :type  issues: :class:`com.vmware.vcenter.lcm_client.Notifications` or ``None``
            :param issues: Lists of the issues and warnings
                This attribute will be None if the precehck is successful.
            :type  summary: :class:`PrecheckReport.ReportSummary`
            :param summary: A summary of the report consist of count of warnings and errors
                returned by running the precheck.
            """
            self.date_created = date_created
            self.estimated_time_to_update = estimated_time_to_update
            self.issues = issues
            self.summary = summary
            VapiStruct.__init__(self)


    Report._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.update.precheck_report.report', {
            'date_created': type.DateTimeType(),
            'estimated_time_to_update': type.OptionalType(type.IntegerType()),
            'issues': type.OptionalType(type.ReferenceType('com.vmware.vcenter.lcm_client', 'Notifications')),
            'summary': type.ReferenceType(__name__, 'PrecheckReport.ReportSummary'),
        },
        Report,
        False,
        None))


    class Result(VapiStruct):
        """
        The ``PrecheckReport.Result`` class contains the precheck report and a link
        to download the CSV report.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     report=None,
                     csv_report=None,
                    ):
            """
            :type  report: :class:`PrecheckReport.Report`
            :param report: The report generated by running the precheck.
            :type  csv_report: :class:`str` or ``None``
            :param csv_report: The identifier of CSV formatted precheck report.
                com.vmware.vcenter.lcm.report#get provides location where the CSV
                report can be downloaded from based on the ``csvReport``.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.lcm.report``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vcenter.lcm.report``.
                None in case of ``errors`` reported in
                :attr:`PrecheckReport.Report.issues`.
            """
            self.report = report
            self.csv_report = csv_report
            VapiStruct.__init__(self)


    Result._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.update.precheck_report.result', {
            'report': type.ReferenceType(__name__, 'PrecheckReport.Report'),
            'csv_report': type.OptionalType(type.IdType()),
        },
        Result,
        False,
        None))




    def create_task(self,
               version,
               ):
        """
        Creates a vCenter Server pre-update compatibility check report for the
        pending update version. The report can be exported and downloaded in
        CSV format. 
        
        The result of this operation can be queried by calling the
        com.vmware.cis.Tasks#get method where ``task`` is the response of this
        operation.

        :type  version: :class:`str`
        :param version: Pending update version for which pre-update compatibility check
            will be executed.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.lcm.update.pending``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no pending update assosiated with the ``version`` in
            the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if a precheck is already in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is some unknown internal error. The accompanying error
            message will give more details about the error.
        """
        task_id = self._invoke('create$task',
                                {
                                'version': version,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'PrecheckReport.Result'))
        return task_instance
class _PendingStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/lcm/update/pending',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'version': type.IdType(resource_types='com.vmware.vcenter.lcm.update.pending'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/lcm/update/pending/{version}',
            path_variables={
                'version': 'version',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Pending.ListResult'),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Pending.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.lcm.update.pending',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _PrecheckReportStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'version': type.IdType(resource_types='com.vmware.vcenter.lcm.update.pending'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/lcm/update/pending/{version}/precheck-report',
            path_variables={
                'version': 'version',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.lcm.update.precheck_report',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Pending': Pending,
        'PrecheckReport': PrecheckReport,
    }

