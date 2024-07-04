# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.vcha.cluster.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.vcha.cluster_client`` module provides classes for
redeploying and monitoring a vCenter High Availability (VCHA) Cluster after a
successful initial deployment.

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


class Active(VapiInterface):
    """
    The ``Active`` class provides methods to get information related to the
    active vCenter High Availability (VCHA) node. This class was added in
    vSphere API 6.7.1.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vcha.cluster.active'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ActiveStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Active.Info`` class contains the network and placement information of
        the active node of a VCHA Cluster. This class was added in vSphere API
        6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     management=None,
                     ha=None,
                     placement=None,
                    ):
            """
            :type  management: :class:`com.vmware.vcenter.vcha_client.IpSpec`
            :param management: IP specification for the Management network. This attribute was
                added in vSphere API 6.7.1.
            :type  ha: :class:`com.vmware.vcenter.vcha_client.IpSpec` or ``None``
            :param ha: IP specification for the HA network. This attribute was added in
                vSphere API 6.7.1.
                If None, then the second NIC of the Active Node of the VCHA cluster
                is not configured.
            :type  placement: :class:`com.vmware.vcenter.vcha_client.PlacementInfo` or ``None``
            :param placement: Contains the placement information of the active node. This
                attribute was added in vSphere API 6.7.1.
                If None, the request specified that placement information of the
                active node should not be included.
            """
            self.management = management
            self.ha = ha
            self.placement = placement
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.active.info', {
            'management': type.ReferenceType('com.vmware.vcenter.vcha_client', 'IpSpec'),
            'ha': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'IpSpec')),
            'placement': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'PlacementInfo')),
        },
        Info,
        False,
        None))



    def get(self,
            vc_spec=None,
            partial=None,
            ):
        """
        Retrieves information about the active node of a VCHA cluster. This
        method was added in vSphere API 6.7.1.

        :type  vc_spec: :class:`com.vmware.vcenter.vcha_client.CredentialsSpec` or ``None``
        :param vc_spec: Contains active node's management vCenter server credentials.
            If None, then the active vCenter Server instance is assumed to be
            either self-managed or else in enhanced linked mode and managed by
            a linked vCenter Server instance.
        :type  partial: :class:`bool` or ``None``
        :param partial: If true, then return only the information that does not require
            connecting to the Active vCenter Server. 
            If false or unset, then return all the information.
            If None, then return all the information.
        :rtype: :class:`Active.Info`
        :return: Info Information about the VCHA network and placement of the active
            node.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the credentials provided for authentincating with the active
            node's management vCenter server are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user has insufficient privilege to perform the operation. 
            
            * If ``partial`` is false or unset, then the operation execution
              requires the Global.VCServer privilege.
            * If ``partial`` is true, then the operation execution requires the
              System.Read privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            If the SSL certificate of the management vCenter server cannot be
            validated. 
            The value of the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` will be a class
            that contains all the attributes defined in
            :class:`com.vmware.vcenter.vcha_client.CertificateInfo`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidElementConfiguration` 
            If the active node is on more than one datastore.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the active virtual machine is not managed by the specified
            vCenter server for the active node.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If the management interface IP address assignment is not static.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        return self._invoke('get',
                            {
                            'vc_spec': vc_spec,
                            'partial': partial,
                            })
class DeploymentType(VapiInterface):
    """
    The DeploymentType class provides methods to get the deployment type of a
    vCenter High Availability Cluster (VCHA Cluster). This class was added in
    vSphere API 6.7.1.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vcha.cluster.deployment_type'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DeploymentTypeStub)
        self._VAPI_OPERATION_IDS = {}

    class Type(Enum):
        """
        The ``DeploymentType.Type`` class defines the possible deployment types for
        a VCHA Cluster. This enumeration was added in vSphere API 6.7.1.

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
        VCHA Cluster is not configured. This class attribute was added in vSphere
        API 6.7.1.

        """
        AUTO = None
        """
        VCHA Cluster was deployed automatically. This class attribute was added in
        vSphere API 6.7.1.

        """
        MANUAL = None
        """
        VCHA Cluster was deployed manually. This class attribute was added in
        vSphere API 6.7.1.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'NONE': Type('NONE'),
        'AUTO': Type('AUTO'),
        'MANUAL': Type('MANUAL'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vcha.cluster.deployment_type.type',
        Type))


    class Info(VapiStruct):
        """
        The ``DeploymentType.Info`` class contains the deployment type of the VCHA
        Cluster. This class was added in vSphere API 6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     deployment_type=None,
                    ):
            """
            :type  deployment_type: :class:`DeploymentType.Type`
            :param deployment_type: Identifies the deployment type of the VCHA cluster. This attribute
                was added in vSphere API 6.7.1.
            """
            self.deployment_type = deployment_type
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.deployment_type.info', {
            'deployment_type': type.ReferenceType(__name__, 'DeploymentType.Type'),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Retrieves the deployment type of a VCHA cluster. This method was added
        in vSphere API 6.7.1.


        :rtype: :class:`DeploymentType.Info`
        :return: Info structure containing the deployment type information of the
            the VCHA cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user has insufficient privilege to perform the operation.
            Operation execution requires the System.Read privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        return self._invoke('get', None)
class Mode(VapiInterface):
    """
    The Mode class provides methods to manage the operating mode of a vCenter
    High Availability Cluster (VCHA Cluster). This class was added in vSphere
    API 6.7.1.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vcha.cluster.mode'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ModeStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'set_task': 'set$task'})

    class ClusterMode(Enum):
        """
        The ``Mode.ClusterMode`` class defines the possible modes for a VCHA
        Cluster. This enumeration was added in vSphere API 6.7.1.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        ENABLED = None
        """
        VCHA Cluster is enabled. State replication between the Active and Passive
        node is enabled and automatic failover is allowed. This class attribute was
        added in vSphere API 6.7.1.

        """
        DISABLED = None
        """
        VCHA Cluster is disabled. State replication between the Active and Passive
        node is disabled and automatic failover is not allowed. This class
        attribute was added in vSphere API 6.7.1.

        """
        MAINTENANCE = None
        """
        VCHA Cluster is in maintenance mode. State replication between the and
        Passive node is enabled but automatic failover is not allowed. This class
        attribute was added in vSphere API 6.7.1.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ClusterMode` instance.
            """
            Enum.__init__(string)

    ClusterMode._set_values({
        'ENABLED': ClusterMode('ENABLED'),
        'DISABLED': ClusterMode('DISABLED'),
        'MAINTENANCE': ClusterMode('MAINTENANCE'),
    })
    ClusterMode._set_binding_type(type.EnumType(
        'com.vmware.vcenter.vcha.cluster.mode.cluster_mode',
        ClusterMode))


    class Info(VapiStruct):
        """
        The ``Mode.Info`` class contains the mode of the VCHA Cluster. This class
        was added in vSphere API 6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     mode=None,
                    ):
            """
            :type  mode: :class:`Mode.ClusterMode`
            :param mode: Identifies the mode of the VCHA cluster. This attribute was added
                in vSphere API 6.7.1.
            """
            self.mode = mode
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.mode.info', {
            'mode': type.ReferenceType(__name__, 'Mode.ClusterMode'),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Retrieves the current mode of a VCHA cluster. This method was added in
        vSphere API 6.7.1.


        :rtype: :class:`Mode.Info`
        :return: Info structure containing the mode of the the VCHA cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the VCHA cluster is not configured.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user has insufficient privilege to perform the operation.
            Operation execution requires the System.Read privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        return self._invoke('get', None)


    def set_task(self,
            mode,
            ):
        """
        Manipulates the mode of a VCHA Cluster. Following mode transitions are
        allowed:
        enabled -> disabled - Allowed only in healthy and degraded states.
        enabled -> maintenance - Allowed only in healthy state.
        disabled -> enabled - Allowed only in healthy state.
        maintenance -> enabled - Allowed only in healthy state with all nodes
        are running the same version.
        maintenance -> disabled - Allowed only in healthy state with all nodes
        are running the same version.
        All other transitions are not allowed. 
        
        VCHA Cluster configuration remains intact in any of the cluster modes..
        This method was added in vSphere API 6.7.1.

        :type  mode: :class:`Mode.ClusterMode`
        :param mode: Clustermode to change the VCHA cluster mode to.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user has insufficient privilege to perform the operation.
            Operation execution requires the Global.VCServer privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        task_id = self._invoke('set$task',
                                {
                                'mode': mode,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class Passive(VapiInterface):
    """
    The ``Passive`` class provides methods to validate a passive's placement
    configuration and redeploy the passive node in a vCenter High Availability
    (VCHA) cluster. This class was added in vSphere API 6.7.1.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vcha.cluster.passive'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PassiveStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'redeploy_task': 'redeploy$task'})

    class CheckSpec(VapiStruct):
        """
        The ``Passive.CheckSpec`` class contains placement information for
        validation. This class was added in vSphere API 6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vc_spec=None,
                     placement=None,
                    ):
            """
            :type  vc_spec: :class:`com.vmware.vcenter.vcha_client.CredentialsSpec` or ``None``
            :param vc_spec: Contains the active node's management vCenter server credentials.
                This attribute was added in vSphere API 6.7.1.
                If None, then the active vCenter Server instance is assumed to be
                either self-managed or else in enhanced linked mode and managed by
                a linked vCenter Server instance.
            :type  placement: :class:`com.vmware.vcenter.vcha_client.PlacementSpec`
            :param placement: Contains the node's placement information for validation. This
                attribute was added in vSphere API 6.7.1.
            """
            self.vc_spec = vc_spec
            self.placement = placement
            VapiStruct.__init__(self)


    CheckSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.passive.check_spec', {
            'vc_spec': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'CredentialsSpec')),
            'placement': type.ReferenceType('com.vmware.vcenter.vcha_client', 'PlacementSpec'),
        },
        CheckSpec,
        False,
        None))


    class CheckResult(VapiStruct):
        """
        The ``Passive.CheckResult`` class contains the warnings and errors that
        will occur during the clone operation. This class was added in vSphere API
        6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     warnings=None,
                     errors=None,
                    ):
            """
            :type  warnings: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param warnings: A list of problems which may require attention, but which are not
                fatal. This attribute was added in vSphere API 6.7.1.
            :type  errors: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param errors: A list of problems which are fatal to the operation and the
                operation will fail. This attribute was added in vSphere API 6.7.1.
            """
            self.warnings = warnings
            self.errors = errors
            VapiStruct.__init__(self)


    CheckResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.passive.check_result', {
            'warnings': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'errors': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        CheckResult,
        False,
        None))


    class RedeploySpec(VapiStruct):
        """
        The ``Passive.RedeploySpec`` class contains the redeploy specification.
        This class was added in vSphere API 6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vc_spec=None,
                     placement=None,
                     ha_ip=None,
                     failover_ip=None,
                    ):
            """
            :type  vc_spec: :class:`com.vmware.vcenter.vcha_client.CredentialsSpec` or ``None``
            :param vc_spec: Contains the active node's management vCenter server credentials.
                This attribute was added in vSphere API 6.7.1.
                If None, then the active vCenter Server instance is assumed to be
                either self-managed or else in enhanced linked mode and managed by
                a linked vCenter Server instance.
            :type  placement: :class:`com.vmware.vcenter.vcha_client.PlacementSpec`
            :param placement: Contains the node's placement information. This attribute was added
                in vSphere API 6.7.1.
            :type  ha_ip: :class:`com.vmware.vcenter.vcha_client.IpSpec` or ``None``
            :param ha_ip: Contains the VCHA HA network configuration of the node. All cluster
                communication (state replication, heartbeat, cluster messages)
                happens over this network. This attribute was added in vSphere API
                6.7.1.
                If None, then the stored network configuration for the VCHA HA
                network for the passive node will be used.
            :type  failover_ip: :class:`com.vmware.vcenter.vcha_client.IpSpec` or ``None``
            :param failover_ip: Failover IP address that this node must assume after the failover
                to serve client requests. This attribute was added in vSphere API
                6.7.1.
                If None, then the public IP address of the Active vCenter Server is
                assumed.
            """
            self.vc_spec = vc_spec
            self.placement = placement
            self.ha_ip = ha_ip
            self.failover_ip = failover_ip
            VapiStruct.__init__(self)


    RedeploySpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.passive.redeploy_spec', {
            'vc_spec': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'CredentialsSpec')),
            'placement': type.ReferenceType('com.vmware.vcenter.vcha_client', 'PlacementSpec'),
            'ha_ip': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'IpSpec')),
            'failover_ip': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'IpSpec')),
        },
        RedeploySpec,
        False,
        None))



    def check(self,
              spec,
              ):
        """
        Validates the specified passive node's placement configuration. This
        method was added in vSphere API 6.7.1.

        :type  spec: :class:`Passive.CheckSpec`
        :param spec: Contains the passive node's placement specification.
        :rtype: :class:`Passive.CheckResult`
        :return: CheckResult structure containing errors and warnings.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the credentials provided for authentincating with the active
            node's management vCenter server are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the specified resource spec is deemed invalid for the clone
            operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            If the SSL certificate of the management vCenter server cannot be
            validated.
            The value of the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` will be a class
            that contains all the attributes defined in
            :class:`com.vmware.vcenter.vcha_client.CertificateInfo`.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the active virtual machine is not managed by the specified
            vCenter server for the active node.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidElementConfiguration` 
            If the active node is on more than one datastore.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the clone operation is not allowed in the current state of the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user has insufficient privilege to perform the operation.
            Operation execution requires the Global.VCServer privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        return self._invoke('check',
                            {
                            'spec': spec,
                            })


    def redeploy_task(self,
                 spec,
                 ):
        """
        Creates the passive node in a degraded cluster with node location
        information and pre-existing VCHA cluster configuration from the active
        node. This method was added in vSphere API 6.7.1.

        :type  spec: :class:`Passive.RedeploySpec`
        :param spec: Contains the passive node's redeploy specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the credentials provided for authentincating with the active
            node's management vCenter server are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user has insufficient privilege to perform the operation.
            Operation execution requires the Global.VCServer privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            If the SSL certificate of the management vCenter server cannot be
            validated.
            The value of the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` will be a class
            that contains all the attributes defined in
            :class:`com.vmware.vcenter.vcha_client.CertificateInfo`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        task_id = self._invoke('redeploy$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class Witness(VapiInterface):
    """
    The ``Witness`` class provides methods to validate a witness's placement
    configuration and redeploy the witness node in a vCenter High Availability
    (VCHA) cluster. This class was added in vSphere API 6.7.1.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.vcha.cluster.witness'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _WitnessStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'redeploy_task': 'redeploy$task'})

    class CheckSpec(VapiStruct):
        """
        The ``Witness.CheckSpec`` class contains placement information for
        validation. This class was added in vSphere API 6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vc_spec=None,
                     placement=None,
                    ):
            """
            :type  vc_spec: :class:`com.vmware.vcenter.vcha_client.CredentialsSpec` or ``None``
            :param vc_spec: Contains the active node's management vCenter server credentials.
                This attribute was added in vSphere API 6.7.1.
                If None, then the active vCenter Server instance is assumed to be
                either self-managed or else in enhanced linked mode and managed by
                a linked vCenter Server instance.
            :type  placement: :class:`com.vmware.vcenter.vcha_client.PlacementSpec`
            :param placement: Contains the node's placement information for validation. This
                attribute was added in vSphere API 6.7.1.
            """
            self.vc_spec = vc_spec
            self.placement = placement
            VapiStruct.__init__(self)


    CheckSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.witness.check_spec', {
            'vc_spec': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'CredentialsSpec')),
            'placement': type.ReferenceType('com.vmware.vcenter.vcha_client', 'PlacementSpec'),
        },
        CheckSpec,
        False,
        None))


    class CheckResult(VapiStruct):
        """
        The ``Witness.CheckResult`` class contains the warnings and errors that
        will occur during the clone operation. This class was added in vSphere API
        6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     warnings=None,
                     errors=None,
                    ):
            """
            :type  warnings: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param warnings: A list of problems which may require attention, but which are not
                fatal. This attribute was added in vSphere API 6.7.1.
            :type  errors: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param errors: A list of problems which are fatal to the operation and the
                operation will fail. This attribute was added in vSphere API 6.7.1.
            """
            self.warnings = warnings
            self.errors = errors
            VapiStruct.__init__(self)


    CheckResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.witness.check_result', {
            'warnings': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'errors': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        CheckResult,
        False,
        None))


    class RedeploySpec(VapiStruct):
        """
        The ``Witness.RedeploySpec`` class contains the redeploy specification.
        This class was added in vSphere API 6.7.1.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vc_spec=None,
                     placement=None,
                     ha_ip=None,
                    ):
            """
            :type  vc_spec: :class:`com.vmware.vcenter.vcha_client.CredentialsSpec` or ``None``
            :param vc_spec: Contains the active node's management vCenter server credentials.
                This attribute was added in vSphere API 6.7.1.
                If None, then the active vCenter Server instance is assumed to be
                either self-managed or else in enhanced linked mode and managed by
                a linked vCenter Server instance.
            :type  placement: :class:`com.vmware.vcenter.vcha_client.PlacementSpec`
            :param placement: Contains the node's placement information. This attribute was added
                in vSphere API 6.7.1.
            :type  ha_ip: :class:`com.vmware.vcenter.vcha_client.IpSpec` or ``None``
            :param ha_ip: Contains the VCHA HA network configuration of the node. All cluster
                communication (state replication, heartbeat, cluster messages)
                happens over this network. This attribute was added in vSphere API
                6.7.1.
                If None, then the stored network configuration for the VCHA HA
                network for the witness node will be used.
            """
            self.vc_spec = vc_spec
            self.placement = placement
            self.ha_ip = ha_ip
            VapiStruct.__init__(self)


    RedeploySpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.vcha.cluster.witness.redeploy_spec', {
            'vc_spec': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'CredentialsSpec')),
            'placement': type.ReferenceType('com.vmware.vcenter.vcha_client', 'PlacementSpec'),
            'ha_ip': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'IpSpec')),
        },
        RedeploySpec,
        False,
        None))



    def check(self,
              spec,
              ):
        """
        Validates the specified witness node's placement configuration. This
        method was added in vSphere API 6.7.1.

        :type  spec: :class:`Witness.CheckSpec`
        :param spec: Contains the witness node's placement specification.
        :rtype: :class:`Witness.CheckResult`
        :return: CheckResult structure containing errors and warnings.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the credentials provided for authentincating with the active
            node's management vCenter server are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the specified resource spec is deemed invalid for the clone
            operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            If the SSL certificate of the management vCenter server cannot be
            validated.
            The value of the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` will be a class
            that contains all the attributes defined in
            :class:`com.vmware.vcenter.vcha_client.CertificateInfo`.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the active virtual machine is not managed by the specified
            vCenter server for the active node.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidElementConfiguration` 
            If the active node is on more than one datastore.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the clone operation is not allowed in the current state of the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user has insufficient privilege to perform the operation.
            Operation execution requires the Global.VCServer privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        return self._invoke('check',
                            {
                            'spec': spec,
                            })


    def redeploy_task(self,
                 spec,
                 ):
        """
        Creates the witness node in a degraded cluster with node location
        information and pre-existing VCHA cluster configuration from the active
        node. This method was added in vSphere API 6.7.1.

        :type  spec: :class:`Witness.RedeploySpec`
        :param spec: Contains the witness node's redeploy specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the credentials provided for authentincating with the active
            node's management vCenter server are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user has insufficient privilege to perform the operation.
            Operation execution requires the Global.VCServer privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            If the SSL certificate of the management vCenter server cannot be
            validated.
            The value of the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` will be a class
            that contains all the attributes defined in
            :class:`com.vmware.vcenter.vcha_client.CertificateInfo`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        """
        task_id = self._invoke('redeploy$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class _ActiveStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'vc_spec': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vcha_client', 'CredentialsSpec')),
            'partial': type.OptionalType(type.BooleanType()),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),
            'com.vmware.vapi.std.errors.invalid_element_configuration':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidElementConfiguration'),
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
            http_method='POST',
            url_template='/vcenter/vcha/cluster/active',
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
                'output_type': type.ReferenceType(__name__, 'Active.Info'),
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
            self, iface_name='com.vmware.vcenter.vcha.cluster.active',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _DeploymentTypeStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
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
            url_template='/vcenter/vcha/cluster/deployment-type',
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
                'output_type': type.ReferenceType(__name__, 'DeploymentType.Info'),
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
            self, iface_name='com.vmware.vcenter.vcha.cluster.deployment_type',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ModeStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
            url_template='/vcenter/vcha/cluster/mode',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'mode': type.ReferenceType(__name__, 'Mode.ClusterMode'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/vcenter/vcha/cluster/mode',
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
                'output_type': type.ReferenceType(__name__, 'Mode.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set$task': {
                'input_type': set_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': set_error_dict,
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'set': set_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vcha.cluster.mode',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _PassiveStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Passive.CheckSpec'),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_element_configuration':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidElementConfiguration'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vcha/cluster/passive',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for redeploy operation
        redeploy_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Passive.RedeploySpec'),
        })
        redeploy_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        redeploy_input_value_validator_list = [
        ]
        redeploy_output_validator_list = [
        ]
        redeploy_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vcha/cluster/passive',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'check': {
                'input_type': check_input_type,
                'output_type': type.ReferenceType(__name__, 'Passive.CheckResult'),
                'errors': check_error_dict,
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': check_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'redeploy$task': {
                'input_type': redeploy_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': redeploy_error_dict,
                'input_value_validator_list': redeploy_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'check': check_rest_metadata,
            'redeploy': redeploy_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vcha.cluster.passive',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _WitnessStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Witness.CheckSpec'),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_element_configuration':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidElementConfiguration'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vcha/cluster/witness',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for redeploy operation
        redeploy_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Witness.RedeploySpec'),
        })
        redeploy_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        redeploy_input_value_validator_list = [
        ]
        redeploy_output_validator_list = [
        ]
        redeploy_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vcha/cluster/witness',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'check': {
                'input_type': check_input_type,
                'output_type': type.ReferenceType(__name__, 'Witness.CheckResult'),
                'errors': check_error_dict,
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': check_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'redeploy$task': {
                'input_type': redeploy_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': redeploy_error_dict,
                'input_value_validator_list': redeploy_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'check': check_rest_metadata,
            'redeploy': redeploy_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.vcha.cluster.witness',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Active': Active,
        'DeploymentType': DeploymentType,
        'Mode': Mode,
        'Passive': Passive,
        'Witness': Witness,
    }

