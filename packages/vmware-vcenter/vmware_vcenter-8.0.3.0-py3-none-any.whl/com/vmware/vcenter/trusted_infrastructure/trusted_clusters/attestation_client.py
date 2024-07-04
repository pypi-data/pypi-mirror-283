# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation_client``
module provides classes for configuring Attestation Services for Trusted
Clusters.

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


class Services(VapiInterface):
    """
    The ``Services`` class manages the Attestation Service instances a Trusted
    Cluster is configured to use. This class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ServicesStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})

    class Summary(VapiStruct):
        """
        The ``Services.Summary`` class contains basic information about a
        registered Attestation Service instance that is configured for a cluster.
        This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     service=None,
                     address=None,
                     group=None,
                     trust_authority_cluster=None,
                    ):
            """
            :type  service: :class:`str`
            :param service: The service's unique identifier. This attribute was added in
                vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
            :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
            :param address: The service's address. This attribute was added in vSphere API
                7.0.0.0.
            :type  group: :class:`str`
            :param group: The group specifies the Key Provider Service instances can accept
                reports issued by this Attestation Service instance. This attribute
                was added in vSphere API 7.0.0.0.
            :type  trust_authority_cluster: :class:`str`
            :param trust_authority_cluster: The cluster specifies the Trust Authority Cluster this Attestation
                Service belongs to. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.service = service
            self.address = address
            self.group = group
            self.trust_authority_cluster = trust_authority_cluster
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services.summary', {
            'service': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.attestation.Service'),
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
            'group': type.StringType(),
            'trust_authority_cluster': type.StringType(),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Services.Info`` class contains all the stored information about a
        registered Attestation Service instance that is configured for a cluster.
        This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'trusted_CA': 'trusted_ca',
                                }

        def __init__(self,
                     address=None,
                     trusted_ca=None,
                     group=None,
                     trust_authority_cluster=None,
                    ):
            """
            :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
            :param address: The service's address. This attribute was added in vSphere API
                7.0.0.0.
            :type  trusted_ca: :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain`
            :param trusted_ca: The service's TLS certificate chain. This attribute was added in
                vSphere API 7.0.0.0.
            :type  group: :class:`str`
            :param group: The group determines the Key Provider Service instances can accept
                reports issued by this Attestation Service instance. This attribute
                was added in vSphere API 7.0.0.0.
            :type  trust_authority_cluster: :class:`str`
            :param trust_authority_cluster: The cluster specifies the Trust Authority Cluster this Attestation
                Service belongs to. This attribute was added in vSphere API
                7.0.0.0.
            """
            self.address = address
            self.trusted_ca = trusted_ca
            self.group = group
            self.trust_authority_cluster = trust_authority_cluster
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services.info', {
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
            'trusted_CA': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain'),
            'group': type.StringType(),
            'trust_authority_cluster': type.StringType(),
        },
        Info,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Services.CreateSpec`` class contains the data necessary for
        configuring a registered Attestation Service instance with a cluster in the
        environment. This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'SERVICE' : [('service', True)],
                    'CLUSTER' : [('trust_authority_cluster', True)],
                }
            ),
        ]



        def __init__(self,
                     type=None,
                     service=None,
                     trust_authority_cluster=None,
                    ):
            """
            :type  type: :class:`Services.CreateSpec.SourceType`
            :param type: Source of truth for the configuration of the Attestation Service.
                This attribute was added in vSphere API 7.0.0.0.
            :type  service: :class:`str`
            :param service: The service's unique ID. This attribute was added in vSphere API
                7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Services.CreateSpec.SourceType.SERVICE`.
            :type  trust_authority_cluster: :class:`str`
            :param trust_authority_cluster: The attestation cluster's unique ID. This attribute was added in
                vSphere API 7.0.0.0.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Services.CreateSpec.SourceType.CLUSTER`.
            """
            self.type = type
            self.service = service
            self.trust_authority_cluster = trust_authority_cluster
            VapiStruct.__init__(self)


        class SourceType(Enum):
            """
            The ``Services.CreateSpec.SourceType`` class specifies the source of truth
            the Attestation Service will use for its configuration. This enumeration
            was added in vSphere API 7.0.0.0.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            SERVICE = None
            """
            The Attestation Service will be configured based on an ID of an specific
            Attestation Service. This class attribute was added in vSphere API 7.0.0.0.

            """
            CLUSTER = None
            """
            The Attestation Service will be configured based on an ID of a whole
            attestation cluster. This class attribute was added in vSphere API 7.0.0.0.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`SourceType` instance.
                """
                Enum.__init__(string)

        SourceType._set_values({
            'SERVICE': SourceType('SERVICE'),
            'CLUSTER': SourceType('CLUSTER'),
        })
        SourceType._set_binding_type(type.EnumType(
            'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services.create_spec.source_type',
            SourceType))

    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services.create_spec', {
            'type': type.ReferenceType(__name__, 'Services.CreateSpec.SourceType'),
            'service': type.OptionalType(type.IdType()),
            'trust_authority_cluster': type.OptionalType(type.StringType()),
        },
        CreateSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Services.FilterSpec`` class contains the data necessary for
        identifying a Attestation service instance. This class was added in vSphere
        API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     services=None,
                     address=None,
                     group=None,
                     trust_authority_cluster=None,
                    ):
            """
            :type  services: :class:`set` of :class:`str` or ``None``
            :param services: A set of IDs by which to filter the services. This attribute was
                added in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                When methods return a value of this class as a return value, the
                attribute will contain identifiers for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                If None, the services will not be filtered by ID.
            :type  address: :class:`list` of :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress` or ``None``
            :param address: The service's address. This attribute was added in vSphere API
                7.0.0.0.
                If None, the services will not be filtered by address.
            :type  group: :class:`set` of :class:`str` or ``None``
            :param group: The group specifies the Key Provider Service instances can accept
                reports issued by this Attestation Service instance. This attribute
                was added in vSphere API 7.0.0.0.
                If None, the services will not be filtered by group.
            :type  trust_authority_cluster: :class:`set` of :class:`str` or ``None``
            :param trust_authority_cluster: The cluster specifies the Trust Authority Cluster this Attestation
                Service instance belongs to. This attribute was added in vSphere
                API 7.0.0.0.
                If None, the services will not be filtered by
                trustAuthorityCluster.
            """
            self.services = services
            self.address = address
            self.group = group
            self.trust_authority_cluster = trust_authority_cluster
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services.filter_spec', {
            'services': type.OptionalType(type.SetType(type.IdType())),
            'address': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'))),
            'group': type.OptionalType(type.SetType(type.StringType())),
            'trust_authority_cluster': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             cluster,
             spec=None,
             ):
        """
        Returns the basic information about all configured Attestation Service
        instances used by this cluster. This method was added in vSphere API
        7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`Services.FilterSpec` or ``None``
        :param spec: Only return services matching the filters.
            If None return all services.
        :rtype: :class:`list` of :class:`Services.Summary`
        :return: Basic information about all configured Attestation Service
            instances used by this cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the cluster ID is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ReadTrustedHosts``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires ``System.View``.
        """
        return self._invoke('list',
                            {
                            'cluster': cluster,
                            'spec': spec,
                            })

    def get(self,
            cluster,
            service,
            ):
        """
        Returns detailed information about the given registered Attestation
        Service instance that is configured for the given cluster. This method
        was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  service: :class:`str`
        :param service: The ID of the service.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
        :rtype: :class:`Services.Info`
        :return: Detailed information about the specified Attestation Service
            configured for the given cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the cluster or the service ID is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``TrustedAdmin.ReadTrustedHosts``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires ``System.View``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            'service': service,
                            })


    def create_task(self,
               cluster,
               spec,
               ):
        """
        Configures the cluster to use a the given registered Attestation
        Service. This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`Services.CreateSpec`
        :param spec: Describes the registered instance of the Attestation Service
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if the Attestation Service is already configured for this cluster
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            for any other error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the CreateSpec is not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the cluster ID is not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if all the hosts in the cluster do not have VMware vSphere Trust
            Authority enabled license.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        task_id = self._invoke('create$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.attestation.Service'))
        return task_instance


    def delete_task(self,
               cluster,
               service,
               ):
        """
        Removes the Attestation Service instance from the configuration of the
        given cluster. This method was added in vSphere API 7.0.0.0.

        :type  cluster: :class:`str`
        :param cluster: the unique ID of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  service: :class:`str`
        :param service: the registered Attestation Service instance unique identifier.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the Attestation Service instance or the cluster are not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cluster': cluster,
                                'service': service,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class ServicesAppliedConfig(VapiInterface):
    """
    The ``ServicesAppliedConfig`` class provides information about the
    aggregate health of the applied Attestation Service configuration on the
    Trusted Clusters. The desired state of the Attestation Service is stored
    within vCenter, while the applied configuration is stored on the hosts in
    the cluster. The ``ServicesAppliedConfig`` class is available for all
    clusters, not only Trusted Clusters. In such cases empty desired state is
    assumed, e.g. when an applied Attestation Service configuration is found
    outside of a Trusted Cluster it is considered an
    :attr:`ServicesAppliedConfig.Health.ERROR`. The ``ServicesAppliedConfig``
    class is able to put the applied Attestation Service configuration into a
    consistent state when individual host configurations have diverged from the
    desired state. This class was added in vSphere API 7.0.1.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services_applied_config'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ServicesAppliedConfigStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'list_task': 'list$task'})
        self._VAPI_OPERATION_IDS.update({'get_task': 'get$task'})
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})

    class Health(Enum):
        """
        The ``ServicesAppliedConfig.Health`` class is an indicator for the
        consistency of the applied Attestation Service configuration in a cluster
        with respect to the desired state. This enumeration was added in vSphere
        API 7.0.1.0.

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
        The consistency of the applied configuration is unknown. This class
        attribute was added in vSphere API 7.0.1.0.

        """
        OK = None
        """
        The applied Attestation Service configuration is consistent with the
        desired state. This class attribute was added in vSphere API 7.0.1.0.

        """
        ERROR = None
        """
        The applied Attestation Service configuration has diverged from the desired
        state. This class attribute was added in vSphere API 7.0.1.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Health` instance.
            """
            Enum.__init__(string)

    Health._set_values({
        'NONE': Health('NONE'),
        'OK': Health('OK'),
        'ERROR': Health('ERROR'),
    })
    Health._set_binding_type(type.EnumType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services_applied_config.health',
        Health))


    class Summary(VapiStruct):
        """
        The ``ServicesAppliedConfig.Summary`` class contains basic information
        about the aggregated health status for a service. This class was added in
        vSphere API 7.0.1.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     health=None,
                     address=None,
                     service=None,
                    ):
            """
            :type  health: :class:`ServicesAppliedConfig.Health`
            :param health: The health value indicates whether the configuration applied to the
                cluster differs from the desired state. This attribute was added in
                vSphere API 7.0.1.0.
            :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
            :param address: The network address of the Attestation Service configured for use
                in the Trusted Cluster. This attribute was added in vSphere API
                7.0.1.0.
            :type  service: :class:`str` or ``None``
            :param service: The unique identifier of an Attestation Service configuration from
                the desired state. This attribute was added in vSphere API 7.0.1.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                If None, this Attestation Service is not registered within this
                vCenter and thus the applied configuration is not present in the
                desired state.
            """
            self.health = health
            self.address = address
            self.service = service
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services_applied_config.summary', {
            'health': type.ReferenceType(__name__, 'ServicesAppliedConfig.Health'),
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
            'service': type.OptionalType(type.IdType()),
        },
        Summary,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``ServicesAppliedConfig.FilterSpec`` class specifies the matching
        criteria to be applied when filtering out ``ServicesAppliedConfig.Summary``
        structures from the collection returned by the list method. Only
        ``ServicesAppliedConfig.Summary`` structures containing the values
        specified in this structure will be returned from the list method. If
        multiple members of the filter spec are set, all of them must match for a
        result to be filtered out and returned. This class was added in vSphere API
        7.0.1.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     health=None,
                     address=None,
                    ):
            """
            :type  health: :class:`set` of :class:`ServicesAppliedConfig.Health` or ``None``
            :param health: The health of the applied Attestation Service configuration. This
                attribute was added in vSphere API 7.0.1.0.
                If None, no filtration will be performed by health.
            :type  address: :class:`list` of :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress` or ``None``
            :param address: The network address of the Attestation Service configured for use
                in the Trusted Cluster. This attribute was added in vSphere API
                7.0.1.0.
                If None, no filtration will be performed by network address.
            """
            self.health = health
            self.address = address
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services_applied_config.filter_spec', {
            'health': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'ServicesAppliedConfig.Health'))),
            'address': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'))),
        },
        FilterSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``ServicesAppliedConfig.Info`` class contains detailed information
        about an applied Attestation Service configuration in a Trusted cluster.
        This class was added in vSphere API 7.0.1.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     health=None,
                     address=None,
                     service=None,
                     groups=None,
                     trustedc_as=None,
                     details=None,
                    ):
            """
            :type  health: :class:`ServicesAppliedConfig.Health`
            :param health: A health value which indicates whether the configuration applied to
                the cluster differs from the desired state. This attribute was
                added in vSphere API 7.0.1.0.
            :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
            :param address: The network address of the Attestation Service configured for use
                in the Trusted Cluster. This attribute was added in vSphere API
                7.0.1.0.
            :type  service: :class:`str` or ``None``
            :param service: The unique identifier of an Attestation Service configuration from
                the desired state. This attribute was added in vSphere API 7.0.1.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.trusted_infrastructure.attestation.Service``.
                If None, this Attestation Service is not registered within this
                vCenter and thus the applied configuration is not present in the
                desired state.
            :type  groups: :class:`set` of :class:`str`
            :param groups: The set of distinct groups found on the hosts in the cluster which
                differ from the desired state. This attribute was added in vSphere
                API 7.0.1.0.
            :type  trustedc_as: :class:`list` of :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain`
            :param trustedc_as: A list of distinct trusted CA chains found on the hosts in the
                cluster which differ from the desired state. This attribute was
                added in vSphere API 7.0.1.0.
            :type  details: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details regarding the health. When the
                ``ServicesAppliedConfig.Health`` is not
                :attr:`ServicesAppliedConfig.Health.OK`, this member will provide a
                detailed description of the issues present. This attribute was
                added in vSphere API 7.0.1.0.
            """
            self.health = health
            self.address = address
            self.service = service
            self.groups = groups
            self.trustedc_as = trustedc_as
            self.details = details
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services_applied_config.info', {
            'health': type.ReferenceType(__name__, 'ServicesAppliedConfig.Health'),
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
            'service': type.OptionalType(type.IdType()),
            'groups': type.SetType(type.StringType()),
            'trustedc_as': type.ListType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain')),
            'details': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Info,
        False,
        None))




    def list_task(self,
             cluster,
             spec=None,
             ):
        """
        Returns basic information about the health of all Attestation Service
        configurations applied to the cluster with respect to the desired
        state. This method was added in vSphere API 7.0.1.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster against which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`ServicesAppliedConfig.FilterSpec` or ``None``
        :param spec: The specification for the subset of results desired to be returned.
            If None all results are returned.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster ID is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no cluster corresponding to the given ID is found within this
            vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if there are ongoing mutating operations.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('list$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ListType(type.ReferenceType(__name__, 'ServicesAppliedConfig.Summary')))
        return task_instance


    def get_task(self,
            cluster,
            address,
            ):
        """
        Returns detailed information about the health of the specified
        Attestation Service configuration applied to the cluster with respect
        to the desired state. This method was added in vSphere API 7.0.1.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster against which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  address: :class:`com.vmware.vcenter.trusted_infrastructure_client.NetworkAddress`
        :param address: The network address of the Attestation Service instance.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster ID is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no cluster corresponding to the given ID is found within this
            vCenter or if no service corresponding to the given address is
            found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('get$task',
                                {
                                'cluster': cluster,
                                'address': address,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'ServicesAppliedConfig.Info'))
        return task_instance


    def update_task(self,
               cluster,
               ):
        """
        Update the applied Attestation Service configuration on the given
        Trusted Cluster to be consistent with the desired state. This method
        has no affect on the desired state, apart from it being used as a
        reference point for the remediation. This method was added in vSphere
        API 7.0.1.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the Trusted Cluster against which the operation will be
            executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster ID is empty
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no cluster corresponding to the given ID is found within this
            vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if there are ongoing mutating operations.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('update$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def delete_task(self,
               cluster,
               ):
        """
        Delete the Attestation Service configuration that has been applied to
        the given cluster. This method has no affect on the desired state, it
        only removes applied Attestation Service configuration from any Trusted
        Hosts within the given cluster. This method was added in vSphere API
        7.0.1.0.

        :type  cluster: :class:`str`
        :param cluster: The ID of the cluster against which the operation will be executed.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the cluster ID is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no cluster corresponding to the given ID is found within this
            vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if there are ongoing mutating operations.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cluster': cluster,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class _ServicesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'Services.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/attestation/services',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'query',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'service': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.attestation.Service'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/attestation/services/{service}',
            path_variables={
                'cluster': 'cluster',
                'service': 'service',
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

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'Services.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/attestation/services',
            request_body_parameter='spec',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'service': type.IdType(resource_types='com.vmware.vcenter.trusted_infrastructure.attestation.Service'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/attestation/services/{service}',
            path_variables={
                'cluster': 'cluster',
                'service': 'service',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'Services.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Services.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'delete$task': {
                'input_type': delete_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ServicesAppliedConfigStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'ServicesAppliedConfig.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/attestation/services-applied-config',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'query',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'address': type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'NetworkAddress'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/attestation/services-applied-config',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/attestation/services-applied-config',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/trusted-infrastructure/trusted-clusters/{cluster}/attestation/services-applied-config',
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

        operations = {
            'list$task': {
                'input_type': list_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'get$task': {
                'input_type': get_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'delete$task': {
                'input_type': delete_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.trusted_infrastructure.trusted_clusters.attestation.services_applied_config',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Services': Services,
        'ServicesAppliedConfig': ServicesAppliedConfig,
    }

