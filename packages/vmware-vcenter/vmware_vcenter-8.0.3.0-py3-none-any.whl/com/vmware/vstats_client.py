# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vstats.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vstats_client`` component provides API classes and types used
in the vStats service.

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

class QueryPredicate(Enum):
    """
    The ``QueryPredicate`` enum describes how to query an id present in a
    ``RsrcId``. **Warning:** This enumeration is available as Technology
    Preview. These are early access APIs provided to test, automate and provide
    feedback on the feature. Since this can change based on feedback, VMware
    does not guarantee backwards compatibility and recommends against using
    them in production environments. Some Technology Preview APIs might only be
    applicable to specific environments.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    EQUAL = None
    """
    Matching id-s by equality. **Warning:** This class attribute is available
    as Technology Preview. These are early access APIs provided to test,
    automate and provide feedback on the feature. Since this can change based
    on feedback, VMware does not guarantee backwards compatibility and
    recommends against using them in production environments. Some Technology
    Preview APIs might only be applicable to specific environments.

    """
    ALL = None
    """
    Matching all available id-s. **Warning:** This class attribute is available
    as Technology Preview. These are early access APIs provided to test,
    automate and provide feedback on the feature. Since this can change based
    on feedback, VMware does not guarantee backwards compatibility and
    recommends against using them in production environments. Some Technology
    Preview APIs might only be applicable to specific environments.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`QueryPredicate` instance.
        """
        Enum.__init__(string)

QueryPredicate._set_values({
    'EQUAL': QueryPredicate('EQUAL'),
    'ALL': QueryPredicate('ALL'),
})
QueryPredicate._set_binding_type(type.EnumType(
    'com.vmware.vstats.query_predicate',
    QueryPredicate))




class CidMid(VapiStruct):
    """
    The ``CidMid`` class is used to designate a counter. It contains a counter
    id that identifies the semantical counter. There is optional metadata
    identifier that identifies the particular generation of the counter. When
    counter metadata is not designated vStats will use a default for the
    counter metadata. **Warning:** This class is available as Technology
    Preview. These are early access APIs provided to test, automate and provide
    feedback on the feature. Since this can change based on feedback, VMware
    does not guarantee backwards compatibility and recommends against using
    them in production environments. Some Technology Preview APIs might only be
    applicable to specific environments.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 cid=None,
                 mid=None,
                ):
        """
        :type  cid: :class:`str`
        :param cid: Counter Id. CID is a string with rather strong semantic consistency
            across deployments and versions. If two CIDs are identical it
            implies the corresponding counters are the same. **Warning:** This
            attribute is available as Technology Preview. These are early
            access APIs provided to test, automate and provide feedback on the
            feature. Since this can change based on feedback, VMware does not
            guarantee backwards compatibility and recommends against using them
            in production environments. Some Technology Preview APIs might only
            be applicable to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vstats.model.Counter``. When methods return a value of
            this class as a return value, the attribute will be an identifier
            for the resource type: ``com.vmware.vstats.model.Counter``.
        :type  mid: :class:`str` or ``None``
        :param mid: MID is a 64-bit integer with strong consistency. Given a particular
            CID=cid, if two MIDs are the same, then the corresponding
            counter-metadata objects are same. **Warning:** This attribute is
            available as Technology Preview. These are early access APIs
            provided to test, automate and provide feedback on the feature.
            Since this can change based on feedback, VMware does not guarantee
            backwards compatibility and recommends against using them in
            production environments. Some Technology Preview APIs might only be
            applicable to specific environments.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vstats.model.CounterMetadata``. When methods return a
            value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.vstats.model.CounterMetadata``.
            When this attribute is None vStats will use default for the counter
            metadata as obtained from the provider.
        """
        self.cid = cid
        self.mid = mid
        VapiStruct.__init__(self)


CidMid._set_binding_type(type.StructType(
    'com.vmware.vstats.cid_mid', {
        'cid': type.IdType(resource_types='com.vmware.vstats.model.Counter'),
        'mid': type.OptionalType(type.IdType()),
    },
    CidMid,
    False,
    None))



class RsrcId(VapiStruct):
    """
    The ``RsrcId`` class specifies identification of a resource to be monitored
    by an acquisition specification record. **Warning:** This class is
    available as Technology Preview. These are early access APIs provided to
    test, automate and provide feedback on the feature. Since this can change
    based on feedback, VMware does not guarantee backwards compatibility and
    recommends against using them in production environments. Some Technology
    Preview APIs might only be applicable to specific environments.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 key=None,
                 type=None,
                 id_value=None,
                 predicate=None,
                 scheme=None,
                ):
        """
        :type  key: :class:`str` or ``None``
        :param key: Key relates to the corresponding ResourceIdDefinition of the
            related resource address schema. **Warning:** This attribute is
            available as Technology Preview. These are early access APIs
            provided to test, automate and provide feedback on the feature.
            Since this can change based on feedback, VMware does not guarantee
            backwards compatibility and recommends against using them in
            production environments. Some Technology Preview APIs might only be
            applicable to specific environments.
            When this attribute is None, type attribute will be used.
        :type  type: :class:`str` or ``None``
        :param type: Type of the resource identified by the Resource Id. **Warning:**
            This attribute is available as Technology Preview. These are early
            access APIs provided to test, automate and provide feedback on the
            feature. Since this can change based on feedback, VMware does not
            guarantee backwards compatibility and recommends against using them
            in production environments. Some Technology Preview APIs might only
            be applicable to specific environments.
            When this attribute is None, in current version the api will throw
            InvalidArgument error. To be made optional in future.
        :type  id_value: :class:`str`
        :param id_value: The id value binding the related resource id definition.
            **Warning:** This attribute is available as Technology Preview.
            These are early access APIs provided to test, automate and provide
            feedback on the feature. Since this can change based on feedback,
            VMware does not guarantee backwards compatibility and recommends
            against using them in production environments. Some Technology
            Preview APIs might only be applicable to specific environments.
        :type  predicate: :class:`QueryPredicate` or ``None``
        :param predicate: Predicate to use to match resource Ids. **Warning:** This attribute
            is available as Technology Preview. These are early access APIs
            provided to test, automate and provide feedback on the feature.
            Since this can change based on feedback, VMware does not guarantee
            backwards compatibility and recommends against using them in
            production environments. Some Technology Preview APIs might only be
            applicable to specific environments.
            When this attribute is None, default predicate is EQUAL.
        :type  scheme: :class:`str` or ``None``
        :param scheme: An optional designation of the scheme. **Warning:** This attribute
            is available as Technology Preview. These are early access APIs
            provided to test, automate and provide feedback on the feature.
            Since this can change based on feedback, VMware does not guarantee
            backwards compatibility and recommends against using them in
            production environments. Some Technology Preview APIs might only be
            applicable to specific environments.
            When this attribute is None, default scheme is moid (ManagedObject
            Identifier).
        """
        self.key = key
        self.type = type
        self.id_value = id_value
        self.predicate = predicate
        self.scheme = scheme
        VapiStruct.__init__(self)


RsrcId._set_binding_type(type.StructType(
    'com.vmware.vstats.rsrc_id', {
        'key': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
        'id_value': type.StringType(),
        'predicate': type.OptionalType(type.ReferenceType(__name__, 'QueryPredicate')),
        'scheme': type.OptionalType(type.StringType()),
    },
    RsrcId,
    False,
    None))



class UserInfo(VapiStruct):
    """
    The ``UserInfo`` class contains human legible, localizable description,
    used for VMware provided objects. **Warning:** This class is available as
    Technology Preview. These are early access APIs provided to test, automate
    and provide feedback on the feature. Since this can change based on
    feedback, VMware does not guarantee backwards compatibility and recommends
    against using them in production environments. Some Technology Preview APIs
    might only be applicable to specific environments.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 label=None,
                 description=None,
                ):
        """
        :type  label: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param label: Short label. **Warning:** This attribute is available as Technology
            Preview. These are early access APIs provided to test, automate and
            provide feedback on the feature. Since this can change based on
            feedback, VMware does not guarantee backwards compatibility and
            recommends against using them in production environments. Some
            Technology Preview APIs might only be applicable to specific
            environments.
        :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param description: Detailed description of the object. **Warning:** This attribute is
            available as Technology Preview. These are early access APIs
            provided to test, automate and provide feedback on the feature.
            Since this can change based on feedback, VMware does not guarantee
            backwards compatibility and recommends against using them in
            production environments. Some Technology Preview APIs might only be
            applicable to specific environments.
        """
        self.label = label
        self.description = description
        VapiStruct.__init__(self)


UserInfo._set_binding_type(type.StructType(
    'com.vmware.vstats.user_info', {
        'label': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
    },
    UserInfo,
    False,
    None))



class AcqSpecs(VapiInterface):
    """
    The ``AcqSpecs`` class provides methods to perform acquisition
    specification related operations. An acquisition specification defines the
    statistical data that should be collected at desired sampling rates from
    the underlying providers. It designates the resources and their counters
    which should be sampled, and a desired sampling rate. **Warning:** This
    class is available as Technology Preview. These are early access APIs
    provided to test, automate and provide feedback on the feature. Since this
    can change based on feedback, VMware does not guarantee backwards
    compatibility and recommends against using them in production environments.
    Some Technology Preview APIs might only be applicable to specific
    environments.
    """
    RESOURCE_TYPE = "com.vmware.vstats.model.AcqSpec"
    """
    Resource type for acquisition specifications. **Warning:** This class attribute
    is available as Technology Preview. These are early access APIs provided to
    test, automate and provide feedback on the feature. Since this can change based
    on feedback, VMware does not guarantee backwards compatibility and recommends
    against using them in production environments. Some Technology Preview APIs
    might only be applicable to specific environments.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.acq_specs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AcqSpecsStub)
        self._VAPI_OPERATION_IDS = {}

    class Status(Enum):
        """
        Describes the status of an Acquisition Specification. **Warning:** This
        enumeration is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

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
        The acquisition specification is enabled when the stats data collection is
        going on. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        DISABLED = None
        """
        The acquisition specification is disabled when the stats data collection is
        paused. This can happen when the counters are enabled or disabled
        dynamically on providers. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        EXPIRED = None
        """
        The acquisition specification is expired when the expiration time is
        exceeded. There is no data collection in that case. **Warning:** This class
        attribute is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Status` instance.
            """
            Enum.__init__(string)

    Status._set_values({
        'ENABLED': Status('ENABLED'),
        'DISABLED': Status('DISABLED'),
        'EXPIRED': Status('EXPIRED'),
    })
    Status._set_binding_type(type.EnumType(
        'com.vmware.vstats.acq_specs.status',
        Status))


    class CounterSpec(VapiStruct):
        """
        The ``AcqSpecs.CounterSpec`` class designates a counter or counter set in
        an acquisition specification. **Warning:** This class is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cid_mid=None,
                     set_id=None,
                    ):
            """
            :type  cid_mid: :class:`CidMid` or ``None``
            :param cid_mid: Counter and optional meatadata identifier. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                When None the ``setId`` field will be used.
            :type  set_id: :class:`str` or ``None``
            :param set_id: Counter set identifier. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.CounterSet``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.CounterSet``.
                When None the ``cidMid`` field will be used.
            """
            self.cid_mid = cid_mid
            self.set_id = set_id
            VapiStruct.__init__(self)


    CounterSpec._set_binding_type(type.StructType(
        'com.vmware.vstats.acq_specs.counter_spec', {
            'cid_mid': type.OptionalType(type.ReferenceType(__name__, 'CidMid')),
            'set_id': type.OptionalType(type.IdType()),
        },
        CounterSpec,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``AcqSpecs.CreateSpec`` class contains information for a new data
        acquisition specification. **Warning:** This class is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     counters=None,
                     resources=None,
                     interval=None,
                     expiration=None,
                     memo_=None,
                    ):
            """
            :type  counters: :class:`AcqSpecs.CounterSpec`
            :param counters: Designates the counter(s) to be sampled. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
            :type  resources: :class:`list` of :class:`RsrcId`
            :param resources: A set of resource identifiers representing a single resource to be
                monitored. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
            :type  interval: :class:`long` or ``None``
            :param interval: Desired sampling rate in seconds. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                If None default of 10s will be used.
            :type  expiration: :class:`long` or ``None``
            :param expiration: Expiration time for this acquisition specification in Unix UTC
                number of seconds (since epoch). **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                When this attribute is None or 0, default expiration duration is
                100 minutes.
            :type  memo_: :class:`str` or ``None``
            :param memo_: Consumer provided text about this acquisition specification.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
                If None default empty string will be used.
            """
            self.counters = counters
            self.resources = resources
            self.interval = interval
            self.expiration = expiration
            self.memo_ = memo_
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vstats.acq_specs.create_spec', {
            'counters': type.ReferenceType(__name__, 'AcqSpecs.CounterSpec'),
            'resources': type.ListType(type.ReferenceType(__name__, 'RsrcId')),
            'interval': type.OptionalType(type.IntegerType()),
            'expiration': type.OptionalType(type.IntegerType()),
            'memo_': type.OptionalType(type.StringType()),
        },
        CreateSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``AcqSpecs.Info`` class is the information about an acquisition
        specification. It specifies the statistical data that should be collected
        at desired sampling rates. It designates the resources and their counters
        which should be sampled, and a desired sampling rate. **Warning:** This
        class is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     counters=None,
                     resources=None,
                     interval=None,
                     expiration=None,
                     memo_=None,
                     status=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Acquisition specification identifier. **Warning:** This attribute
                is available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.AcqSpec``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.AcqSpec``.
            :type  counters: :class:`AcqSpecs.CounterSpec`
            :param counters: Designates the counter(s) to be sampled. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
            :type  resources: :class:`list` of :class:`RsrcId`
            :param resources: A set of resource identifiers representing a single resource to be
                monitored. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
            :type  interval: :class:`long` or ``None``
            :param interval: Desired sampling rate in seconds. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                When this attribute is None, default interval is 10 seconds.
            :type  expiration: :class:`long` or ``None``
            :param expiration: Expiration time for this acquisition specification represented as
                Unix UTC number of seconds (since epoch). **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                When this attribute is None or 0, default expiration duration is
                100 minutes.
            :type  memo_: :class:`str`
            :param memo_: Consumer provided text about this Acquisition Specification.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
            :type  status: :class:`AcqSpecs.Status`
            :param status: Acquisition Specification status. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
            """
            self.id = id
            self.counters = counters
            self.resources = resources
            self.interval = interval
            self.expiration = expiration
            self.memo_ = memo_
            self.status = status
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vstats.acq_specs.info', {
            'id': type.IdType(resource_types='com.vmware.vstats.model.AcqSpec'),
            'counters': type.ReferenceType(__name__, 'AcqSpecs.CounterSpec'),
            'resources': type.ListType(type.ReferenceType(__name__, 'RsrcId')),
            'interval': type.OptionalType(type.IntegerType()),
            'expiration': type.OptionalType(type.IntegerType()),
            'memo_': type.StringType(),
            'status': type.ReferenceType(__name__, 'AcqSpecs.Status'),
        },
        Info,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``AcqSpecs.ListResult`` class contains attributes used to return the
        acquisition specifications. **Warning:** This class is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     acq_specs=None,
                     next=None,
                    ):
            """
            :type  acq_specs: :class:`list` of :class:`AcqSpecs.Info`
            :param acq_specs: List of acquisition specifications received. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
            :type  next: :class:`str` or ``None``
            :param next: The ``next`` attribute is a token used to retrieve paged data for
                larger result sets. This is opaque token generated by the server.
                It is to be sent in the :attr:`AcqSpecs.FilterSpec.page` attribute
                to issue a subsequent call to the list method for retrieving
                results that did not fit the current page. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                :class:`set` when there are more results to retrieve.
            """
            self.acq_specs = acq_specs
            self.next = next
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vstats.acq_specs.list_result', {
            'acq_specs': type.ListType(type.ReferenceType(__name__, 'AcqSpecs.Info')),
            'next': type.OptionalType(type.StringType()),
        },
        ListResult,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``AcqSpecs.FilterSpec`` class contains attributes used to filter the
        results when listing acquisition specifications. **Warning:** This class is
        available as Technology Preview. These are early access APIs provided to
        test, automate and provide feedback on the feature. Since this can change
        based on feedback, VMware does not guarantee backwards compatibility and
        recommends against using them in production environments. Some Technology
        Preview APIs might only be applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     page=None,
                    ):
            """
            :type  page: :class:`str` or ``None``
            :param page: Used to retrieve paged data for larger result sets. The value of
                this token is generated by server and returned as ``next``
                attribute in the result of ``list`` methods. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                None the first page of results will be returned.
            """
            self.page = page
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vstats.acq_specs.filter_spec', {
            'page': type.OptionalType(type.StringType()),
        },
        FilterSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``AcqSpecs.UpdateSpec`` class contains attributes that can be updated
        in an acquisition specification. **Warning:** This class is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     counters=None,
                     resources=None,
                     interval=None,
                     expiration=None,
                     memo_=None,
                    ):
            """
            :type  counters: :class:`AcqSpecs.CounterSpec` or ``None``
            :param counters: Designates the counter(s) to be sampled. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                If None, the value is unchanged.
            :type  resources: :class:`list` of :class:`RsrcId` or ``None``
            :param resources: A set of resource identifiers representing a single resource to be
                monitored. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                If None, the value is unchanged.
            :type  interval: :class:`long` or ``None``
            :param interval: Desired sampling rate in seconds. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                If None, the value is unchanged.
            :type  expiration: :class:`long` or ``None``
            :param expiration: Expiration time for this acquisition specification in Unix UTC
                number of seconds (since epoch). When this attribute is 0, the
                default expiration duration is 100 minutes. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                If None, the value is unchanged.
            :type  memo_: :class:`str` or ``None``
            :param memo_: Consumer provided text about this Acquisition Specification.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
                If None, the value is unchanged.
            """
            self.counters = counters
            self.resources = resources
            self.interval = interval
            self.expiration = expiration
            self.memo_ = memo_
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vstats.acq_specs.update_spec', {
            'counters': type.OptionalType(type.ReferenceType(__name__, 'AcqSpecs.CounterSpec')),
            'resources': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'RsrcId'))),
            'interval': type.OptionalType(type.IntegerType()),
            'expiration': type.OptionalType(type.IntegerType()),
            'memo_': type.OptionalType(type.StringType()),
        },
        UpdateSpec,
        False,
        None))



    def create(self,
               acq_spec,
               ):
        """
        Create a new acquisition specification record. **Warning:** This method
        is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since
        this can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  acq_spec: :class:`AcqSpecs.CreateSpec`
        :param acq_spec: Specification for the acquisition of stats data.
        :rtype: :class:`str`
        :return: Identifier of the newly created acquisition specification.
            The return value will be an identifier for the resource type:
            ``com.vmware.vstats.model.AcqSpec``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``acq_spec`` contain any errors.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('create',
                            {
                            'acq_spec': acq_spec,
                            })

    def delete(self,
               id,
               ):
        """
        Delete an acquisition specification. **Warning:** This method is
        available as Technology Preview. These are early access APIs provided
        to test, automate and provide feedback on the feature. Since this can
        change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  id: :class:`str`
        :param id: Acquisition specification ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.AcqSpec``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``id`` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if acquisition specification could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('delete',
                            {
                            'id': id,
                            })

    def list(self,
             filter=None,
             ):
        """
        Returns information about all acquisition specifications. **Warning:**
        This method is available as Technology Preview. These are early access
        APIs provided to test, automate and provide feedback on the feature.
        Since this can change based on feedback, VMware does not guarantee
        backwards compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  filter: :class:`AcqSpecs.FilterSpec` or ``None``
        :param filter: Criteria for selecting records to return.
            When :class:`set` filtering will be applied to the result.
        :rtype: :class:`AcqSpecs.ListResult`
        :return: List of acquisition specification records.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def get(self,
            id,
            ):
        """
        Returns information about a specific acquisition specification.
        **Warning:** This method is available as Technology Preview. These are
        early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        :type  id: :class:`str`
        :param id: Acquisition specification ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.AcqSpec``.
        :rtype: :class:`AcqSpecs.Info`
        :return: Information about the desired acquisition specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``id`` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            acquisition specification could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('get',
                            {
                            'id': id,
                            })

    def update(self,
               id,
               acq_spec,
               ):
        """
        Update an existing acquisition specification. **Warning:** This method
        is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since
        this can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  id: :class:`str`
        :param id: Acquisition specification ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.AcqSpec``.
        :type  acq_spec: :class:`AcqSpecs.UpdateSpec`
        :param acq_spec: Updated acquisition specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            acquisition specification could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('update',
                            {
                            'id': id,
                            'acq_spec': acq_spec,
                            })
class CounterMetadata(VapiInterface):
    """
    The ``CounterMetadata`` class provides access to the different historical
    editions of counters. As computing platforms evolve over time the
    measurement units for different characteristics of the systems change. As
    such changes occur, counters will receive different editions reflected in a
    new metadata record. For example computer memory had changes from kilobytes
    through megabytes into gigabytes. **Warning:** This class is available as
    Technology Preview. These are early access APIs provided to test, automate
    and provide feedback on the feature. Since this can change based on
    feedback, VMware does not guarantee backwards compatibility and recommends
    against using them in production environments. Some Technology Preview APIs
    might only be applicable to specific environments.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.counter_metadata'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CounterMetadataStub)
        self._VAPI_OPERATION_IDS = {}

    class CounterEditionStatus(Enum):
        """
        Counter metadata status. **Warning:** This enumeration is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DEFAULT = None
        """
        The counter edition is current and is the default. **Warning:** This class
        attribute is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        """
        CURRENT = None
        """
        The counter edition is current. This implies a support commitment.
        **Warning:** This class attribute is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        DEPRECATED = None
        """
        The counter edition is deprecated. It will be decommissioned rather soon.
        **Warning:** This class attribute is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        EXPERIMENTAL = None
        """
        The counter edition is experimental. Consumers shouldn't rely on it for the
        long haul. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        REMOVED = None
        """
        The counter edition was removed. **Warning:** This class attribute is
        available as Technology Preview. These are early access APIs provided to
        test, automate and provide feedback on the feature. Since this can change
        based on feedback, VMware does not guarantee backwards compatibility and
        recommends against using them in production environments. Some Technology
        Preview APIs might only be applicable to specific environments.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`CounterEditionStatus` instance.
            """
            Enum.__init__(string)

    CounterEditionStatus._set_values({
        'DEFAULT': CounterEditionStatus('DEFAULT'),
        'CURRENT': CounterEditionStatus('CURRENT'),
        'DEPRECATED': CounterEditionStatus('DEPRECATED'),
        'EXPERIMENTAL': CounterEditionStatus('EXPERIMENTAL'),
        'REMOVED': CounterEditionStatus('REMOVED'),
    })
    CounterEditionStatus._set_binding_type(type.EnumType(
        'com.vmware.vstats.counter_metadata.counter_edition_status',
        CounterEditionStatus))


    class SampleType(Enum):
        """
        Type of the sampled data. **Warning:** This enumeration is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        RAW = None
        """
        Raw samples. The value unprocessed as-is sampled. **Warning:** This class
        attribute is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        """
        ABSOLUTE = None
        """
        Absolute value samples. Represents an actual value of the counter.
        **Warning:** This class attribute is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        FRACTION = None
        """
        Fraction samples. Implies range from 0.00 to 1.00. **Warning:** This class
        attribute is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        """
        RATE = None
        """
        Rate samples. Represents a value that has been normalized over the time
        period. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        DELTA = None
        """
        Delta samples. Represents an amount of change for the counter between the
        current time-stamp and the last time-stamp when the counter was sampled.
        **Warning:** This class attribute is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        LOGN = None
        """
        Log(n) samples. A natural logarithm of the value. **Warning:** This class
        attribute is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SampleType` instance.
            """
            Enum.__init__(string)

    SampleType._set_values({
        'RAW': SampleType('RAW'),
        'ABSOLUTE': SampleType('ABSOLUTE'),
        'FRACTION': SampleType('FRACTION'),
        'RATE': SampleType('RATE'),
        'DELTA': SampleType('DELTA'),
        'LOGN': SampleType('LOGN'),
    })
    SampleType._set_binding_type(type.EnumType(
        'com.vmware.vstats.counter_metadata.sample_type',
        SampleType))


    class MetricUnits(Enum):
        """
        Unit used by a metric. **Warning:** This enumeration is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        PERCENT = None
        """
        Percent. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        NUMBER = None
        """
        Number. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        SECOND = None
        """
        Second. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        HERTZ = None
        """
        Hertz. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        METER = None
        """
        Meter. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        METERSPERSECOND = None
        """
        Meters per second. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        METERSPERSECONDSQUARED = None
        """
        Meters per second squared. **Warning:** This class attribute is available
        as Technology Preview. These are early access APIs provided to test,
        automate and provide feedback on the feature. Since this can change based
        on feedback, VMware does not guarantee backwards compatibility and
        recommends against using them in production environments. Some Technology
        Preview APIs might only be applicable to specific environments.

        """
        BYTE = None
        """
        Byte. **Warning:** This class attribute is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        BIT = None
        """
        Bit. **Warning:** This class attribute is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        BYTESPERSECOND = None
        """
        Bytes per second. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        BITSPERSECOND = None
        """
        Bits per second. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        KILOGRAM = None
        """
        Kilogram. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        GRAM = None
        """
        Gram. **Warning:** This class attribute is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        CELSIUS = None
        """
        Celsius. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        KELVIN = None
        """
        Kelvin. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        JOULE = None
        """
        Joule. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        WATT = None
        """
        Watt. **Warning:** This class attribute is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        VOLT = None
        """
        Volt. **Warning:** This class attribute is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        AMPERE = None
        """
        Ampere. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        VOLTAMPERE = None
        """
        Volt Ampere. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        CANDELA = None
        """
        Candela. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        MOLE = None
        """
        Mole. **Warning:** This class attribute is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`MetricUnits` instance.
            """
            Enum.__init__(string)

    MetricUnits._set_values({
        'PERCENT': MetricUnits('PERCENT'),
        'NUMBER': MetricUnits('NUMBER'),
        'SECOND': MetricUnits('SECOND'),
        'HERTZ': MetricUnits('HERTZ'),
        'METER': MetricUnits('METER'),
        'METERSPERSECOND': MetricUnits('METERSPERSECOND'),
        'METERSPERSECONDSQUARED': MetricUnits('METERSPERSECONDSQUARED'),
        'BYTE': MetricUnits('BYTE'),
        'BIT': MetricUnits('BIT'),
        'BYTESPERSECOND': MetricUnits('BYTESPERSECOND'),
        'BITSPERSECOND': MetricUnits('BITSPERSECOND'),
        'KILOGRAM': MetricUnits('KILOGRAM'),
        'GRAM': MetricUnits('GRAM'),
        'CELSIUS': MetricUnits('CELSIUS'),
        'KELVIN': MetricUnits('KELVIN'),
        'JOULE': MetricUnits('JOULE'),
        'WATT': MetricUnits('WATT'),
        'VOLT': MetricUnits('VOLT'),
        'AMPERE': MetricUnits('AMPERE'),
        'VOLTAMPERE': MetricUnits('VOLTAMPERE'),
        'CANDELA': MetricUnits('CANDELA'),
        'MOLE': MetricUnits('MOLE'),
    })
    MetricUnits._set_binding_type(type.EnumType(
        'com.vmware.vstats.counter_metadata.metric_units',
        MetricUnits))


    class UnitsFactor(Enum):
        """
        Unit factor of measurement. **Warning:** This enumeration is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        YOTTA = None
        """
        Yotta 10^24. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        ZETTA = None
        """
        Zetta 10^21. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        EXA = None
        """
        Exa 10^18. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        PETA = None
        """
        Peta 10^15. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        TERA = None
        """
        Tera 10^12. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        GIGA = None
        """
        Giga 10^9. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        MEGA = None
        """
        Mega 10^6. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        KILO = None
        """
        Kilo 10^3. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        HECTO = None
        """
        Hecto 10^2. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        DECA = None
        """
        Deca 10. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        ONE = None
        """
        One. **Warning:** This class attribute is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        DECI = None
        """
        Deci 10^-1. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        CENTI = None
        """
        Centi 10^-2. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        MILLI = None
        """
        Milli 10^-3. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        MICRO = None
        """
        Micro 10^-6. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        NANO = None
        """
        Nano 10^-9. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        PIKO = None
        """
        Pico 10^-12. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        FEMTO = None
        """
        Femto 10^-15. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        ATTO = None
        """
        Atto 10^-18. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        ZEPTO = None
        """
        Zepto 10^-21. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        YOCTO = None
        """
        Yocto 10^-24. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        YOBI = None
        """
        Yobi 2^80, 1024^8. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        ZEBI = None
        """
        Zebi 2^70, 1024^7. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        EXBI = None
        """
        Exbi 2^60, 1024^6. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        PEBI = None
        """
        Pebi 2^50, 1024^5. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        TEBI = None
        """
        Tebi 2^40, 1024^4. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        GIBI = None
        """
        Gibi 2^30, 1024^3. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        MEBI = None
        """
        Mebi 2^20, 1024^2. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """
        KIBI = None
        """
        Kibi 2^10, 1024. **Warning:** This class attribute is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`UnitsFactor` instance.
            """
            Enum.__init__(string)

    UnitsFactor._set_values({
        'YOTTA': UnitsFactor('YOTTA'),
        'ZETTA': UnitsFactor('ZETTA'),
        'EXA': UnitsFactor('EXA'),
        'PETA': UnitsFactor('PETA'),
        'TERA': UnitsFactor('TERA'),
        'GIGA': UnitsFactor('GIGA'),
        'MEGA': UnitsFactor('MEGA'),
        'KILO': UnitsFactor('KILO'),
        'HECTO': UnitsFactor('HECTO'),
        'DECA': UnitsFactor('DECA'),
        'ONE': UnitsFactor('ONE'),
        'DECI': UnitsFactor('DECI'),
        'CENTI': UnitsFactor('CENTI'),
        'MILLI': UnitsFactor('MILLI'),
        'MICRO': UnitsFactor('MICRO'),
        'NANO': UnitsFactor('NANO'),
        'PIKO': UnitsFactor('PIKO'),
        'FEMTO': UnitsFactor('FEMTO'),
        'ATTO': UnitsFactor('ATTO'),
        'ZEPTO': UnitsFactor('ZEPTO'),
        'YOCTO': UnitsFactor('YOCTO'),
        'YOBI': UnitsFactor('YOBI'),
        'ZEBI': UnitsFactor('ZEBI'),
        'EXBI': UnitsFactor('EXBI'),
        'PEBI': UnitsFactor('PEBI'),
        'TEBI': UnitsFactor('TEBI'),
        'GIBI': UnitsFactor('GIBI'),
        'MEBI': UnitsFactor('MEBI'),
        'KIBI': UnitsFactor('KIBI'),
    })
    UnitsFactor._set_binding_type(type.EnumType(
        'com.vmware.vstats.counter_metadata.units_factor',
        UnitsFactor))


    class Info(VapiStruct):
        """
        The ``CounterMetadata.Info`` class contains information about
        CounterMetadata. It represents edition of the Counter. **Warning:** This
        class is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cid=None,
                     mid=None,
                     status=None,
                     type=None,
                     units=None,
                     scale=None,
                     user_info=None,
                     pid=None,
                    ):
            """
            :type  cid: :class:`str`
            :param cid: Counter Id. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Counter``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Counter``.
            :type  mid: :class:`str`
            :param mid: Metadata Id. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.CounterMetadata``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.CounterMetadata``.
            :type  status: :class:`CounterMetadata.CounterEditionStatus`
            :param status: Counter Edition status. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
            :type  type: :class:`CounterMetadata.SampleType`
            :param type: Numeric properties of the sampled data. **Warning:** This attribute
                is available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
            :type  units: :class:`CounterMetadata.MetricUnits`
            :param units: The units of the measurement. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
            :type  scale: :class:`CounterMetadata.UnitsFactor` or ``None``
            :param scale: Additional multiplier factors to be used with units. **Warning:**
                This attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                When None default of ``ONE`` is used.
            :type  user_info: :class:`UserInfo` or ``None``
            :param user_info: Human legible localizable text about the counter. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                This attribute is None in the current version.
            :type  pid: :class:`str` or ``None``
            :param pid: ID of the respective provider. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Provider``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.Provider``.
                This attribute is None in the current version.
            """
            self.cid = cid
            self.mid = mid
            self.status = status
            self.type = type
            self.units = units
            self.scale = scale
            self.user_info = user_info
            self.pid = pid
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vstats.counter_metadata.info', {
            'cid': type.IdType(resource_types='com.vmware.vstats.model.Counter'),
            'mid': type.IdType(resource_types='com.vmware.vstats.model.CounterMetadata'),
            'status': type.ReferenceType(__name__, 'CounterMetadata.CounterEditionStatus'),
            'type': type.ReferenceType(__name__, 'CounterMetadata.SampleType'),
            'units': type.ReferenceType(__name__, 'CounterMetadata.MetricUnits'),
            'scale': type.OptionalType(type.ReferenceType(__name__, 'CounterMetadata.UnitsFactor')),
            'user_info': type.OptionalType(type.ReferenceType(__name__, 'UserInfo')),
            'pid': type.OptionalType(type.IdType()),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``CounterMetadata.FilterSpec`` class is used to filter the counter
        metadata list. **Warning:** This class is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                    ):
            """
            :type  status: :class:`CounterMetadata.CounterEditionStatus` or ``None``
            :param status: Counter edition status. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When None no filtering on counter metadata status will be made.
            """
            self.status = status
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vstats.counter_metadata.filter_spec', {
            'status': type.OptionalType(type.ReferenceType(__name__, 'CounterMetadata.CounterEditionStatus')),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             cid,
             filter=None,
             ):
        """
        Returns information about all counter metadata records for a specific
        Counter. **Warning:** This method is available as Technology Preview.
        These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback,
        VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview
        APIs might only be applicable to specific environments.

        :type  cid: :class:`str`
        :param cid: Counter ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.Counter``.
        :type  filter: :class:`CounterMetadata.FilterSpec` or ``None``
        :param filter: Filter specification.
            When None no filtering will be performed.
        :rtype: :class:`list` of :class:`CounterMetadata.Info`
        :return: List of counter metadata for the specified counter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Counter could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('list',
                            {
                            'cid': cid,
                            'filter': filter,
                            })

    def get_default(self,
                    cid,
                    ):
        """
        This method returns the "default" CounterMetadata. A Counter has at
        least one related metadata object. Usually, stats providers (for
        example hosts) are in agreement about the default metadata. In this
        case the returned list has a single metadata object. 
        
        Sometimes, when providers are in "disagreement" about the default, then
        the returned list would include all the possible "defaults". This
        potential ambiguity isn't a real issue because consumers of the vStats
        API rarely need to specify the "mid" of metadata. Therefore, this API
        is used primarily for informational purposes.. **Warning:** This method
        is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since
        this can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  cid: :class:`str`
        :param cid: Counter ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.Counter``.
        :rtype: :class:`list` of :class:`CounterMetadata.Info`
        :return: List of counter metadata records.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``cid`` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Counter could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('get_default',
                            {
                            'cid': cid,
                            })

    def get(self,
            cid,
            mid,
            ):
        """
        Returns information about a specific CounterMetadata. **Warning:** This
        method is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since
        this can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  cid: :class:`str`
        :param cid: Counter ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.Counter``.
        :type  mid: :class:`str`
        :param mid: CounterMetadata ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.CounterMetadata``.
        :rtype: :class:`CounterMetadata.Info`
        :return: Information about the desired CounterMetadata.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Counter or CounterMetadata could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('get',
                            {
                            'cid': cid,
                            'mid': mid,
                            })
class CounterSets(VapiInterface):
    """
    The ``CounterSets`` class provides methods for accessing groupings of
    counters. Counter-sets allow consumers to use groups of counters. The
    counters may relate to different resource types. When an :class:`AcqSpecs`
    record refers to a counter-set, only the relevant counters apply.
    **Warning:** This class is available as Technology Preview. These are early
    access APIs provided to test, automate and provide feedback on the feature.
    Since this can change based on feedback, VMware does not guarantee
    backwards compatibility and recommends against using them in production
    environments. Some Technology Preview APIs might only be applicable to
    specific environments.
    """
    RESOURCE_TYPE = "com.vmware.vstats.model.CounterSet"
    """
    Resource type for counter sets. **Warning:** This class attribute is available
    as Technology Preview. These are early access APIs provided to test, automate
    and provide feedback on the feature. Since this can change based on feedback,
    VMware does not guarantee backwards compatibility and recommends against using
    them in production environments. Some Technology Preview APIs might only be
    applicable to specific environments.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.counter_sets'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CounterSetsStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``CounterSets.Info`` class contains information about a set of
        counters. **Warning:** This class is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     counters=None,
                     user_info=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Counter set identifier. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
            :type  counters: :class:`list` of :class:`CidMid`
            :param counters: List of Counter CidMids. **Warning:** This attribute is available
                as Technology Preview. These are early access APIs provided to
                test, automate and provide feedback on the feature. Since this can
                change based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
            :type  user_info: :class:`UserInfo` or ``None``
            :param user_info: Human legible localizable conter set description. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                In future versions it may be possible to have custom counter sets
                that lack localizable descriptions.
            """
            self.id = id
            self.counters = counters
            self.user_info = user_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vstats.counter_sets.info', {
            'id': type.StringType(),
            'counters': type.ListType(type.ReferenceType(__name__, 'CidMid')),
            'user_info': type.OptionalType(type.ReferenceType(__name__, 'UserInfo')),
        },
        Info,
        False,
        None))



    def list(self):
        """
        Returns information about all the counter sets. **Warning:** This
        method is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since
        this can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.


        :rtype: :class:`list` of :class:`CounterSets.Info`
        :return: List of counter sets.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('list', None)

    def get(self,
            counter_set,
            ):
        """
        Returns information about a specific counter set. **Warning:** This
        method is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since
        this can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  counter_set: :class:`str`
        :param counter_set: identifier of the counter set to retrieve.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.CounterSet``.
        :rtype: :class:`CounterSets.Info`
        :return: Information about the desired CounterSet.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``counter_set`` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the requested counter set could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('get',
                            {
                            'counter_set': counter_set,
                            })
class Counters(VapiInterface):
    """
    The ``Counters`` class provides methods to perform various Counter related
    operations. Counter is derived from metric. It applies the metric to a
    particular class of a resource. **Warning:** This class is available as
    Technology Preview. These are early access APIs provided to test, automate
    and provide feedback on the feature. Since this can change based on
    feedback, VMware does not guarantee backwards compatibility and recommends
    against using them in production environments. Some Technology Preview APIs
    might only be applicable to specific environments.
    """
    RESOURCE_TYPE = "com.vmware.vstats.model.Counter"
    """
    Resource type for counters. **Warning:** This class attribute is available as
    Technology Preview. These are early access APIs provided to test, automate and
    provide feedback on the feature. Since this can change based on feedback,
    VMware does not guarantee backwards compatibility and recommends against using
    them in production environments. Some Technology Preview APIs might only be
    applicable to specific environments.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.counters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CountersStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Counters.Info`` class contains the counter information. Counter is
        derived from metric. It applies the metric to a particular class of a
        resource. **Warning:** This class is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cid=None,
                     metric=None,
                     resource_address_schema=None,
                    ):
            """
            :type  cid: :class:`str`
            :param cid: Counter Id. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Counter``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Counter``.
            :type  metric: :class:`str`
            :param metric: A metric is typically human-legible ASCII/English name of a
                measurable aspect, for example "length" and "temperature". It is
                not internationalizable. **Warning:** This attribute is available
                as Technology Preview. These are early access APIs provided to
                test, automate and provide feedback on the feature. Since this can
                change based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Metric``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Metric``.
            :type  resource_address_schema: :class:`str`
            :param resource_address_schema: Describes formally how to address (or identify) the resources the
                counter could be bound to (or instantiated for). **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.RsrcAddrSchema``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.RsrcAddrSchema``.
            """
            self.cid = cid
            self.metric = metric
            self.resource_address_schema = resource_address_schema
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vstats.counters.info', {
            'cid': type.IdType(resource_types='com.vmware.vstats.model.Counter'),
            'metric': type.IdType(resource_types='com.vmware.vstats.model.Metric'),
            'resource_address_schema': type.IdType(resource_types='com.vmware.vstats.model.RsrcAddrSchema'),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Counters.FilterSpec`` class contains fields that can be used to
        filter list of counters. **Warning:** This class is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cid=None,
                     types=None,
                     metric=None,
                    ):
            """
            :type  cid: :class:`str` or ``None``
            :param cid: Counter identifier that will be listed. **Warning:** This attribute
                is available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Counter``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Counter``.
                If None counter filter will not be applied.
            :type  types: :class:`list` of :class:`str` or ``None``
            :param types: Resource type filter. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vstats.model.RsrcType``. When methods return a value
                of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vstats.model.RsrcType``.
                If None resource type filter will not be applied.
            :type  metric: :class:`str` or ``None``
            :param metric: Metric for which counters will be listed. **Warning:** This
                attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Metric``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Metric``.
                If None metric filter will not be applied.
            """
            self.cid = cid
            self.types = types
            self.metric = metric
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vstats.counters.filter_spec', {
            'cid': type.OptionalType(type.IdType()),
            'types': type.OptionalType(type.ListType(type.IdType())),
            'metric': type.OptionalType(type.IdType()),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns information about all counters matching the filter parameters.
        **Warning:** This method is available as Technology Preview. These are
        early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        :type  filter: :class:`Counters.FilterSpec` or ``None``
        :param filter: Filters the returned records.
            When None no filtering will be applied.
        :rtype: :class:`list` of :class:`Counters.Info`
        :return: List of Counters.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def get(self,
            cid,
            ):
        """
        Returns information about a specific Counter. **Warning:** This method
        is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since
        this can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  cid: :class:`str`
        :param cid: Counter ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.Counter``.
        :rtype: :class:`Counters.Info`
        :return: Information about the requested counter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``cid`` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Counter could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('get',
                            {
                            'cid': cid,
                            })
class Data(VapiInterface):
    """
    The ``Data`` class provides methods to query measurement and statistic
    data. **Warning:** This class is available as Technology Preview. These are
    early access APIs provided to test, automate and provide feedback on the
    feature. Since this can change based on feedback, VMware does not guarantee
    backwards compatibility and recommends against using them in production
    environments. Some Technology Preview APIs might only be applicable to
    specific environments.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.data'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DataStub)
        self._VAPI_OPERATION_IDS = {}

    class DataPoint(VapiStruct):
        """
        The ``Data.DataPoint`` class is an instance of a measurement or stat. A
        data point is comprised of a Counter, CounterMetadata, Resource, timestamp
        and value. **Warning:** This class is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cid=None,
                     mid=None,
                     rid=None,
                     ts=None,
                     val=None,
                    ):
            """
            :type  cid: :class:`str`
            :param cid: Counter Id. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Counter``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Counter``.
            :type  mid: :class:`str`
            :param mid: CounterMetadata Id. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.CounterMetadata``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.CounterMetadata``.
            :type  rid: :class:`str`
            :param rid: Resource Id. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
            :type  ts: :class:`long`
            :param ts: Timestamp for the data point. format: 64-bit integer. **Warning:**
                This attribute is available as Technology Preview. These are early
                access APIs provided to test, automate and provide feedback on the
                feature. Since this can change based on feedback, VMware does not
                guarantee backwards compatibility and recommends against using them
                in production environments. Some Technology Preview APIs might only
                be applicable to specific environments.
            :type  val: :class:`float`
            :param val: Stat value. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
            """
            self.cid = cid
            self.mid = mid
            self.rid = rid
            self.ts = ts
            self.val = val
            VapiStruct.__init__(self)


    DataPoint._set_binding_type(type.StructType(
        'com.vmware.vstats.data.data_point', {
            'cid': type.IdType(resource_types='com.vmware.vstats.model.Counter'),
            'mid': type.IdType(resource_types='com.vmware.vstats.model.CounterMetadata'),
            'rid': type.StringType(),
            'ts': type.IntegerType(),
            'val': type.DoubleType(),
        },
        DataPoint,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Data.FilterSpec`` class contains attributes used to filter the
        results when listing DataPoint. **Warning:** This class is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     start=None,
                     end=None,
                     cid=None,
                     metric=None,
                     types=None,
                     resources=None,
                     order=None,
                     page=None,
                    ):
            """
            :type  start: :class:`long` or ``None``
            :param start: Start of a time window (included), timestamp in seconds UTC.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
                When None the result will not be limited by start time.
            :type  end: :class:`long` or ``None``
            :param end: End of a time window (excluded), timestamp in seconds UTC.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
                When None the result will not be limited by end time.
            :type  cid: :class:`str` or ``None``
            :param cid: Counter ID. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Counter``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Counter``.
                When None the result will not be filtered by counter.
            :type  metric: :class:`str` or ``None``
            :param metric: Metric name. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Metric``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Metric``.
                When None the result will not be filtered by metric name.
            :type  types: :class:`list` of :class:`str` or ``None``
            :param types: List of Resource types. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vstats.model.RsrcType``. When methods return a value
                of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vstats.model.RsrcType``.
                When None the result will not be filtered by resource types.
            :type  resources: :class:`list` of :class:`str` or ``None``
            :param resources: Resources to include in the query. Each resource is specified
                through a composite string that follows the following format. 
                
                ``type.<resource type>[.<scheme>]=<resource id>`` 
                
                **resource type** specifies the type of resource for example
                ``VM``, ``VCPU`` etc. 
                
                **scheme** is an optional element to disambiguate the resource as
                needed for example to differentiate managed object id from
                ``uuid``. 
                
                **resource id** is the unique resource identifier value for
                example: ``vm-41`` 
                
                Example values include: ``type.VM=vm-41``, ``type.VCPU=1``,
                ``type.VM.moid=vm-41``. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When left None the result will not be filtered for specific
                resources.
            :type  order: :class:`str` or ``None``
            :param order: Directs the server to order the returned data. Passing a value of
                ``DEFAULT`` will apply default ordering of the results that makes
                them easier for consumption. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                When this parameter is None the server will not order the result,
                save computational time and therefore the API will operate faster.
            :type  page: :class:`str` or ``None``
            :param page: Used to retrieve paged data for larger result sets. The value of
                this token is generated by server and returned as ``next``
                attribute in the result of ``queryDataPoints`` methods.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
                When None the first page of results will be returned.
            """
            self.start = start
            self.end = end
            self.cid = cid
            self.metric = metric
            self.types = types
            self.resources = resources
            self.order = order
            self.page = page
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vstats.data.filter_spec', {
            'start': type.OptionalType(type.IntegerType()),
            'end': type.OptionalType(type.IntegerType()),
            'cid': type.OptionalType(type.IdType()),
            'metric': type.OptionalType(type.IdType()),
            'types': type.OptionalType(type.ListType(type.IdType())),
            'resources': type.OptionalType(type.ListType(type.StringType())),
            'order': type.OptionalType(type.StringType()),
            'page': type.OptionalType(type.StringType()),
        },
        FilterSpec,
        False,
        None))


    class DataPointsResult(VapiStruct):
        """
        The ``Data.DataPointsResult`` class contains attributes used to return
        DataPoints. **Warning:** This class is available as Technology Preview.
        These are early access APIs provided to test, automate and provide feedback
        on the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     data_points=None,
                     next=None,
                    ):
            """
            :type  data_points: :class:`list` of :class:`Data.DataPoint`
            :param data_points: List of DataPoints received. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
            :type  next: :class:`str` or ``None``
            :param next: The ``next`` attribute is a token used to retrieve paged data for
                larger result sets. This is opaque token generated by the server.
                It is to be sent in the :attr:`Data.FilterSpec.page` attribute to
                issue a subsequent call to the query method for retrieving results
                that did not fit the current page. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                :class:`set` when there are more results to retrieve.
            """
            self.data_points = data_points
            self.next = next
            VapiStruct.__init__(self)


    DataPointsResult._set_binding_type(type.StructType(
        'com.vmware.vstats.data.data_points_result', {
            'data_points': type.ListType(type.ReferenceType(__name__, 'Data.DataPoint')),
            'next': type.OptionalType(type.StringType()),
        },
        DataPointsResult,
        False,
        None))



    def query_data_points(self,
                          filter=None,
                          ):
        """
        Returns :class:`Data.DataPointsResult` matching the filter parameters. 
        
        ``"/stats/data/dp?types=VM&types=VCPU"`` 
        
        ``"/stats/data/dp?rsrcs=type.HOST=host-16&rsrcs=type.VM=vm-31"``.
        **Warning:** This method is available as Technology Preview. These are
        early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        :type  filter: :class:`Data.FilterSpec` or ``None``
        :param filter: Specification to match DataPoints.
            When :class:`set` filtering will be applied to the result.
        :rtype: :class:`Data.DataPointsResult`
        :return: Data points matching the filter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('query_data_points',
                            {
                            'filter': filter,
                            })
class Metrics(VapiInterface):
    """
    The ``Metrics`` class provides method to list metrics. A metric is a
    fundamental concept. It means a measurable aspect or property. For
    instance, temperature, count, velocity, data size, bandwidth. **Warning:**
    This class is available as Technology Preview. These are early access APIs
    provided to test, automate and provide feedback on the feature. Since this
    can change based on feedback, VMware does not guarantee backwards
    compatibility and recommends against using them in production environments.
    Some Technology Preview APIs might only be applicable to specific
    environments.
    """
    RESOURCE_TYPE = "com.vmware.vstats.model.Metric"
    """
    Resource type for metrics. **Warning:** This class attribute is available as
    Technology Preview. These are early access APIs provided to test, automate and
    provide feedback on the feature. Since this can change based on feedback,
    VMware does not guarantee backwards compatibility and recommends against using
    them in production environments. Some Technology Preview APIs might only be
    applicable to specific environments.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.metrics'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _MetricsStub)
        self._VAPI_OPERATION_IDS = {}

    class Summary(VapiStruct):
        """
        The ``Metrics.Summary`` class contains metric summary. **Warning:** This
        class is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     metric=None,
                    ):
            """
            :type  metric: :class:`str`
            :param metric: Metric name. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Metric``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vstats.model.Metric``.
            """
            self.metric = metric
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vstats.metrics.summary', {
            'metric': type.IdType(resource_types='com.vmware.vstats.model.Metric'),
        },
        Summary,
        False,
        None))



    def list(self):
        """
        Returns list of available Metrics as supplied by the discovered
        providers. **Warning:** This method is available as Technology Preview.
        These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback,
        VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview
        APIs might only be applicable to specific environments.


        :rtype: :class:`list` of :class:`Metrics.Summary`
        :return: List of Metrics.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('list', None)
class Providers(VapiInterface):
    """
    The ``Providers`` class manages list of statistical data provider services
    that are currently used. **Warning:** This class is available as Technology
    Preview. These are early access APIs provided to test, automate and provide
    feedback on the feature. Since this can change based on feedback, VMware
    does not guarantee backwards compatibility and recommends against using
    them in production environments. Some Technology Preview APIs might only be
    applicable to specific environments.
    """
    RESOURCE_TYPE = "com.vmware.vstats.model.Provider"
    """
    Resource type for data providers. **Warning:** This class attribute is
    available as Technology Preview. These are early access APIs provided to test,
    automate and provide feedback on the feature. Since this can change based on
    feedback, VMware does not guarantee backwards compatibility and recommends
    against using them in production environments. Some Technology Preview APIs
    might only be applicable to specific environments.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.providers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProvidersStub)
        self._VAPI_OPERATION_IDS = {}

    class Summary(VapiStruct):
        """
        ``Providers.Summary`` class describes a statistical data provider.
        **Warning:** This class is available as Technology Preview. These are early
        access APIs provided to test, automate and provide feedback on the feature.
        Since this can change based on feedback, VMware does not guarantee
        backwards compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     id_value=None,
                     type=None,
                     scheme=None,
                     metadata=None,
                     tracking_sn=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Provider identifier. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.Provider``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.Provider``.
            :type  id_value: :class:`str`
            :param id_value: The ID given to the provider by its respective inventory.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
            :type  type: :class:`str`
            :param type: Provider type. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
            :type  scheme: :class:`str` or ``None``
            :param scheme: An optional designation of the scheme. **Warning:** This attribute
                is available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                When None the provider is not designating a specific scheme.
            :type  metadata: :class:`str` or ``None``
            :param metadata: Schema-less metadata with extra information for the provider.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
                As supplied by the provider.
            :type  tracking_sn: :class:`long` or ``None``
            :param tracking_sn: Timestamp which is obtained when querying counters from a provider
                and is used as since parameter when new counter listing is needed.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
                {term unset} if no timestamp has been obtained yet.
            """
            self.id = id
            self.id_value = id_value
            self.type = type
            self.scheme = scheme
            self.metadata = metadata
            self.tracking_sn = tracking_sn
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vstats.providers.summary', {
            'id': type.IdType(resource_types='com.vmware.vstats.model.Provider'),
            'id_value': type.StringType(),
            'type': type.StringType(),
            'scheme': type.OptionalType(type.StringType()),
            'metadata': type.OptionalType(type.StringType()),
            'tracking_sn': type.OptionalType(type.IntegerType()),
        },
        Summary,
        False,
        None))



    def list(self):
        """
        Returns a list of stats providers. **Warning:** This method is
        available as Technology Preview. These are early access APIs provided
        to test, automate and provide feedback on the feature. Since this can
        change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.


        :rtype: :class:`list` of :class:`Providers.Summary`
        :return: List of stats providers.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('list', None)
class ResourceAddressSchemas(VapiInterface):
    """
    The ``ResourceAddressSchemas`` class manages inventory of resource
    addressing schemas used by :class:`Counters`. Each schema consists of a
    named list of resource identifiers of specific resource type. **Warning:**
    This class is available as Technology Preview. These are early access APIs
    provided to test, automate and provide feedback on the feature. Since this
    can change based on feedback, VMware does not guarantee backwards
    compatibility and recommends against using them in production environments.
    Some Technology Preview APIs might only be applicable to specific
    environments.
    """
    RESOURCE_TYPE = "com.vmware.vstats.model.RsrcAddrSchema"
    """
    Resource type for resource addressing schemas. **Warning:** This class
    attribute is available as Technology Preview. These are early access APIs
    provided to test, automate and provide feedback on the feature. Since this can
    change based on feedback, VMware does not guarantee backwards compatibility and
    recommends against using them in production environments. Some Technology
    Preview APIs might only be applicable to specific environments.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.resource_address_schemas'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ResourceAddressSchemasStub)
        self._VAPI_OPERATION_IDS = {}

    class QueryCapabilities(Enum):
        """
        Declares which predicates are supported by the
        ``ResourceAddressSchemas.ResourceIdDefinition``. **Warning:** This
        enumeration is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        EQUAL = None
        """
        Equal. **Warning:** This class attribute is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        """
        EQUAL_ALL = None
        """
        Supports both Equality and Aggregation. **Warning:** This class attribute
        is available as Technology Preview. These are early access APIs provided to
        test, automate and provide feedback on the feature. Since this can change
        based on feedback, VMware does not guarantee backwards compatibility and
        recommends against using them in production environments. Some Technology
        Preview APIs might only be applicable to specific environments.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`QueryCapabilities` instance.
            """
            Enum.__init__(string)

    QueryCapabilities._set_values({
        'EQUAL': QueryCapabilities('EQUAL'),
        'EQUAL_ALL': QueryCapabilities('EQUAL_ALL'),
    })
    QueryCapabilities._set_binding_type(type.EnumType(
        'com.vmware.vstats.resource_address_schemas.query_capabilities',
        QueryCapabilities))


    class ResourceIdDefinition(VapiStruct):
        """
        The ``ResourceAddressSchemas.ResourceIdDefinition`` class describes a
        single identifier of the Resource Addressing Schema. **Warning:** This
        class is available as Technology Preview. These are early access APIs
        provided to test, automate and provide feedback on the feature. Since this
        can change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production environments.
        Some Technology Preview APIs might only be applicable to specific
        environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     key=None,
                     type=None,
                     query_options=None,
                    ):
            """
            :type  key: :class:`str`
            :param key: Designates a semantic key for the resource identifier. This could
                be "vm" for virtual machine whose CPU usage is metered or "source"
                to identify the virtual machine that is origin of measured network
                traffic. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
            :type  type: :class:`str`
            :param type: Type of the resource. This represents various entities for which
                statistical data is gathered such as virtual machines, containers,
                servers, disks etc. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.RsrcType``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.RsrcType``.
            :type  query_options: :class:`ResourceAddressSchemas.QueryCapabilities`
            :param query_options: Designates the supported query-options. **Warning:** This attribute
                is available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
            """
            self.key = key
            self.type = type
            self.query_options = query_options
            VapiStruct.__init__(self)


    ResourceIdDefinition._set_binding_type(type.StructType(
        'com.vmware.vstats.resource_address_schemas.resource_id_definition', {
            'key': type.StringType(),
            'type': type.IdType(resource_types='com.vmware.vstats.model.RsrcType'),
            'query_options': type.ReferenceType(__name__, 'ResourceAddressSchemas.QueryCapabilities'),
        },
        ResourceIdDefinition,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``ResourceAddressSchemas.Info`` class defines addressing schema for a
        counter. This is set of named placeholders for different resource types.
        For example a network link between VMs will take two arguments "source" and
        "destination" both of type VM. For each argument query capability is
        defined. **Warning:** This class is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     schema=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Identifier. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.RsrcAddrSchema``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.RsrcAddrSchema``.
            :type  schema: :class:`list` of :class:`ResourceAddressSchemas.ResourceIdDefinition`
            :param schema: List of :class:`ResourceAddressSchemas.ResourceIdDefinition`s.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
            """
            self.id = id
            self.schema = schema
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vstats.resource_address_schemas.info', {
            'id': type.IdType(resource_types='com.vmware.vstats.model.RsrcAddrSchema'),
            'schema': type.ListType(type.ReferenceType(__name__, 'ResourceAddressSchemas.ResourceIdDefinition')),
        },
        Info,
        False,
        None))



    def get(self,
            id,
            ):
        """
        Returns information about a specific resource address schema.
        **Warning:** This method is available as Technology Preview. These are
        early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        :type  id: :class:`str`
        :param id: Resource address schema identifier.
        :rtype: :class:`ResourceAddressSchemas.Info`
        :return: Information about the desired resource address schema.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``id`` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if RsrcAddrSchema could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('get',
                            {
                            'id': id,
                            })
class ResourceAddresses(VapiInterface):
    """
    The ``ResourceAddresses`` class provides methods to perform resource
    addressing queries. **Warning:** This class is available as Technology
    Preview. These are early access APIs provided to test, automate and provide
    feedback on the feature. Since this can change based on feedback, VMware
    does not guarantee backwards compatibility and recommends against using
    them in production environments. Some Technology Preview APIs might only be
    applicable to specific environments.
    """
    RESOURCE_TYPE = "com.vmware.vstats.model.RsrcAddr"
    """
    Resource type for ``ResourceAddresses``. **Warning:** This class attribute is
    available as Technology Preview. These are early access APIs provided to test,
    automate and provide feedback on the feature. Since this can change based on
    feedback, VMware does not guarantee backwards compatibility and recommends
    against using them in production environments. Some Technology Preview APIs
    might only be applicable to specific environments.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.resource_addresses'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ResourceAddressesStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``ResourceAddresses.Info`` class contains global address of a specific
        Resource. **Warning:** This class is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     resource_ids=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Identifier. **Warning:** This attribute is available as Technology
                Preview. These are early access APIs provided to test, automate and
                provide feedback on the feature. Since this can change based on
                feedback, VMware does not guarantee backwards compatibility and
                recommends against using them in production environments. Some
                Technology Preview APIs might only be applicable to specific
                environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.RsrcAddr``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.RsrcAddr``.
            :type  resource_ids: :class:`list` of :class:`RsrcId`
            :param resource_ids: List of Resource Identifiers. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
            """
            self.id = id
            self.resource_ids = resource_ids
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vstats.resource_addresses.info', {
            'id': type.IdType(resource_types='com.vmware.vstats.model.RsrcAddr'),
            'resource_ids': type.ListType(type.ReferenceType(__name__, 'RsrcId')),
        },
        Info,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The :class:`ResourceAddresses.ListResult` class contains attributes used to
        return the resource addresses. **Warning:** This class is available as
        Technology Preview. These are early access APIs provided to test, automate
        and provide feedback on the feature. Since this can change based on
        feedback, VMware does not guarantee backwards compatibility and recommends
        against using them in production environments. Some Technology Preview APIs
        might only be applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     rsrc_addrs=None,
                     next=None,
                    ):
            """
            :type  rsrc_addrs: :class:`list` of :class:`ResourceAddresses.Info`
            :param rsrc_addrs: List of Resource Addresses received. **Warning:** This attribute is
                available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
            :type  next: :class:`str` or ``None``
            :param next: Used to retrieve paged data for larger result sets. Token is
                generated by server. The value of this field should be supplied in
                a subsequent call to :func:`ResourceAddresses.list` method.
                **Warning:** This attribute is available as Technology Preview.
                These are early access APIs provided to test, automate and provide
                feedback on the feature. Since this can change based on feedback,
                VMware does not guarantee backwards compatibility and recommends
                against using them in production environments. Some Technology
                Preview APIs might only be applicable to specific environments.
                None when there are no more pages of data to be retrieved.
            """
            self.rsrc_addrs = rsrc_addrs
            self.next = next
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vstats.resource_addresses.list_result', {
            'rsrc_addrs': type.ListType(type.ReferenceType(__name__, 'ResourceAddresses.Info')),
            'next': type.OptionalType(type.StringType()),
        },
        ListResult,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        ``ResourceAddresses.FilterSpec`` class describes filter criteria for
        resource addresses. **Warning:** This class is available as Technology
        Preview. These are early access APIs provided to test, automate and provide
        feedback on the feature. Since this can change based on feedback, VMware
        does not guarantee backwards compatibility and recommends against using
        them in production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     types=None,
                     resources=None,
                     page=None,
                    ):
            """
            :type  types: :class:`list` of :class:`str` or ``None``
            :param types: List of Resource types. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vstats.model.RsrcType``. When methods return a value
                of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vstats.model.RsrcType``.
                When None the result will not be filtered by resource types.
            :type  resources: :class:`list` of :class:`str` or ``None``
            :param resources: Resources to include in the query. Each resource is specified
                through a composite string that follows the following format. 
                
                ``type.<resource type>[.<scheme>]=<resource id>`` 
                
                **resource type** specifies the type of resource for example
                ``VM``, ``VCPU`` etc. 
                
                **scheme** is an optional element to disambiguate the resource as
                needed for example to differentiate managed object id from
                ``uuid``. 
                
                **resource id** is the unique resource identifier value for
                example: ``vm-41`` 
                
                Example values include: ``type.VM=vm-41``, ``type.VCPU=1``,
                ``type.VM.moid=vm-41``. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When left None the result will not be filtered for specific
                resources.
            :type  page: :class:`str` or ``None``
            :param page: The ``page`` field is used to retrieve paged data for large result
                sets. It is an opaque paging token obtained from a prior call to
                the :func:`ResourceAddresses.list` API. **Warning:** This attribute
                is available as Technology Preview. These are early access APIs
                provided to test, automate and provide feedback on the feature.
                Since this can change based on feedback, VMware does not guarantee
                backwards compatibility and recommends against using them in
                production environments. Some Technology Preview APIs might only be
                applicable to specific environments.
                when :class:`set` a follow up page in a paged result set will be
                delivered.
            """
            self.types = types
            self.resources = resources
            self.page = page
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vstats.resource_addresses.filter_spec', {
            'types': type.OptionalType(type.ListType(type.IdType())),
            'resources': type.OptionalType(type.ListType(type.StringType())),
            'page': type.OptionalType(type.StringType()),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns the list of Resource Addresses matching the filter parameters.
        **Warning:** This method is available as Technology Preview. These are
        early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        :type  filter: :class:`ResourceAddresses.FilterSpec` or ``None``
        :param filter: Criteria for selecting records to return.
            If None all records will be returned.
        :rtype: :class:`ResourceAddresses.ListResult`
        :return: Matching resource addresses.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def get(self,
            id,
            ):
        """
        Returns information about a specific Resource Address. **Warning:**
        This method is available as Technology Preview. These are early access
        APIs provided to test, automate and provide feedback on the feature.
        Since this can change based on feedback, VMware does not guarantee
        backwards compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.

        :type  id: :class:`str`
        :param id: Resource Address ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vstats.model.RsrcAddr``.
        :rtype: :class:`ResourceAddresses.Info`
        :return: Information about the desired Resource Address.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``id`` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Resource Address could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('get',
                            {
                            'id': id,
                            })
class ResourceTypes(VapiInterface):
    """
    The ``ResourceTypes`` class provides list of resource types. Resource
    refers to any item or concept that could have measurable properties. It is
    a prerequisite that a resource can be identified. 
    
    Example resource types are virtual machine, virtual disk etc.. **Warning:**
    This class is available as Technology Preview. These are early access APIs
    provided to test, automate and provide feedback on the feature. Since this
    can change based on feedback, VMware does not guarantee backwards
    compatibility and recommends against using them in production environments.
    Some Technology Preview APIs might only be applicable to specific
    environments.
    """
    RESOURCE_TYPE = "com.vmware.vstats.model.RsrcType"
    """
    Resource type for resource types. **Warning:** This class attribute is
    available as Technology Preview. These are early access APIs provided to test,
    automate and provide feedback on the feature. Since this can change based on
    feedback, VMware does not guarantee backwards compatibility and recommends
    against using them in production environments. Some Technology Preview APIs
    might only be applicable to specific environments.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vstats.resource_types'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ResourceTypesStub)
        self._VAPI_OPERATION_IDS = {}

    class Summary(VapiStruct):
        """
        The ``ResourceTypes.Summary`` class contains information of addressable
        resource. **Warning:** This class is available as Technology Preview. These
        are early access APIs provided to test, automate and provide feedback on
        the feature. Since this can change based on feedback, VMware does not
        guarantee backwards compatibility and recommends against using them in
        production environments. Some Technology Preview APIs might only be
        applicable to specific environments.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                    ):
            """
            :type  type: :class:`str`
            :param type: Resource type. **Warning:** This attribute is available as
                Technology Preview. These are early access APIs provided to test,
                automate and provide feedback on the feature. Since this can change
                based on feedback, VMware does not guarantee backwards
                compatibility and recommends against using them in production
                environments. Some Technology Preview APIs might only be applicable
                to specific environments.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vstats.model.RsrcType``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vstats.model.RsrcType``.
            """
            self.type = type
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vstats.resource_types.summary', {
            'type': type.IdType(resource_types='com.vmware.vstats.model.RsrcType'),
        },
        Summary,
        False,
        None))



    def list(self):
        """
        Returns a list of available resource types. **Warning:** This method is
        available as Technology Preview. These are early access APIs provided
        to test, automate and provide feedback on the feature. Since this can
        change based on feedback, VMware does not guarantee backwards
        compatibility and recommends against using them in production
        environments. Some Technology Preview APIs might only be applicable to
        specific environments.


        :rtype: :class:`list` of :class:`ResourceTypes.Summary`
        :return: List of resource types.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges.
        """
        return self._invoke('list', None)
class _AcqSpecsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'acq_spec': type.ReferenceType(__name__, 'AcqSpecs.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/stats/acq-specs',
            request_body_parameter='acq_spec',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'id': type.IdType(resource_types='com.vmware.vstats.model.AcqSpec'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/stats/acq-specs/{id}',
            path_variables={
                'id': 'id',
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
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'AcqSpecs.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/stats/acq-specs',
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
            'id': type.IdType(resource_types='com.vmware.vstats.model.AcqSpec'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/stats/acq-specs/{id}',
            path_variables={
                'id': 'id',
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
            'id': type.IdType(resource_types='com.vmware.vstats.model.AcqSpec'),
            'acq_spec': type.ReferenceType(__name__, 'AcqSpecs.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/stats/acq-specs/{id}',
            request_body_parameter='acq_spec',
            path_variables={
                'id': 'id',
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
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.vstats.model.AcqSpec'),
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'AcqSpecs.ListResult'),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'AcqSpecs.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vstats.acq_specs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _CounterMetadataStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cid': type.IdType(resource_types='com.vmware.vstats.model.Counter'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'CounterMetadata.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/stats/counters/{cid}/metadata',
            path_variables={
                'cid': 'cid',
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

        # properties for get_default operation
        get_default_input_type = type.StructType('operation-input', {
            'cid': type.IdType(resource_types='com.vmware.vstats.model.Counter'),
        })
        get_default_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_default_input_value_validator_list = [
        ]
        get_default_output_validator_list = [
        ]
        get_default_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/stats/counters/{cid}/metadata/default',
            path_variables={
                'cid': 'cid',
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
            'cid': type.IdType(resource_types='com.vmware.vstats.model.Counter'),
            'mid': type.IdType(resource_types='com.vmware.vstats.model.CounterMetadata'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/stats/counters/{cid}/metadata/{mid}',
            path_variables={
                'cid': 'cid',
                'mid': 'mid',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'CounterMetadata.Info')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_default': {
                'input_type': get_default_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'CounterMetadata.Info')),
                'errors': get_default_error_dict,
                'input_value_validator_list': get_default_input_value_validator_list,
                'output_validator_list': get_default_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'CounterMetadata.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get_default': get_default_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vstats.counter_metadata',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _CounterSetsStub(ApiInterfaceStub):
    def __init__(self, config):
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
            url_template='/stats/counter-sets',
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
            'counter_set': type.IdType(resource_types='com.vmware.vstats.model.CounterSet'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/stats/counter-sets/{counterSet}',
            path_variables={
                'counter_set': 'counterSet',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'CounterSets.Info')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'CounterSets.Info'),
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
            self, iface_name='com.vmware.vstats.counter_sets',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _CountersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Counters.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/stats/counters',
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
            'cid': type.IdType(resource_types='com.vmware.vstats.model.Counter'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/stats/counters/{cid}',
            path_variables={
                'cid': 'cid',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'Counters.Info')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Counters.Info'),
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
            self, iface_name='com.vmware.vstats.counters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _DataStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for query_data_points operation
        query_data_points_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Data.FilterSpec')),
        })
        query_data_points_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        query_data_points_input_value_validator_list = [
        ]
        query_data_points_output_validator_list = [
        ]
        query_data_points_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/stats/data/dp',
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
            'query_data_points': {
                'input_type': query_data_points_input_type,
                'output_type': type.ReferenceType(__name__, 'Data.DataPointsResult'),
                'errors': query_data_points_error_dict,
                'input_value_validator_list': query_data_points_input_value_validator_list,
                'output_validator_list': query_data_points_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'query_data_points': query_data_points_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vstats.data',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _MetricsStub(ApiInterfaceStub):
    def __init__(self, config):
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
            url_template='/stats/metrics',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Metrics.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vstats.metrics',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ProvidersStub(ApiInterfaceStub):
    def __init__(self, config):
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
            url_template='/stats/providers',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Providers.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vstats.providers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ResourceAddressSchemasStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/stats/rsrc-addr-schemas/{id}',
            path_variables={
                'id': 'id',
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
                'output_type': type.ReferenceType(__name__, 'ResourceAddressSchemas.Info'),
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
            self, iface_name='com.vmware.vstats.resource_address_schemas',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ResourceAddressesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'ResourceAddresses.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/stats/rsrc-addrs',
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
            'id': type.IdType(resource_types='com.vmware.vstats.model.RsrcAddr'),
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
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/stats/rsrc-addrs/{id}',
            path_variables={
                'id': 'id',
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
                'output_type': type.ReferenceType(__name__, 'ResourceAddresses.ListResult'),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'ResourceAddresses.Info'),
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
            self, iface_name='com.vmware.vstats.resource_addresses',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ResourceTypesStub(ApiInterfaceStub):
    def __init__(self, config):
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
            url_template='/stats/rsrc-types',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'ResourceTypes.Summary')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vstats.resource_types',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'AcqSpecs': AcqSpecs,
        'CounterMetadata': CounterMetadata,
        'CounterSets': CounterSets,
        'Counters': Counters,
        'Data': Data,
        'Metrics': Metrics,
        'Providers': Providers,
        'ResourceAddressSchemas': ResourceAddressSchemas,
        'ResourceAddresses': ResourceAddresses,
        'ResourceTypes': ResourceTypes,
    }

