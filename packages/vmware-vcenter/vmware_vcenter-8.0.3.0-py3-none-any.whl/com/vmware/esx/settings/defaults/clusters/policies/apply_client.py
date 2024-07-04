# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.defaults.clusters.policies.apply.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.defaults.clusters.policies.apply_client`` module
provides classes to manage policies that affect application of desired state
configuration and software for ESXi clusters. Copyright 2019-2023 VMware, Inc.
All rights reserved. VMware Confidential Copyright 2019-2023 VMware, Inc. All
rights reserved. VMware Confidential

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


class Effective(VapiInterface):
    """
    The ``Effective`` class provides methods to manage the effective policies
    that will impact how the software and configuration specification documents
    are applied to ESXi clusters.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.defaults.clusters.policies.apply.effective'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EffectiveStub)
        self._VAPI_OPERATION_IDS = {}

    class FailureAction(VapiStruct):
        """
        The ``Effective.FailureAction`` class contains attributes that describe the
        actions to be taken when entering maintenance mode fails on a single host
        within the cluster.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'action',
                {
                    'RETRY' : [('retry_delay', True), ('retry_count', True)],
                    'FAIL' : [],
                }
            ),
        ]



        def __init__(self,
                     action=None,
                     retry_delay=None,
                     retry_count=None,
                    ):
            """
            :type  action: :class:`Effective.FailureAction.Action`
            :param action: What action (FAIL, RETRY) is to be taken if entering maintenance
                mode fails on a single host within the cluster.
            :type  retry_delay: :class:`long`
            :param retry_delay: Time to wait to retry the failed operation in seconds.
                This attribute is optional and it is only relevant when the value
                of ``action`` is :attr:`Effective.FailureAction.Action.RETRY`.
            :type  retry_count: :class:`long`
            :param retry_count: Number of times to retry the failed operation.
                This attribute is optional and it is only relevant when the value
                of ``action`` is :attr:`Effective.FailureAction.Action.RETRY`.
            """
            self.action = action
            self.retry_delay = retry_delay
            self.retry_count = retry_count
            VapiStruct.__init__(self)


        class Action(Enum):
            """
            The ``Effective.FailureAction.Action`` class defines the actions to be
            taken when entering maintenance mode fails on a single host within the
            cluster.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            FAIL = None
            """
            Fail the apply method

            """
            RETRY = None
            """
            Retry the task Apply.FailureAction#retryCount number of times on the failed
            host after Apply.FailureAction#retryDelay.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Action` instance.
                """
                Enum.__init__(string)

        Action._set_values({
            'FAIL': Action('FAIL'),
            'RETRY': Action('RETRY'),
        })
        Action._set_binding_type(type.EnumType(
            'com.vmware.esx.settings.defaults.clusters.policies.apply.effective.failure_action.action',
            Action))

    FailureAction._set_binding_type(type.StructType(
        'com.vmware.esx.settings.defaults.clusters.policies.apply.effective.failure_action', {
            'action': type.ReferenceType(__name__, 'Effective.FailureAction.Action'),
            'retry_delay': type.OptionalType(type.IntegerType()),
            'retry_count': type.OptionalType(type.IntegerType()),
        },
        FailureAction,
        False,
        None))


    class ParallelRemediationAction(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     enabled=None,
                     max_hosts=None,
                    ):
            """
            :type  enabled: :class:`bool`
            :param enabled: Enable parallel remediation for hosts in maintenance mode within a
                cluster. This attribute was added in vSphere API 8.0.0.1.
            :type  max_hosts: :class:`long` or ``None``
            :param max_hosts: Maximum number of hosts that can be remediated in parallel. Setting
                :attr:`com.vmware.esx.settings.defaults.clusters.policies_client.Apply.ParallelRemediationAction.max_hosts`
                does not guarantee maxHosts to be remediated in parallel. This
                attribute was added in vSphere API 8.0.0.1.
            """
            self.enabled = enabled
            self.max_hosts = max_hosts
            VapiStruct.__init__(self)


    ParallelRemediationAction._set_binding_type(type.StructType(
        'com.vmware.esx.settings.defaults.clusters.policies.apply.effective.parallel_remediation_action', {
            'enabled': type.BooleanType(),
            'max_hosts': type.OptionalType(type.IntegerType()),
        },
        ParallelRemediationAction,
        False,
        None))


    class EffectivePolicySpec(VapiStruct):
        """
        The ``Effective.EffectivePolicySpec`` class contains attributes that
        describe the effective policies to be used when the software and
        configuration specification documents are applied to ESXi clusters.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     failure_action=None,
                     pre_remediation_power_action=None,
                     enable_quick_boot=None,
                     disable_dpm=None,
                     disable_hac=None,
                     evacuate_offline_vms=None,
                     enforce_hcl_validation=None,
                     parallel_remediation_action=None,
                     enforce_quick_patch=None,
                     config_manager_policy_spec=None,
                    ):
            """
            :type  failure_action: :class:`Effective.FailureAction`
            :param failure_action: What action is to be taken if entering maintenance mode fails on a
                given host of the cluster.
            :type  pre_remediation_power_action: :class:`Effective.EffectivePolicySpec.PreRemediationPowerAction`
            :param pre_remediation_power_action: Specifies what should be done to the power state of the VM before
                entering maintenance mode.
            :type  enable_quick_boot: :class:`bool`
            :param enable_quick_boot: Enable Quick Boot during remediation in the cluster.
            :type  disable_dpm: :class:`bool`
            :param disable_dpm: Disable DPM on the cluster.
            :type  disable_hac: :class:`bool`
            :param disable_hac: Disable HA Admission control on the cluster.
            :type  evacuate_offline_vms: :class:`bool`
            :param evacuate_offline_vms: Evacuate powered off/suspended VMs when attempting maintenance
                mode.
            :type  enforce_hcl_validation: :class:`bool`
            :param enforce_hcl_validation: Enforce Hcl validation, when applicable, to prevent remediation if
                hardware compatibility issues are found. This attribute was added
                in vSphere API 7.0.1.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  parallel_remediation_action: :class:`Effective.ParallelRemediationAction`
            :param parallel_remediation_action: Enable parallel remediation of hosts in maintenance mode. Set max
                hosts when applicable. This attribute was added in vSphere API
                8.0.0.1.
                If None, parallel remediation will not happen.
            :type  enforce_quick_patch: :class:`bool`
            :param enforce_quick_patch: Enforce quick patch on the cluster for images that support it. This
                attribute was added in vSphere API 8.0.3.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  config_manager_policy_spec: :class:`com.vmware.esx.settings.clusters.policies_client.ConfigManagerPolicySpec`
            :param config_manager_policy_spec: Configure settings applicable to the
                com.vmware.esx.settings.clusters.Configuration.apply API. This
                attribute was added in vSphere API 8.0.3.0.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.failure_action = failure_action
            self.pre_remediation_power_action = pre_remediation_power_action
            self.enable_quick_boot = enable_quick_boot
            self.disable_dpm = disable_dpm
            self.disable_hac = disable_hac
            self.evacuate_offline_vms = evacuate_offline_vms
            self.enforce_hcl_validation = enforce_hcl_validation
            self.parallel_remediation_action = parallel_remediation_action
            self.enforce_quick_patch = enforce_quick_patch
            self.config_manager_policy_spec = config_manager_policy_spec
            VapiStruct.__init__(self)


        class PreRemediationPowerAction(Enum):
            """
            The ``Effective.EffectivePolicySpec.PreRemediationPowerAction`` class
            defines the possible actions to be taken, before entering maintenance mode.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            POWER_OFF_VMS = None
            """
            Power off VMs before entering maintenance mode.

            """
            SUSPEND_VMS = None
            """
            Suspend VMs before entering maintenance mode

            """
            DO_NOT_CHANGE_VMS_POWER_STATE = None
            """
            Do not change the VM power state

            """
            SUSPEND_VMS_TO_MEMORY = None
            """
            Suspend VMs to Memory before entering maintenance mode. This class
            attribute was added in vSphere API 7.0.2.0.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`PreRemediationPowerAction` instance.
                """
                Enum.__init__(string)

        PreRemediationPowerAction._set_values({
            'POWER_OFF_VMS': PreRemediationPowerAction('POWER_OFF_VMS'),
            'SUSPEND_VMS': PreRemediationPowerAction('SUSPEND_VMS'),
            'DO_NOT_CHANGE_VMS_POWER_STATE': PreRemediationPowerAction('DO_NOT_CHANGE_VMS_POWER_STATE'),
            'SUSPEND_VMS_TO_MEMORY': PreRemediationPowerAction('SUSPEND_VMS_TO_MEMORY'),
        })
        PreRemediationPowerAction._set_binding_type(type.EnumType(
            'com.vmware.esx.settings.defaults.clusters.policies.apply.effective.effective_policy_spec.pre_remediation_power_action',
            PreRemediationPowerAction))

    EffectivePolicySpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.defaults.clusters.policies.apply.effective.effective_policy_spec', {
            'failure_action': type.ReferenceType(__name__, 'Effective.FailureAction'),
            'pre_remediation_power_action': type.ReferenceType(__name__, 'Effective.EffectivePolicySpec.PreRemediationPowerAction'),
            'enable_quick_boot': type.BooleanType(),
            'disable_dpm': type.BooleanType(),
            'disable_hac': type.BooleanType(),
            'evacuate_offline_vms': type.BooleanType(),
            'enforce_hcl_validation': type.OptionalType(type.BooleanType()),
            'parallel_remediation_action': type.OptionalType(type.ReferenceType(__name__, 'Effective.ParallelRemediationAction')),
            'enforce_quick_patch': type.OptionalType(type.BooleanType()),
            'config_manager_policy_spec': type.OptionalType(type.ReferenceType('com.vmware.esx.settings.clusters.policies_client', 'ConfigManagerPolicySpec')),
        },
        EffectivePolicySpec,
        False,
        None))



    def get(self):
        """
        Returns the effective apply policy based on system defaults and what
        has been configured.


        :rtype: :class:`Effective.EffectivePolicySpec`
        :return: The effective policies that impact the apply method
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.lifecycleSettings.Read``.
        """
        return self._invoke('get', None)
class _EffectiveStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/defaults/clusters/policies/apply/effective',
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
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Effective.EffectivePolicySpec'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.defaults.clusters.policies.apply.effective',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Effective': Effective,
    }

