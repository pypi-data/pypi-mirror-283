# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.
#---------------------------------------------------------------------------

"""
The
``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha_client``
module provides classes to manage the vCenter Server Inventory Cluster HA
settings.

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


class AdmissionControl(VapiStruct):
    """
    The ``FailuresAndResponses`` class contains attributes describing the
    Failures and responses specific configurations of a cluster. It contains
    cluster-wide configurations for vsphere HA.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 host_failures_cluster_tolerates=None,
                 policy_type=None,
                 host_fail_over_slot_policy=None,
                 cluster_resource_percentage=None,
                 dedicated_failover_hosts=None,
                 performance_degradation_vm_tolerate=None,
                ):
        """
        :type  host_failures_cluster_tolerates: :class:`long` or ``None``
        :param host_failures_cluster_tolerates: Number of host failures that should be tolerated, still
            guaranteeing sufficient resources to restart virtual machines on
            available hosts. If not set, we assume 1.
        :type  policy_type: :class:`str` or ``None``
        :param policy_type: 
        :type  host_fail_over_slot_policy: :class:`FixedSizeSlotPolicy` or ``None``
        :param host_fail_over_slot_policy: This policy allows setting a fixed slot size
        :type  cluster_resource_percentage: :class:`ClusterResourcePercentage` or ``None``
        :param cluster_resource_percentage: 
        :type  dedicated_failover_hosts: :class:`list` of :class:`str` or ``None``
        :param dedicated_failover_hosts: List of hosts dedicated for failover.
        :type  performance_degradation_vm_tolerate: :class:`long` or ``None``
        :param performance_degradation_vm_tolerate: Percentage of resource reduction that a cluster of VMs can tolerate
            in case of a failover.
        """
        self.host_failures_cluster_tolerates = host_failures_cluster_tolerates
        self.policy_type = policy_type
        self.host_fail_over_slot_policy = host_fail_over_slot_policy
        self.cluster_resource_percentage = cluster_resource_percentage
        self.dedicated_failover_hosts = dedicated_failover_hosts
        self.performance_degradation_vm_tolerate = performance_degradation_vm_tolerate
        VapiStruct.__init__(self)


AdmissionControl._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.admission_control', {
        'host_failures_cluster_tolerates': type.OptionalType(type.IntegerType()),
        'policy_type': type.OptionalType(type.StringType()),
        'host_fail_over_slot_policy': type.OptionalType(type.ReferenceType(__name__, 'FixedSizeSlotPolicy')),
        'cluster_resource_percentage': type.OptionalType(type.ReferenceType(__name__, 'ClusterResourcePercentage')),
        'dedicated_failover_hosts': type.OptionalType(type.ListType(type.StringType())),
        'performance_degradation_vm_tolerate': type.OptionalType(type.IntegerType()),
    },
    AdmissionControl,
    False,
    None))



class ClusterResourcePercentage(VapiStruct):
    """
    This class defines CPU, Memory resource percentages.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 cpu=None,
                 memory=None,
                ):
        """
        :type  cpu: :class:`long`
        :param cpu: Reserved failover CPU capacity
        :type  memory: :class:`long`
        :param memory: Reserved failover Memory capacity
        """
        self.cpu = cpu
        self.memory = memory
        VapiStruct.__init__(self)


ClusterResourcePercentage._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.cluster_resource_percentage', {
        'cpu': type.IntegerType(),
        'memory': type.IntegerType(),
    },
    ClusterResourcePercentage,
    False,
    None))



class FailuresAndResponses(VapiStruct):
    """
    The ``FailuresAndResponses`` class contains attributes describing the
    Failures and responses specific configurations of a cluster. It contains
    cluster-wide configurations for vsphere HA.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 host_monitoring=None,
                 default_vm_restart_priority=None,
                 restart_priority_condition_timeout=None,
                 additional_delay=None,
                 host_isolation_response=None,
                 datastore_with_pdl_failure_response=None,
                 apd_failure_response=None,
                 response_recovery=None,
                 response_delay=None,
                 vm_monitoring=None,
                 vm_tools_monitoring_settings=None,
                ):
        """
        :type  host_monitoring: :class:`FailuresAndResponses.ServiceState` or ``None``
        :param host_monitoring: 
        :type  default_vm_restart_priority: :class:`FailuresAndResponses.RestartPriority` or ``None``
        :param default_vm_restart_priority: Restart priority for a virtual machine. 
            
            If not specified at either the cluster level or the virtual machine
            level, this will default to ``medium``. 
            If None or empty, the value is skipped.
        :type  restart_priority_condition_timeout: :class:`long` or ``None``
        :param restart_priority_condition_timeout: This setting is used to specify a maximum time the lower priority
            VMs should wait for the higher priority VMs to be ready. If the
            higher priority Vms are not ready by this time, then the lower
            priority VMs are restarted irrespective of the VM ready state. This
            timeout can be used to prevent the failover of lower priority VMs
            to be stuck infinitely. Timeout specified in seconds. To use
            cluster setting for a VM override, set to -1 in per-VM. setting. 
            If None or empty, the value is skipped.
        :type  additional_delay: :class:`long` or ``None``
        :param additional_delay: After condition has been met, a mandatory delay before starting the
            next VM restart priority.
        :type  host_isolation_response: :class:`FailuresAndResponses.IsolationResponse` or ``None``
        :param host_isolation_response: Indicates whether or not the virtual machine should be powered off
            if a host determines that it is isolated from the rest of the
            compute resource. 
            
            If not specified at either the cluster level or the virtual machine
            level, this will default to ``powerOff``. 
            If None or empty, the value is skipped.
        :type  datastore_with_pdl_failure_response: :class:`FailuresAndResponses.StorageVmReaction`
        :param datastore_with_pdl_failure_response: VM storage protection setting for storage failures categorized as
            Permenant Device Loss (PDL). PDL indicates storage device failure
            or LUN removal. In case of PDL, the failed datastore or device is
            unlikely to recover. The details of PDL are
        :type  apd_failure_response: :class:`FailuresAndResponses.StorageVmReaction`
        :param apd_failure_response: VM storage protection setting for storage failures categorized as
            All Paths Down (APD). APD is a condition where a storage has become
            inaccessible for unknown reasons. It only indicates loss of
            connectivity and does not indicate storage device failure or LUN
            removal (Permanent Device Loss or PDL)
        :type  response_recovery: :class:`FailuresAndResponses.VmReactionOnAPDCleared` or ``None``
        :param response_recovery: Action taken by VM Component Protection service for a powered on VM
            when APD condition clears after APD timeout. 
            
            This property is meaningful only when vSphere HA is turned on.
            Valid values are specified by
            :class:`FailuresAndResponses.VmReactionOnAPDCleared`. The default
            value is VmReactionOnAPDCleared#none for cluster setting and
            VmReactionOnAPDCleared#useClusterDefault for per-VM setting.
        :type  response_delay: :class:`long` or ``None``
        :param response_delay: The time interval after an APD timeout has been declared and before
            VM Component Protection service will terminate the VM. The default
            value is 180 seconds if not specified. To use cluster setting for a
            VM override, set to -1 in per-VM setting.
        :type  vm_monitoring: :class:`FailuresAndResponses.VmMonitoringState` or ``None``
        :param vm_monitoring: 
        :type  vm_tools_monitoring_settings: :class:`VmToolsMonitoringSettings` or ``None``
        :param vm_tools_monitoring_settings: 
        """
        self.host_monitoring = host_monitoring
        self.default_vm_restart_priority = default_vm_restart_priority
        self.restart_priority_condition_timeout = restart_priority_condition_timeout
        self.additional_delay = additional_delay
        self.host_isolation_response = host_isolation_response
        self.datastore_with_pdl_failure_response = datastore_with_pdl_failure_response
        self.apd_failure_response = apd_failure_response
        self.response_recovery = response_recovery
        self.response_delay = response_delay
        self.vm_monitoring = vm_monitoring
        self.vm_tools_monitoring_settings = vm_tools_monitoring_settings
        VapiStruct.__init__(self)


    class ServiceState(Enum):
        """
        Possible states of an HA service. All services support the disabled and
        enabled states.

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
        HA service is disabled.

        """
        ENABLED = None
        """
        HA service is enabled.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ServiceState` instance.
            """
            Enum.__init__(string)

    ServiceState._set_values({
        'DISABLED': ServiceState('DISABLED'),
        'ENABLED': ServiceState('ENABLED'),
    })
    ServiceState._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.failures_and_responses.service_state',
        ServiceState))

    class RestartPriority(Enum):
        """
        The enum defines virtual machine restart priority values to resolve
        resource contention. The priority determines the preference that HA gives
        to a virtual machine if sufficient capacity is not available to power on
        all failed virtual machines. For example, high priority virtual machines on
        a host get preference over low priority virtual machines.

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
        vSphere HA is disabled for this virtual machine.

        """
        LOWEST = None
        """
        Virtual machines with this priority have the lowest chance of powering on
        after a failure if there is insufficient capacity on hosts to meet all
        virtual machine needs.

        """
        LOW = None
        """
        Virtual machines with this priority have a lower chance of powering on
        after a failure if there is insufficient capacity on hosts to meet all
        virtual machine needs.

        """
        MEDIUM = None
        """
        Virtual machines with this priority have an intermediate chance of powering
        on after a failure if there is insufficient capacity on hosts to meet all
        virtual machine needs.

        """
        HIGH = None
        """
        Virtual machines with this priority have a higher chance of powering on
        after a failure if there is insufficient capacity on hosts to meet all
        virtual machine needs.

        """
        HIGHEST = None
        """
        Virtual machines with this priority have the highest chance of powering on
        after a failure if there is insufficient capacity on hosts to meet all
        virtual machine needs.

        """
        CLUSTER_RESTART_PRIORITY = None
        """
        Virtual machines with this priority use the default restart priority
        defined for the cluster that contains this virtual machine.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`RestartPriority` instance.
            """
            Enum.__init__(string)

    RestartPriority._set_values({
        'DISABLED': RestartPriority('DISABLED'),
        'LOWEST': RestartPriority('LOWEST'),
        'LOW': RestartPriority('LOW'),
        'MEDIUM': RestartPriority('MEDIUM'),
        'HIGH': RestartPriority('HIGH'),
        'HIGHEST': RestartPriority('HIGHEST'),
        'CLUSTER_RESTART_PRIORITY': RestartPriority('CLUSTER_RESTART_PRIORITY'),
    })
    RestartPriority._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.failures_and_responses.restart_priority',
        RestartPriority))

    class IsolationResponse(Enum):
        """
        The enum defines values that indicate whether or not the virtual machine
        should be powered off if a host determines that it is isolated from the
        rest of the cluster.

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
        Do not power off the virtual machine in the event of a host network
        isolation.

        """
        POWER_OFF = None
        """
        Power off the virtual machine in the event of a host network isolation.

        """
        SHUTDOWN = None
        """
        Shut down the virtual machine guest operating system in the event of a host
        network isolation. If the guest operating system fails to shutdown within
        five minutes, HA will initiate a forced power off. 
        
        When you use the shutdown isolation response, failover can take longer
        (compared to the response) because the virtual machine cannot fail over
        until it is shutdown.

        """
        CLUSTER_ISOLATION_RESPONSE = None
        """
        Use the default isolation response defined for the cluster that contains
        this virtual machine.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`IsolationResponse` instance.
            """
            Enum.__init__(string)

    IsolationResponse._set_values({
        'NONE': IsolationResponse('NONE'),
        'POWER_OFF': IsolationResponse('POWER_OFF'),
        'SHUTDOWN': IsolationResponse('SHUTDOWN'),
        'CLUSTER_ISOLATION_RESPONSE': IsolationResponse('CLUSTER_ISOLATION_RESPONSE'),
    })
    IsolationResponse._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.failures_and_responses.isolation_response',
        IsolationResponse))

    class StorageVmReaction(Enum):
        """
        The VM policy settings that determine the response to storage failures.

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
        VM Component Protection service will not monitor or react to the component
        failure. This setting does not affect other vSphere HA services such as
        Host Monitoring or VM Health Monitoring.

        """
        WARNING = None
        """
        VM Component Protection service will monitor component failures but will
        not restart an affected VM. Rather it will notify users about the component
        failures. This setting does not affect other vSphere HA services such as
        Host Monitoring or VM Health Monitoring.

        """
        RESTART_CONSERVATIVE = None
        """
        VM Component Protection service protects VMs conservatively. With this
        setting, when the service can't determine that capacity is available to
        restart a VM, it will favor keeping the VM running.

        """
        RESTART_AGGRESSIVE = None
        """
        VM Component Protection service protects VMs aggressively. With this
        setting, the service will terminate an affected VM even if it can't
        determine that capacity exists to restart the VM.

        """
        CLUSTER_DEFAULT = None
        """
        VM will use the cluster default setting. This option is only meaningful for
        per-VM settings.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`StorageVmReaction` instance.
            """
            Enum.__init__(string)

    StorageVmReaction._set_values({
        'DISABLED': StorageVmReaction('DISABLED'),
        'WARNING': StorageVmReaction('WARNING'),
        'RESTART_CONSERVATIVE': StorageVmReaction('RESTART_CONSERVATIVE'),
        'RESTART_AGGRESSIVE': StorageVmReaction('RESTART_AGGRESSIVE'),
        'CLUSTER_DEFAULT': StorageVmReaction('CLUSTER_DEFAULT'),
    })
    StorageVmReaction._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.failures_and_responses.storage_vm_reaction',
        StorageVmReaction))

    class VmReactionOnAPDCleared(Enum):
        """
        If an APD condition clears after an APD timeout condition has been declared
        and before VM Component Protection service terminated the VM, the guestOS
        and application may no longer be operational.

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
        VM Component Protection service will not react after APD condition is
        cleared.

        """
        RESET = None
        """
        VM Component Protection service will reset the VM after APD condition is
        cleared. Note this only applies if the subject VM is still powered on.

        """
        USE_CLUSTER_DEFAULT = None
        """
        VM will use the cluster default setting. This option is only meaningful for
        per-VM settings.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`VmReactionOnAPDCleared` instance.
            """
            Enum.__init__(string)

    VmReactionOnAPDCleared._set_values({
        'NONE': VmReactionOnAPDCleared('NONE'),
        'RESET': VmReactionOnAPDCleared('RESET'),
        'USE_CLUSTER_DEFAULT': VmReactionOnAPDCleared('USE_CLUSTER_DEFAULT'),
    })
    VmReactionOnAPDCleared._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.failures_and_responses.vm_reaction_on_APD_cleared',
        VmReactionOnAPDCleared))

    class VmMonitoringState(Enum):
        """
        The enum defines values that indicate the state of Virtual Machine Health
        Monitoring. Health Monitoring uses the vmTools (guest) and application
        agent heartbeat modules. You can configure HA to respond to heartbeat
        failures of either one or both modules. You can also disable the HA
        response to heartbeat failures.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        VM_MONITORING_DISABLED = None
        """
        Virtual machine health monitoring is disabled. In this state, HA response
        to guest and application heartbeat failures are disabled.

        """
        VM_MONITORING_ONLY = None
        """
        HA response to guest heartbeat failure is enabled.

        """
        VM_AND_APP_MONITORING = None
        """
        HA response to both guest and application heartbeat failure is enabled.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`VmMonitoringState` instance.
            """
            Enum.__init__(string)

    VmMonitoringState._set_values({
        'VM_MONITORING_DISABLED': VmMonitoringState('VM_MONITORING_DISABLED'),
        'VM_MONITORING_ONLY': VmMonitoringState('VM_MONITORING_ONLY'),
        'VM_AND_APP_MONITORING': VmMonitoringState('VM_AND_APP_MONITORING'),
    })
    VmMonitoringState._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.failures_and_responses.vm_monitoring_state',
        VmMonitoringState))

FailuresAndResponses._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.failures_and_responses', {
        'host_monitoring': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.ServiceState')),
        'default_vm_restart_priority': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.RestartPriority')),
        'restart_priority_condition_timeout': type.OptionalType(type.IntegerType()),
        'additional_delay': type.OptionalType(type.IntegerType()),
        'host_isolation_response': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.IsolationResponse')),
        'datastore_with_pdl_failure_response': type.ReferenceType(__name__, 'FailuresAndResponses.StorageVmReaction'),
        'apd_failure_response': type.ReferenceType(__name__, 'FailuresAndResponses.StorageVmReaction'),
        'response_recovery': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.VmReactionOnAPDCleared')),
        'response_delay': type.OptionalType(type.IntegerType()),
        'vm_monitoring': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.VmMonitoringState')),
        'vm_tools_monitoring_settings': type.OptionalType(type.ReferenceType(__name__, 'VmToolsMonitoringSettings')),
    },
    FailuresAndResponses,
    False,
    None))



class FixedSizeSlotPolicy(VapiStruct):
    """
    This policy allows setting a fixed slot size

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 cpu=None,
                 memory=None,
                ):
        """
        :type  cpu: :class:`long`
        :param cpu: The cpu component of the slot size (in MHz)
        :type  memory: :class:`long`
        :param memory: The memory component of the slot size (in megabytes)
        """
        self.cpu = cpu
        self.memory = memory
        VapiStruct.__init__(self)


FixedSizeSlotPolicy._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.fixed_size_slot_policy', {
        'cpu': type.IntegerType(),
        'memory': type.IntegerType(),
    },
    FixedSizeSlotPolicy,
    False,
    None))



class HaVmOverrides(VapiStruct):
    """
    The VmOverrides data object contains the HA configuration settings for vm
    as a override from cluster. All fields are optional.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 vm_restart_priority=None,
                 vm_additional_delay=None,
                 vm_restart_priority_timeout=None,
                 vm_isolation_response=None,
                 vm_datastore_with_pdl_failure_response=None,
                 vm_apd_failure_response=None,
                 vm_apd_failover_delay=None,
                 vm_apd_response_recovery=None,
                 vm_monitoring=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Reference to the virtual machine.
        :type  vm_restart_priority: :class:`FailuresAndResponses.RestartPriority` or ``None``
        :param vm_restart_priority: Restart priority for a virtual machine.
            If None or empty, the value is skipped.
        :type  vm_additional_delay: :class:`long` or ``None``
        :param vm_additional_delay: After condition has been met, a mandatory delay before starting the
            next VM restart priority.
        :type  vm_restart_priority_timeout: :class:`long` or ``None``
        :param vm_restart_priority_timeout: This setting is used to specify a maximum time the lower priority
            VMs should wait for the higher priority VMs to be ready. If the
            higher priority Vms are not ready by this time, then the lower
            priority VMs are restarted irrespective of the VM ready state. This
            timeout can be used to prevent the failover of lower priority VMs
            to be stuck infinitely.
            If None or empty, the value is skipped.
        :type  vm_isolation_response: :class:`FailuresAndResponses.IsolationResponse` or ``None``
        :param vm_isolation_response: Indicates whether or not the virtual machine should be powered off
            if a host determines that it is isolated from the rest of the
            compute resource. 
            
            If not specified at either the cluster level or the virtual machine
            level, this will default to ``powerOff``. 
            If None or empty, the value is skipped.
        :type  vm_datastore_with_pdl_failure_response: :class:`FailuresAndResponses.StorageVmReaction`
        :param vm_datastore_with_pdl_failure_response: VM storage protection setting for storage failures categorized as
            Permenant Device Loss (PDL). PDL indicates storage device failure
            or LUN removal. In case of PDL, the failed datastore or device is
            unlikely to recover. The details of PDL are
        :type  vm_apd_failure_response: :class:`FailuresAndResponses.StorageVmReaction`
        :param vm_apd_failure_response: VM storage protection setting for storage failures categorized as
            All Paths Down (APD). APD is a condition where a storage has become
            inaccessible for unknown reasons. It only indicates loss of
            connectivity and does not indicate storage device failure or LUN
            removal (Permanent Device Loss or PDL)
        :type  vm_apd_failover_delay: :class:`long` or ``None``
        :param vm_apd_failover_delay: The time interval after an APD timeout has been declared and before
            VM Component Protection service will terminate the VM. The default
            value is 180 seconds if not specified. To use cluster setting for a
            VM override, set to -1 in per-VM setting.
        :type  vm_apd_response_recovery: :class:`FailuresAndResponses.VmReactionOnAPDCleared` or ``None``
        :param vm_apd_response_recovery: Action taken by VM Component Protection service for a powered on VM
            when APD condition clears after APD timeout. This property is
            meaningful only when vSphere HA is turned on. Valid values are
        :type  vm_monitoring: :class:`FailuresAndResponses.VmMonitoringState` or ``None``
        :param vm_monitoring: Virtual machine health monitoring is disabled. In this state, HA
            response to guest and application heartbeat failures are disabled.
        """
        self.name = name
        self.vm_restart_priority = vm_restart_priority
        self.vm_additional_delay = vm_additional_delay
        self.vm_restart_priority_timeout = vm_restart_priority_timeout
        self.vm_isolation_response = vm_isolation_response
        self.vm_datastore_with_pdl_failure_response = vm_datastore_with_pdl_failure_response
        self.vm_apd_failure_response = vm_apd_failure_response
        self.vm_apd_failover_delay = vm_apd_failover_delay
        self.vm_apd_response_recovery = vm_apd_response_recovery
        self.vm_monitoring = vm_monitoring
        VapiStruct.__init__(self)


HaVmOverrides._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.ha_vm_overrides', {
        'name': type.StringType(),
        'vm_restart_priority': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.RestartPriority')),
        'vm_additional_delay': type.OptionalType(type.IntegerType()),
        'vm_restart_priority_timeout': type.OptionalType(type.IntegerType()),
        'vm_isolation_response': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.IsolationResponse')),
        'vm_datastore_with_pdl_failure_response': type.ReferenceType(__name__, 'FailuresAndResponses.StorageVmReaction'),
        'vm_apd_failure_response': type.ReferenceType(__name__, 'FailuresAndResponses.StorageVmReaction'),
        'vm_apd_failover_delay': type.OptionalType(type.IntegerType()),
        'vm_apd_response_recovery': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.VmReactionOnAPDCleared')),
        'vm_monitoring': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses.VmMonitoringState')),
    },
    HaVmOverrides,
    False,
    None))



class HeartBeatDataStores(VapiStruct):
    """
    The ``HeartBeatDataStores`` class contains attributes describing the
    HeartBeatDataStores It contains cluster-wide configurations for vsphere HA.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 heartbeat_datastore_policy=None,
                 datastores=None,
                ):
        """
        :type  heartbeat_datastore_policy: :class:`HeartBeatDataStores.HBDatastoreCandidate`
        :param heartbeat_datastore_policy: 
        :type  datastores: :class:`list` of :class:`str` or ``None``
        :param datastores: 
        """
        self.heartbeat_datastore_policy = heartbeat_datastore_policy
        self.datastores = datastores
        VapiStruct.__init__(self)


    class HBDatastoreCandidate(Enum):
        """
        The policy to determine the candidates from which vCenter Server can choose
        heartbeat datastores.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        USER_SELECTED_DS = None
        """
        vCenter Server chooses heartbeat datastores from the set specified by the
        user (see #heartbeatDatastore). More specifically, datastores not included
        in the set will not be chosen. Note that if #heartbeatDatastore is empty,
        datastore heartbeating will be disabled for HA.

        """
        ALL_FEASIBLE_DS = None
        """
        vCenter Server chooses heartbeat datastores from all the feasible ones,
        i.e., the datastores that are accessible to more than one host in the
        cluster. The choice will be made without giving preference to those
        specified by the user (see #heartbeatDatastore).

        """
        ALL_FEASIBLE_DS_WITH_USER_PREFERENCE = None
        """
        vCenter Server chooses heartbeat datastores from all the feasible ones
        while giving preference to those specified by the user (see
        #heartbeatDatastore). More specifically, the datastores not included in
        #heartbeatDatastore will be chosen if and only if the specified ones are
        not sufficient.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`HBDatastoreCandidate` instance.
            """
            Enum.__init__(string)

    HBDatastoreCandidate._set_values({
        'USER_SELECTED_DS': HBDatastoreCandidate('USER_SELECTED_DS'),
        'ALL_FEASIBLE_DS': HBDatastoreCandidate('ALL_FEASIBLE_DS'),
        'ALL_FEASIBLE_DS_WITH_USER_PREFERENCE': HBDatastoreCandidate('ALL_FEASIBLE_DS_WITH_USER_PREFERENCE'),
    })
    HBDatastoreCandidate._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.heart_beat_data_stores.HB_datastore_candidate',
        HBDatastoreCandidate))

HeartBeatDataStores._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.heart_beat_data_stores', {
        'heartbeat_datastore_policy': type.ReferenceType(__name__, 'HeartBeatDataStores.HBDatastoreCandidate'),
        'datastores': type.OptionalType(type.ListType(type.StringType())),
    },
    HeartBeatDataStores,
    False,
    None))



class VmToolsMonitoringSettings(VapiStruct):
    """
    The vim.cluster.VmToolsMonitoringSettings data object contains virtual
    machine monitoring settings that are used by the Virtual Machine Health
    Monitoring Service. The Service checks the VMware Tools heartbeat of a
    virtual machine. If heartbeats have not been received within a specified
    time interval, the Service declares the virtual machine as failed and
    resets the virtual machine. All fields are optional. In case of a
    reconfiguration, fields left unset are not changed.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                 cluster_settings=None,
                 failure_interval=None,
                 min_up_time=None,
                 max_failures=None,
                 max_failure_window=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Flag indicating whether or not the Virtual Machine Health
            Monitoring service is enabled. 
            
            The Server does not use this property.
        :type  cluster_settings: :class:`bool` or ``None``
        :param cluster_settings: Flag indicating whether to use the cluster settings or the per VM
            settings. 
            
            The default value is true.
        :type  failure_interval: :class:`long` or ``None``
        :param failure_interval: If no heartbeat has been received for at least the specified number
            of seconds, the virtual machine is declared as failed. 
            
            The default value is 30.
        :type  min_up_time: :class:`long` or ``None``
        :param min_up_time: The number of seconds for the virtual machine's heartbeats to
            stabilize after the virtual machine has been powered on. This time
            should include the guest operating system boot-up time. The virtual
            machine monitoring will begin only after this period. 
            
            The default value is 120.
        :type  max_failures: :class:`long` or ``None``
        :param max_failures: Maximum number of failures and automated resets allowed during the
            time that :attr:`VmToolsMonitoringSettings.max_failure_window`
            specifies. If :attr:`VmToolsMonitoringSettings.max_failure_window`
            is -1 (no window), this represents the absolute number of failures
            after which automated response is stopped. 
            
            If a virtual machine exceeds this threshold, in-depth problem
            analysis is usually needed. 
            
            The default value is 3.
        :type  max_failure_window: :class:`long` or ``None``
        :param max_failure_window: The number of seconds for the window during which up to
            :attr:`VmToolsMonitoringSettings.max_failures` resets can occur
            before automated responses stop. 
            
            If set to -1, no failure window is specified. 
            
            The default value is -1.
        """
        self.enabled = enabled
        self.cluster_settings = cluster_settings
        self.failure_interval = failure_interval
        self.min_up_time = min_up_time
        self.max_failures = max_failures
        self.max_failure_window = max_failure_window
        VapiStruct.__init__(self)


VmToolsMonitoringSettings._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.vm_tools_monitoring_settings', {
        'enabled': type.OptionalType(type.BooleanType()),
        'cluster_settings': type.OptionalType(type.BooleanType()),
        'failure_interval': type.OptionalType(type.IntegerType()),
        'min_up_time': type.OptionalType(type.IntegerType()),
        'max_failures': type.OptionalType(type.IntegerType()),
        'max_failure_window': type.OptionalType(type.IntegerType()),
    },
    VmToolsMonitoringSettings,
    False,
    None))



class VsphereHA(VapiStruct):
    """
    The ``DasInfo`` class contains attributes describing the HA specific
    configurations of a cluster. It contains cluster-wide configurations for
    DAS.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                 failures_and_responses=None,
                 admission_control=None,
                 heartbeat_datastores=None,
                 advanced_options=None,
                ):
        """
        :type  enabled: :class:`bool`
        :param enabled: HA Enabled or Disabled Flag to indicate whether or not vSphere HA
            feature is enabled.
        :type  failures_and_responses: :class:`FailuresAndResponses` or ``None``
        :param failures_and_responses: Configuration settings for HA Failures and responses.
            If None or empty, the value is skipped.
        :type  admission_control: :class:`AdmissionControl` or ``None``
        :param admission_control: Configuration settings for HA admission control.
            If None or empty, the value is skipped.
        :type  heartbeat_datastores: :class:`HeartBeatDataStores` or ``None``
        :param heartbeat_datastores: Configuration settings for heart beat data store policy.
            If None or empty, the value is skipped.
        :type  advanced_options: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.OptionValue` or ``None``
        :param advanced_options: Advanced settings.
            If None or empty, the value is skipped.
        """
        self.enabled = enabled
        self.failures_and_responses = failures_and_responses
        self.admission_control = admission_control
        self.heartbeat_datastores = heartbeat_datastores
        self.advanced_options = advanced_options
        VapiStruct.__init__(self)


VsphereHA._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha.vsphere_HA', {
        'enabled': type.BooleanType(),
        'failures_and_responses': type.OptionalType(type.ReferenceType(__name__, 'FailuresAndResponses')),
        'admission_control': type.OptionalType(type.ReferenceType(__name__, 'AdmissionControl')),
        'heartbeat_datastores': type.OptionalType(type.ReferenceType(__name__, 'HeartBeatDataStores')),
        'advanced_options': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'OptionValue'))),
    },
    VsphereHA,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

