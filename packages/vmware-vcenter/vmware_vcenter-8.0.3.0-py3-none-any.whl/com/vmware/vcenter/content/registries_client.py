# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.content.registries.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.content.registries_client`` module provides classes
and classes for managing image registries in vCenter.

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

class DayOfWeek(Enum):
    """
    The ``DayOfWeek`` class describes the supported days of the week to run a
    specific operation for a container registry.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    SUNDAY = None
    """
    Sunday.

    """
    MONDAY = None
    """
    Monday.

    """
    TUESDAY = None
    """
    Tuesday.

    """
    WEDNESDAY = None
    """
    Wednesday.

    """
    THURSDAY = None
    """
    Thursday.

    """
    FRIDAY = None
    """
    Friday.

    """
    SATURDAY = None
    """
    Saturday.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`DayOfWeek` instance.
        """
        Enum.__init__(string)

DayOfWeek._set_values({
    'SUNDAY': DayOfWeek('SUNDAY'),
    'MONDAY': DayOfWeek('MONDAY'),
    'TUESDAY': DayOfWeek('TUESDAY'),
    'WEDNESDAY': DayOfWeek('WEDNESDAY'),
    'THURSDAY': DayOfWeek('THURSDAY'),
    'FRIDAY': DayOfWeek('FRIDAY'),
    'SATURDAY': DayOfWeek('SATURDAY'),
})
DayOfWeek._set_binding_type(type.EnumType(
    'com.vmware.vcenter.content.registries.day_of_week',
    DayOfWeek))



class Recurrence(Enum):
    """
    The ``Recurrence`` class defines the supported values for how often to run
    a specific operation for a container registry.

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
    No operation is scheduled.

    """
    DAILY = None
    """
    An operation occurs on a daily basis.

    """
    WEEKLY = None
    """
    An operation occurs on a weekly basis.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`Recurrence` instance.
        """
        Enum.__init__(string)

Recurrence._set_values({
    'NONE': Recurrence('NONE'),
    'DAILY': Recurrence('DAILY'),
    'WEEKLY': Recurrence('WEEKLY'),
})
Recurrence._set_binding_type(type.EnumType(
    'com.vmware.vcenter.content.registries.recurrence',
    Recurrence))




class Harbor(VapiInterface):
    """
    The ``Harbor`` class provides methods to manage the lifecycle of an
    integrated Harbor container registry in vCenter.

    .. deprecated:: vSphere API 8.0.1.00200
        Use com.vmware.vcenter.namespace_management.SupervisorServices and
        com.vmware.vcenter.namespace_management.supervisor_services.ClusterSupervisorServices
        instead to register and install a `Harbor <https://goharbor.io>`_
        service. See `the Harbor supervisor service document
        <https://www.vmware.com/go/supervisor-service>`_ for more details.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.content.registries.harbor'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        warn('com.vmware.vcenter.content.registries.Harbor is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
        VapiInterface.__init__(self, config, _HarborStub)
        self._VAPI_OPERATION_IDS = {}

    class StorageSpec(VapiStruct):
        """
        The ``Harbor.StorageSpec`` class contains the specification required to
        configure storage associated with a Harbor registry. In this version,
        Harbor registry is created in Kubernetes environment, information in this
        class will result in storage quotas on a Kubernetes namespace.

        .. deprecated:: vSphere API 8.0.1.00200

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     policy=None,
                     limit=None,
                    ):
            """
            :type  policy: :class:`str`
            :param policy: Identifier of the storage policy.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``SpsStorageProfile``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``SpsStorageProfile``.
            :type  limit: :class:`long` or ``None``
            :param limit: The maximum amount of storage (in mebibytes) which can be utilized
                by the registry for this specification.
                If None, a default limit of 204800 mebibytes will be set as the
                registry's storage capacity.
            """
            warn('com.vmware.vcenter.content.registries.Harbor.StorageSpec is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
            self.policy = policy
            self.limit = limit
            VapiStruct.__init__(self)


    StorageSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.content.registries.harbor.storage_spec', {
            'policy': type.IdType(resource_types='SpsStorageProfile'),
            'limit': type.OptionalType(type.IntegerType()),
        },
        StorageSpec,
        False,
        None))


    class StorageInfo(VapiStruct):
        """
        The ``Harbor.StorageInfo`` class contains the detailed information about
        storage used by the Harbor registry.

        .. deprecated:: vSphere API 8.0.1.00200

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     policy=None,
                     capacity=None,
                     used=None,
                    ):
            """
            :type  policy: :class:`str`
            :param policy: Identifier of the storage policy.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``SpsStorageProfile``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``SpsStorageProfile``.
            :type  capacity: :class:`long`
            :param capacity: Total capacity for the registry storage (in mebibytes). This is the
                storage limit set on the Harbor registry. If a storage limit was
                not set on the registry, the default registry capacity - 204800
                mebibytes is used.
            :type  used: :class:`long`
            :param used: Overall storage used by the registry (in mebibytes). This is the
                sum of used storage associated with storage policies configured for
                the registry.
            """
            warn('com.vmware.vcenter.content.registries.Harbor.StorageInfo is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
            self.policy = policy
            self.capacity = capacity
            self.used = used
            VapiStruct.__init__(self)


    StorageInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.content.registries.harbor.storage_info', {
            'policy': type.IdType(resource_types='SpsStorageProfile'),
            'capacity': type.IntegerType(),
            'used': type.IntegerType(),
        },
        StorageInfo,
        False,
        None))


    class GarbageCollection(VapiStruct):
        """
        The ``Harbor.GarbageCollection`` class contains garbage collection
        configuration for the Harbor registry.

        .. deprecated:: vSphere API 8.0.1.00200

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'WEEKLY' : [('day_of_week', True), ('hour', True), ('minute', True)],
                    'DAILY' : [('hour', True), ('minute', True)],
                    'NONE' : [],
                }
            ),
        ]



        def __init__(self,
                     type=None,
                     day_of_week=None,
                     hour=None,
                     minute=None,
                    ):
            """
            :type  type: :class:`Recurrence`
            :param type: Frequency of garbage collection.
            :type  day_of_week: :class:`DayOfWeek`
            :param day_of_week: Day of the week when garbage collection should run.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Recurrence.WEEKLY`.
            :type  hour: :class:`long`
            :param hour: Hour at which garbage collection should run.
                This attribute is optional and it is only relevant when the value
                of ``type`` is one of :attr:`Recurrence.DAILY` or
                :attr:`Recurrence.WEEKLY`.
            :type  minute: :class:`long`
            :param minute: Minute at which garbage collection should run.
                This attribute is optional and it is only relevant when the value
                of ``type`` is one of :attr:`Recurrence.DAILY` or
                :attr:`Recurrence.WEEKLY`.
            """
            warn('com.vmware.vcenter.content.registries.Harbor.GarbageCollection is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
            self.type = type
            self.day_of_week = day_of_week
            self.hour = hour
            self.minute = minute
            VapiStruct.__init__(self)


    GarbageCollection._set_binding_type(type.StructType(
        'com.vmware.vcenter.content.registries.harbor.garbage_collection', {
            'type': type.ReferenceType(__name__, 'Recurrence'),
            'day_of_week': type.OptionalType(type.ReferenceType(__name__, 'DayOfWeek')),
            'hour': type.OptionalType(type.IntegerType()),
            'minute': type.OptionalType(type.IntegerType()),
        },
        GarbageCollection,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Harbor.CreateSpec`` class contains the specification required to
        create a Harbor registry.

        .. deprecated:: vSphere API 8.0.1.00200

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     garbage_collection=None,
                     storage=None,
                    ):
            """
            :type  cluster: :class:`str` or ``None``
            :param cluster: Identifier of the cluster hosting the registry.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If None, registry will not be created on a specified cluster. This
                is required in current version, since Harbor can only be created on
                a cluster with Kubernetes enabled.
            :type  garbage_collection: :class:`Harbor.GarbageCollection` or ``None``
            :param garbage_collection: Garbage collection configuration for the Harbor registry.
                If None, a default configuration is set, Recurrence#WEEKLY,
                DayOfWeek#SATURDAY, GarbageCollection#hour is 2,
                GarbageCollection#minute is 0.
            :type  storage: :class:`list` of :class:`Harbor.StorageSpec`
            :param storage: Storage associated with the Harbor registry. The list contains only
                one storage backing in this version.
            """
            warn('com.vmware.vcenter.content.registries.Harbor.CreateSpec is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
            self.cluster = cluster
            self.garbage_collection = garbage_collection
            self.storage = storage
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.content.registries.harbor.create_spec', {
            'cluster': type.OptionalType(type.IdType()),
            'garbage_collection': type.OptionalType(type.ReferenceType(__name__, 'Harbor.GarbageCollection')),
            'storage': type.ListType(type.ReferenceType(__name__, 'Harbor.StorageSpec')),
        },
        CreateSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Harbor.Summary`` class contains basic information about a running
        Harbor registry.

        .. deprecated:: vSphere API 8.0.1.00200

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     registry=None,
                     version=None,
                     ui_access_url=None,
                    ):
            """
            :type  cluster: :class:`str` or ``None``
            :param cluster: Identifier of the cluster.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If None, container registry is not created on the cluster specified
                by :attr:`Harbor.CreateSpec.cluster`.
            :type  registry: :class:`str`
            :param registry: Identifier of the registry.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.content.Registry``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.content.Registry``.
            :type  version: :class:`str`
            :param version: Version of the registry.
            :type  ui_access_url: :class:`str`
            :param ui_access_url: URL to access the UI of the registry.
            """
            warn('com.vmware.vcenter.content.registries.Harbor.Summary is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
            self.cluster = cluster
            self.registry = registry
            self.version = version
            self.ui_access_url = ui_access_url
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.content.registries.harbor.summary', {
            'cluster': type.OptionalType(type.IdType()),
            'registry': type.IdType(resource_types='com.vmware.vcenter.content.Registry'),
            'version': type.StringType(),
            'ui_access_url': type.URIType(),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Harbor.Info`` class contains detailed information about a running
        Harbor registry.

        .. deprecated:: vSphere API 8.0.1.00200

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     namespace=None,
                     version=None,
                     creation_time=None,
                     ui_access_url=None,
                     cert_chain=None,
                     garbage_collection=None,
                     storage=None,
                     health=None,
                    ):
            """
            :type  cluster: :class:`str` or ``None``
            :param cluster: Identifier of the cluster.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If None, container registry is not created on the cluster specified
                by :attr:`Harbor.CreateSpec.cluster`.
            :type  namespace: :class:`str` or ``None``
            :param namespace: Identifier of the Harbor namespace in case it is created in a
                Kubernetes environment.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``NamespaceInstance``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``NamespaceInstance``.
                If None, no Kubernetes namespace is created for the Harbor.
            :type  version: :class:`str`
            :param version: Version of the registry.
            :type  creation_time: :class:`datetime.datetime`
            :param creation_time: The date and time when the harbor registry was created.
            :type  ui_access_url: :class:`str`
            :param ui_access_url: URL to access the UI of the registry.
            :type  cert_chain: :class:`list` of :class:`str`
            :param cert_chain: Harbor certificate chain in base64 format.
            :type  garbage_collection: :class:`Harbor.GarbageCollection`
            :param garbage_collection: Garbage collection information for the registry.
            :type  storage: :class:`list` of :class:`Harbor.StorageInfo`
            :param storage: Storage information associated with the registry.
            :type  health: :class:`Health.Info`
            :param health: Health status of the container registry.
            """
            warn('com.vmware.vcenter.content.registries.Harbor.Info is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
            self.cluster = cluster
            self.namespace = namespace
            self.version = version
            self.creation_time = creation_time
            self.ui_access_url = ui_access_url
            self.cert_chain = cert_chain
            self.garbage_collection = garbage_collection
            self.storage = storage
            self.health = health
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.content.registries.harbor.info', {
            'cluster': type.OptionalType(type.IdType()),
            'namespace': type.OptionalType(type.IdType()),
            'version': type.StringType(),
            'creation_time': type.DateTimeType(),
            'ui_access_url': type.URIType(),
            'cert_chain': type.ListType(type.StringType()),
            'garbage_collection': type.ReferenceType(__name__, 'Harbor.GarbageCollection'),
            'storage': type.ListType(type.ReferenceType(__name__, 'Harbor.StorageInfo')),
            'health': type.ReferenceType(__name__, 'Health.Info'),
        },
        Info,
        False,
        None))



    def create(self,
               spec,
               client_token=None,
               ):
        """
        Creates a Harbor registry in the cluster.

        .. deprecated:: vSphere API 8.0.1.00200

        :type  client_token: :class:`str` or ``None``
        :param client_token: A unique token generated on the client for each creation request.
            The token should be a universally unique identifier (UUID), for
            example: ``b8a2a2e3-2314-43cd-a871-6ede0f429751``. This token can
            be used to guarantee idempotent creation.
            If not specified, creation is not idempotent.
        :type  spec: :class:`Harbor.CreateSpec`
        :param spec: Specification for creating the Harbor registry.
        :rtype: :class:`str`
        :return: Identifier of the deployed registry.
            The return value will be an identifier for the resource type:
            ``com.vmware.vcenter.content.Registry``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a Harbor already exists in the associated cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if resources/objects could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if :attr:`Harbor.CreateSpec.cluster` does not have vSphere
            namespace enabled.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``spec`` contains any errors.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have ContentLibrary.ManageRegistry and/or
            CertificateAuthority.Manage privilege, or user does not have
            ContentLibrary.ManageClusterRegistryResource privilege on
            :attr:`Harbor.CreateSpec.cluster`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``ClusterComputeResource`` referenced by the
              attribute :attr:`Harbor.CreateSpec.cluster` requires
              ``System.Read``.
            * The resource ``SpsStorageProfile`` referenced by the attribute
              :attr:`Harbor.StorageSpec.policy` requires ``System.Read``.
        """
        warn('com.vmware.vcenter.content.registries.Harbor.create is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
        return self._invoke('create',
                            {
                            'client_token': client_token,
                            'spec': spec,
                            })

    def delete(self,
               registry,
               ):
        """
        Delete the Harbor registry in the cluster. All Harbor projects,
        repositories and images will be deleted upon Harbor registry deletion.

        .. deprecated:: vSphere API 8.0.1.00200

        :type  registry: :class:`str`
        :param registry: Identifier of the registry.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.content.Registry``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if a registry specified by ``registry`` could not be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have ContentLibrary.ManageRegistry privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.vcenter.content.Registry`` referenced
              by the parameter ``registry`` requires ``System.Read``.
        """
        warn('com.vmware.vcenter.content.registries.Harbor.delete is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
        return self._invoke('delete',
                            {
                            'registry': registry,
                            })

    def get(self,
            registry,
            ):
        """
        Get detailed information of the Harbor registry.

        .. deprecated:: vSphere API 8.0.1.00200

        :type  registry: :class:`str`
        :param registry: Identifier of the registry.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.content.Registry``.
        :rtype: :class:`Harbor.Info`
        :return: Information about the registry.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if a Harbor registry specified by ``registry`` could not be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.vcenter.content.Registry`` referenced
              by the parameter ``registry`` requires ``System.Read``.
        """
        warn('com.vmware.vcenter.content.registries.Harbor.get is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
        return self._invoke('get',
                            {
                            'registry': registry,
                            })

    def list(self):
        """
        Returns basic information of all Harbor registries.

        .. deprecated:: vSphere API 8.0.1.00200


        :rtype: :class:`list` of :class:`Harbor.Summary`
        :return: The list of basic information of all Harbor registries.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
        """
        warn('com.vmware.vcenter.content.registries.Harbor.list is deprecated as of release vSphere API 8.0.1.00200.', DeprecationWarning)
        return self._invoke('list', None)
class Health(VapiInterface):
    """
    The ``Health`` class provides methods to retrieve health status for a
    container registry.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.content.registries.health'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HealthStub)
        self._VAPI_OPERATION_IDS = {}

    class Status(Enum):
        """
        The ``Health.Status`` class describes the status of the container registry.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        STARTING = None
        """
        Container registry is starting.

        """
        RUNNING = None
        """
        Container registry is running.

        """
        WARNING = None
        """
        Container registry is running with some warning, for example, storage
        reaches the threshold configuration.

        """
        ERROR = None
        """
        Container registry failed to start or stopped with fatal error.

        """
        DELETING = None
        """
        Container registry is being deleted.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Status` instance.
            """
            Enum.__init__(string)

    Status._set_values({
        'STARTING': Status('STARTING'),
        'RUNNING': Status('RUNNING'),
        'WARNING': Status('WARNING'),
        'ERROR': Status('ERROR'),
        'DELETING': Status('DELETING'),
    })
    Status._set_binding_type(type.EnumType(
        'com.vmware.vcenter.content.registries.health.status',
        Status))


    class Info(VapiStruct):
        """
        The ``Health.Info`` class contains health information about a container
        registry.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'WARNING' : [('details', True)],
                    'ERROR' : [('details', True)],
                    'STARTING' : [],
                    'RUNNING' : [],
                    'DELETING' : [],
                }
            ),
        ]



        def __init__(self,
                     status=None,
                     details=None,
                    ):
            """
            :type  status: :class:`Health.Status`
            :param status: Container registry status.
            :type  details: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param details: Details about the status.
                If None, message details are not required for taking actions.
            """
            self.status = status
            self.details = details
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.content.registries.health.info', {
            'status': type.ReferenceType(__name__, 'Health.Status'),
            'details': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Info,
        False,
        None))



    def get(self,
            registry,
            ):
        """
        Returns the health information of a container registry in the vCenter.

        :type  registry: :class:`str`
        :param registry: Identifier of the registry.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.content.Registry``.
        :rtype: :class:`Health.Info`
        :return: Health information of the registry.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the registry does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not a member of the Administrators
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
            * The resource ``com.vmware.vcenter.content.Registry`` referenced
              by the parameter ``registry`` requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'registry': registry,
                            })
class _HarborStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'client_token': type.OptionalType(type.StringType()),
            'spec': type.ReferenceType(__name__, 'Harbor.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/content/registries/harbor',
            path_variables={
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'registry': type.IdType(resource_types='com.vmware.vcenter.content.Registry'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/content/registries/harbor/{registry}',
            path_variables={
                'registry': 'registry',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'registry': type.IdType(resource_types='com.vmware.vcenter.content.Registry'),
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

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/content/registries/harbor/{registry}',
            path_variables={
                'registry': 'registry',
            },
             header_parameters={
               },
            query_parameters={
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
            url_template='/vcenter/content/registries/harbor',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.vcenter.content.Registry'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Harbor.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Harbor.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.content.registries.harbor',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _HealthStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'registry': type.IdType(resource_types='com.vmware.vcenter.content.Registry'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/content/registries/{registry}/health',
            path_variables={
                'registry': 'registry',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Health.Info'),
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
            self, iface_name='com.vmware.vcenter.content.registries.health',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Harbor': Harbor,
        'Health': Health,
        'harbor': 'com.vmware.vcenter.content.registries.harbor_client.StubFactory',
    }

