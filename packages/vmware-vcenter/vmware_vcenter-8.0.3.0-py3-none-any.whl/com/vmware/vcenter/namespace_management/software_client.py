# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.software.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.software_client`` module provides
classes for managing namespaces software components.

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


class Clusters(VapiInterface):
    """
    The ``Clusters`` class provides methods to upgrade the vSphere clusters.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.software.clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ClustersStub)
        self._VAPI_OPERATION_IDS = {}

    class State(Enum):
        """
        The ``Clusters.State`` class describes the state of the upgrade.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        PENDING = None
        """
        Upgrade is in progress.

        """
        READY = None
        """
        Cluster is ready when there is no upgrade or upgrade is completed.

        """
        ERROR = None
        """
        Upgrade failed and need user intervention.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`State` instance.
            """
            Enum.__init__(string)

    State._set_values({
        'PENDING': State('PENDING'),
        'READY': State('READY'),
        'ERROR': State('ERROR'),
    })
    State._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.software.clusters.state',
        State))


    class Result(VapiStruct):
        """
        The ``Clusters.Result`` class contains the result of batch upgrade method.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'res',
                {
                    'REJECTED' : [('exception', True)],
                    'STARTED' : [],
                }
            ),
        ]



        def __init__(self,
                     res=None,
                     exception=None,
                    ):
            """
            :type  res: :class:`Clusters.Result.Res`
            :param res: The result of batch upgrade method.
            :type  exception: :class:`Exception`
            :param exception: Exception when cluster pre-check failed during upgrade invocation.
                This attribute is optional and it is only relevant when the value
                of ``res`` is :attr:`Clusters.Result.Res.REJECTED`.
            """
            self.res = res
            self.exception = exception
            VapiStruct.__init__(self)


        class Res(Enum):
            """
            The ``Clusters.Result.Res`` class represents the upgrade invocation result
            for each cluster.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            STARTED = None
            """
            Upgrade is started.

            """
            REJECTED = None
            """
            Upgrade is rejected. This implies pre-check failed when invoking upgrade of
            the cluster.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Res` instance.
                """
                Enum.__init__(string)

        Res._set_values({
            'STARTED': Res('STARTED'),
            'REJECTED': Res('REJECTED'),
        })
        Res._set_binding_type(type.EnumType(
            'com.vmware.vcenter.namespace_management.software.clusters.result.res',
            Res))

    Result._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.clusters.result', {
            'res': type.ReferenceType(__name__, 'Clusters.Result.Res'),
            'exception': type.OptionalType(type.AnyErrorType()),
        },
        Result,
        False,
        None))


    class UpgradeSpec(VapiStruct):
        """
        The ``Clusters.UpgradeSpec`` class contains the specification required to
        upgrade a cluster.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     desired_version=None,
                     ignore_precheck_warnings=None,
                    ):
            """
            :type  desired_version: :class:`str`
            :param desired_version: Version number the cluster is going to be upgraded to.
            :type  ignore_precheck_warnings: :class:`bool` or ``None``
            :param ignore_precheck_warnings: If true, the upgrade workflow will ignore any pre-check warnings
                and proceed with the upgrade.
                If None, the upgrade workflow will not ignore pre-check warnings
                and fail the upgrade. It is equivalent to setting the value to
                false. The workflow adopts a conservative approach of failing the
                upgrade if None to solely let the user decide whether to force the
                upgrade despite the warnings.
            """
            self.desired_version = desired_version
            self.ignore_precheck_warnings = ignore_precheck_warnings
            VapiStruct.__init__(self)


    UpgradeSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.clusters.upgrade_spec', {
            'desired_version': type.StringType(),
            'ignore_precheck_warnings': type.OptionalType(type.BooleanType()),
        },
        UpgradeSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Clusters.Summary`` class contains basic information about the cluster
        upgrade related information.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     cluster_name=None,
                     current_version=None,
                     available_versions=None,
                     last_upgraded_date=None,
                     desired_version=None,
                     state=None,
                    ):
            """
            :type  cluster: :class:`str`
            :param cluster: Identifier for the cluster.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            :type  cluster_name: :class:`str`
            :param cluster_name: Name of the cluster.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource.name``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``ClusterComputeResource.name``.
            :type  current_version: :class:`str`
            :param current_version: Current version of the cluster.
            :type  available_versions: :class:`list` of :class:`str`
            :param available_versions: Set of versions available for upgrade.
            :type  last_upgraded_date: :class:`datetime.datetime` or ``None``
            :param last_upgraded_date: Date of last successful upgrade.
                If None, the cluster has not yet been upgraded.
            :type  desired_version: :class:`str` or ``None``
            :param desired_version: Desired version the cluster will be upgraded to.
                If None, the cluster upgrade is not in progress.
            :type  state: :class:`Clusters.State`
            :param state: Current state of the upgrade.
            """
            self.cluster = cluster
            self.cluster_name = cluster_name
            self.current_version = current_version
            self.available_versions = available_versions
            self.last_upgraded_date = last_upgraded_date
            self.desired_version = desired_version
            self.state = state
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.clusters.summary', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'cluster_name': type.IdType(resource_types='ClusterComputeResource.name'),
            'current_version': type.StringType(),
            'available_versions': type.ListType(type.StringType()),
            'last_upgraded_date': type.OptionalType(type.DateTimeType()),
            'desired_version': type.OptionalType(type.StringType()),
            'state': type.ReferenceType(__name__, 'Clusters.State'),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Clusters.Info`` class contains detailed information about the cluster
        upgrade status and related information.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     current_version=None,
                     available_versions=None,
                     last_upgraded_date=None,
                     messages=None,
                     state=None,
                     upgrade_status=None,
                     upgrade_prechecks=None,
                    ):
            """
            :type  current_version: :class:`str`
            :param current_version: Current version of the cluster.
            :type  available_versions: :class:`list` of :class:`str`
            :param available_versions: Set of available versions can be upgraded to.
            :type  last_upgraded_date: :class:`datetime.datetime` or ``None``
            :param last_upgraded_date: Date of last successful upgrade.
                If None, the cluster has not yet been upgraded.
            :type  messages: :class:`list` of :class:`Clusters.Message`
            :param messages: Current set of messages associated with the cluster version.
            :type  state: :class:`Clusters.State`
            :param state: Current state of the upgrade.
            :type  upgrade_status: :class:`Clusters.UpgradeStatus` or ``None``
            :param upgrade_status: Information about upgrade in progress.
                If None, the cluster upgrade is not in progress.
            :type  upgrade_prechecks: :class:`list` of :class:`com.vmware.vcenter.namespace_management_client.Clusters.Condition` or ``None``
            :param upgrade_prechecks: Detailed information about Supervisor upgrade pre-checks. This
                attribute was added in vSphere API 8.0.3.0.
                If None, the cluster pre-checks did not run or supervisor upgrade
                is not available.
            """
            self.current_version = current_version
            self.available_versions = available_versions
            self.last_upgraded_date = last_upgraded_date
            self.messages = messages
            self.state = state
            self.upgrade_status = upgrade_status
            self.upgrade_prechecks = upgrade_prechecks
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.clusters.info', {
            'current_version': type.StringType(),
            'available_versions': type.ListType(type.StringType()),
            'last_upgraded_date': type.OptionalType(type.DateTimeType()),
            'messages': type.ListType(type.ReferenceType(__name__, 'Clusters.Message')),
            'state': type.ReferenceType(__name__, 'Clusters.State'),
            'upgrade_status': type.OptionalType(type.ReferenceType(__name__, 'Clusters.UpgradeStatus')),
            'upgrade_prechecks': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management_client', 'Clusters.Condition'))),
        },
        Info,
        False,
        None))


    class UpgradeStatus(VapiStruct):
        """
        The ``Clusters.UpgradeStatus`` class contains detailed information about
        the cluster when upgraded is in progress.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     desired_version=None,
                     messages=None,
                     progress=None,
                     components=None,
                    ):
            """
            :type  desired_version: :class:`str` or ``None``
            :param desired_version: Desired version the cluster will be upgraded to.
                If None, the cluster upgrade is not in progress.
            :type  messages: :class:`list` of :class:`Clusters.Message`
            :param messages: Current set of messages associated with the upgrade state.
            :type  progress: :class:`Clusters.UpgradeProgress` or ``None``
            :param progress: Information about upgrade progess.
                If None, the cluster upgrade is not in progress.
            :type  components: :class:`list` of :class:`com.vmware.vcenter.namespace_management_client.Clusters.Condition` or ``None``
            :param components: Information about control plane components' upgrade status. This
                attribute was added in vSphere API 8.0.3.0.
                If None, the cluster upgrade is not in progress.
            """
            self.desired_version = desired_version
            self.messages = messages
            self.progress = progress
            self.components = components
            VapiStruct.__init__(self)


    UpgradeStatus._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.clusters.upgrade_status', {
            'desired_version': type.OptionalType(type.StringType()),
            'messages': type.ListType(type.ReferenceType(__name__, 'Clusters.Message')),
            'progress': type.OptionalType(type.ReferenceType(__name__, 'Clusters.UpgradeProgress')),
            'components': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management_client', 'Clusters.Condition'))),
        },
        UpgradeStatus,
        False,
        None))


    class UpgradeProgress(VapiStruct):
        """
        The ``Clusters.UpgradeProgress`` class contains detailed information about
        the cluster upgrade progess.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     total=None,
                     completed=None,
                     message=None,
                    ):
            """
            :type  total: :class:`long`
            :param total: Total amount of the work for the operation. The work here
                represents the number of master nodes in the cluster need to be
                upgraded.
            :type  completed: :class:`long`
            :param completed: The amount of work completed for the operation. The value can only
                be incremented. The number or master nodes which upgrade completed.
            :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param message: Message about the work progress.
            """
            self.total = total
            self.completed = completed
            self.message = message
            VapiStruct.__init__(self)


    UpgradeProgress._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.clusters.upgrade_progress', {
            'total': type.IntegerType(),
            'completed': type.IntegerType(),
            'message': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        },
        UpgradeProgress,
        False,
        None))


    class Message(VapiStruct):
        """
        The ``Clusters.Message`` class contains the information about the object
        configuration.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     severity=None,
                     details=None,
                    ):
            """
            :type  severity: :class:`Clusters.Message.Severity`
            :param severity: Type of the message.
            :type  details: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details about the message.
            """
            self.severity = severity
            self.details = details
            VapiStruct.__init__(self)


        class Severity(Enum):
            """
            The ``Clusters.Message.Severity`` class represents the severity of the
            message.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            INFO = None
            """
            Informational message. This may be accompanied by vCenter event.

            """
            WARNING = None
            """
            Warning message. This may be accompanied by vCenter event.

            """
            ERROR = None
            """
            Error message. This is accompanied by vCenter event and/or alarm.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Severity` instance.
                """
                Enum.__init__(string)

        Severity._set_values({
            'INFO': Severity('INFO'),
            'WARNING': Severity('WARNING'),
            'ERROR': Severity('ERROR'),
        })
        Severity._set_binding_type(type.EnumType(
            'com.vmware.vcenter.namespace_management.software.clusters.message.severity',
            Severity))

    Message._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.clusters.message', {
            'severity': type.ReferenceType(__name__, 'Clusters.Message.Severity'),
            'details': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        },
        Message,
        False,
        None))



    def upgrade(self,
                cluster,
                spec,
                ):
        """
        Upgrade the cluster to a specific version. This operation upgrades the
        components on control plane VMs and worker plane hosts based on the
        selected version. Before upgrading, this operation performs pre-checks
        and sets the evaluation response in Info.UpgradeStatus.messages with
        various Message.Severity levels. Depending on the severity, the upgrade
        may or may not proceed beyond prechecks. Here is a list of severities
        and corresponding behavior: - ERROR: Upgrade does not proceed beyond
        precheck operation - WARNING: Upgrade proceeds beyond precheck
        operation only if UpgradeSpec.ignorePrecheckWarnings is set to true -
        INFO: Upgrade proceeds beyond precheck operation uninterrupted

        :type  cluster: :class:`str`
        :param cluster: Identifier for the cluster which will be upgraded.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`Clusters.UpgradeSpec`
        :param spec: Specification for upgrading the cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if pre-check failed of the cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if cluster could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Upgrade privilege.
        """
        return self._invoke('upgrade',
                            {
                            'cluster': cluster,
                            'spec': spec,
                            })

    def upgrade_multiple(self,
                         specs,
                         ):
        """
        Upgrade a set of clusters to its corresponding specific version.

        :type  specs: :class:`dict` of :class:`str` and :class:`Clusters.UpgradeSpec`
        :param specs: Specifications for upgrading selected clusters.
            The key in the parameter :class:`dict` must be an identifier for
            the resource type: ``ClusterComputeResource``.
        :rtype: :class:`dict` of :class:`str` and :class:`Clusters.Result`
        :return: Pre-check result when invoking upgrade for each cluster.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``ClusterComputeResource``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Upgrade privilege on all
            specified clusters.
        """
        return self._invoke('upgrade_multiple',
                            {
                            'specs': specs,
                            })

    def get(self,
            cluster,
            ):
        """
        Returns upgrade related information of a specific cluster.

        :type  cluster: :class:`str`
        :param cluster: Identifier for the cluster which will be upgraded.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:`Clusters.Info`
        :return: Information about the upgrade of the specified WCP enabled cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if cluster could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the cluster is not WCP enabled.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            })

    def list(self):
        """
        Returns upgrade related information about all WCP enabled clusters.


        :rtype: :class:`list` of :class:`Clusters.Summary`
        :return: List of upgrade summary of all WCP enabled clusters.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('list', None)
class _ClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for upgrade operation
        upgrade_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'Clusters.UpgradeSpec'),
        })
        upgrade_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        upgrade_input_value_validator_list = [
        ]
        upgrade_output_validator_list = [
        ]
        upgrade_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/software/clusters/{cluster}',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'upgrade',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for upgrade_multiple operation
        upgrade_multiple_input_type = type.StructType('operation-input', {
            'specs': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Clusters.UpgradeSpec')),
        })
        upgrade_multiple_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        upgrade_multiple_input_value_validator_list = [
        ]
        upgrade_multiple_output_validator_list = [
        ]
        upgrade_multiple_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/software/clusters',
            request_body_parameter='specs',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'upgradeMultiple',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespace-management/software/clusters/{cluster}',
            path_variables={
                'cluster': 'cluster',
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

        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespace-management/software/clusters',
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

        operations = {
            'upgrade': {
                'input_type': upgrade_input_type,
                'output_type': type.VoidType(),
                'errors': upgrade_error_dict,
                'input_value_validator_list': upgrade_input_value_validator_list,
                'output_validator_list': upgrade_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'upgrade_multiple': {
                'input_type': upgrade_multiple_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Clusters.Result')),
                'errors': upgrade_multiple_error_dict,
                'input_value_validator_list': upgrade_multiple_input_value_validator_list,
                'output_validator_list': upgrade_multiple_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Clusters.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Clusters.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'upgrade': upgrade_rest_metadata,
            'upgrade_multiple': upgrade_multiple_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.software.clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Clusters': Clusters,
        'supervisors': 'com.vmware.vcenter.namespace_management.software.supervisors_client.StubFactory',
    }

