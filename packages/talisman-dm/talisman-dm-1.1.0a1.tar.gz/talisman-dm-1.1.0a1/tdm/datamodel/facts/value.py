from abc import ABCMeta
from dataclasses import dataclass, replace
from typing import Callable, Set, Union

from tdm.abstract.datamodel import AbstractDomain, AbstractFact, AbstractLinkFact, AbstractNode, AbstractNodeMention, \
    FactStatus, Identifiable
from tdm.abstract.datamodel.fact import AbstractValueFact
from tdm.abstract.datamodel.value import AbstractValue
from tdm.abstract.json_schema import generate_model
from tdm.datamodel.common import PrunableMixin, ViewContainer
from tdm.datamodel.domain import AtomValueType, ComponentValueType, CompositeValueType


@generate_model(label='atom')
@dataclass(frozen=True)
class AtomValueFact(Identifiable, AbstractValueFact[AtomValueType, AbstractValue], PrunableMixin):
    """
    Represents a fact that holds an atomic value.

    If the fact status is FactStatus.NEW `value` should be a tuple.
    If the fact status is FactStatus.APPROVED `value` should be single-valued.
    """
    def replace_with_domain(self, domain: AbstractDomain) -> 'AtomValueFact':
        if isinstance(self.type_id, str):
            domain_type = domain.get_type(self.type_id)
            if not isinstance(domain_type, AtomValueType):
                raise ValueError
            return replace(self, type_id=domain_type)
        return self

    def _as_tuple(self) -> tuple:
        return self.id, (self.type_id if isinstance(self.type_id, str) else self.type_id.id), self.value

    def __eq__(self, other):
        if not isinstance(other, AtomValueFact):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    @staticmethod
    def empty_value_filter() -> Callable[['AtomValueFact'], bool]:
        """
        Create a filter function to filter `AtomValueFact` instances with empty values.

        :return: A filter function for `AtomValueFact` instances with empty values.
        """
        return lambda f: isinstance(f.value, tuple) and not f.value

    @staticmethod
    def tuple_value_filter() -> Callable[['AtomValueFact'], bool]:
        """
        Create a filter function to filter `AtomValueFact` instances with tuple values.

        :return: A filter function for `AtomValueFact` instances with tuple values.
        """
        return lambda f: isinstance(f.value, tuple)

    @staticmethod
    def single_value_filter() -> Callable[['AtomValueFact'], bool]:
        """
        Create a filter function to filter `AtomValueFact` instances with a single value.

        :return: A filter function for `AtomValueFact` instances with a single value.
        """
        return lambda f: isinstance(f.value, AbstractValue)

    def is_hanging(self, doc: ViewContainer) -> bool:
        return self.status is not FactStatus.APPROVED \
            and not self.value \
            and not tuple(doc.related_elements(AbstractFact, self, MentionFact, tuple()))


@dataclass(frozen=True)
class _CompositeValueFact(AbstractFact, metaclass=ABCMeta):
    """
    Auxiliary class for `CompositeValueFact` to fix dataclass fields order.

    Attributes
    ----------
    type_id:
        The type identifier or domain composite value type of the composite value fact.
    """
    type_id: Union[str, CompositeValueType]

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'type_id'}

    @property
    def str_type_id(self) -> str:
        return self.type_id if isinstance(self.type_id, str) else self.type_id.id


@generate_model(label='composite')
@dataclass(frozen=True)
class CompositeValueFact(Identifiable, _CompositeValueFact, PrunableMixin):
    """
    Represents a fact that holds a composite value.

    The whole value is represented as `CompositeValueFact` with related `ComponentFact`s.
    """

    def replace_with_domain(self, domain: AbstractDomain) -> 'CompositeValueFact':
        if isinstance(self.type_id, str):
            domain_type = domain.get_type(self.type_id)
            if not isinstance(domain_type, CompositeValueType):
                raise ValueError
            return replace(self, type_id=domain_type)
        return self

    def _as_tuple(self) -> tuple:
        return self.id, (self.type_id if isinstance(self.type_id, str) else self.type_id.id)

    def __eq__(self, other):
        if not isinstance(other, CompositeValueFact):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    def is_hanging(self, doc: ViewContainer) -> bool:
        return self.status is not FactStatus.APPROVED and \
            not [x.target for x in doc.related_elements(AbstractFact, self, ComponentFact, tuple())]


ValueFact = Union[AtomValueFact, CompositeValueFact]


@dataclass(frozen=True)
class _MentionFact(AbstractFact, metaclass=ABCMeta):
    """
    Auxiliary class for `MentionFact` to fix dataclass fields order.

    Attributes
    ----------
    mention:
        The part of the node that contains value fact mention.
    value:
        The value fact mentioned in document node.
    """
    mention: AbstractNodeMention
    value: AtomValueFact

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'mention', 'value'}


@generate_model(label='mention')
@dataclass(frozen=True)
class MentionFact(Identifiable, _MentionFact):
    """
    Represents fact that some `AtomValueFact` is mentioned in the document node.

    """

    def replace_with_domain(self, domain: AbstractDomain) -> 'MentionFact':
        value = self.value.replace_with_domain(domain)
        if value is self.value:
            return self
        return replace(self, value=value)

    @staticmethod
    def node_filter(node: Union[AbstractNode, str]) -> Callable[['MentionFact'], bool]:
        """
        Create a filter function to filter `MentionFact` instances based on the document node.

        :param node: The document node or its identifier to filter by.
        :return: A filter function for `MentionFact` instances.
        """
        node_id = node.id if isinstance(node, AbstractNode) else node

        def _filter(fact: MentionFact) -> bool:
            return fact.mention.node_id == node_id

        return _filter

    @staticmethod
    def value_filter(filter_: Callable[[AtomValueFact], bool]) -> Callable[['MentionFact'], bool]:
        """
        Create a filter function to filter `MentionFact` instances based on the value.

        :param filter_: A filter function for mentioned `AtomValueFact`.
        :return: A filter function for `MentionFact` instances.
        """

        def _filter(fact: MentionFact) -> bool:
            return filter_(fact.value)

        return _filter


@generate_model(label='component')
@dataclass(frozen=True, eq=False)
class ComponentFact(Identifiable, AbstractLinkFact[CompositeValueFact, ValueFact, ComponentValueType]):
    """
    Represents a composite value component fact.
    It links composite value fact with another value fact (its component).
    """
    pass
