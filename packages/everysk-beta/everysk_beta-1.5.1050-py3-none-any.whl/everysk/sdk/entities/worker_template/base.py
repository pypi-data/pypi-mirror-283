###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from everysk.config import settings
from everysk.core.fields import StrField, ChoiceField, ListField, BoolField, DictField, IntField
from everysk.core.exceptions import SDKValueError

from everysk.sdk.entities.base import BaseEntity
from everysk.sdk.entities.query import Query
from everysk.sdk.entities.fields import EntityNameField, EntityTagsField

###############################################################################
#   Worker Template Implementation
###############################################################################
class WorkerTemplate(BaseEntity):

    description = StrField()
    tags = EntityTagsField()
    name = EntityNameField()

    visible = BoolField(default=False)
    category = StrField(default=Undefined, required_lazy=True)
    icon = ChoiceField(default=Undefined, choices=settings.WORKER_TEMPLATE_ICONS, required_lazy=True)
    type = ChoiceField(default=settings.WORKER_TEMPLATE_DEFAULT_TYPE, choices=settings.WORKER_TEMPLATE_TYPES, required_lazy=True)
    sort_index = IntField(required_lazy=True)

    ports = ListField()
    form_functions = DictField()
    form_inputs = ListField(max_size=settings.WORKER_TEMPLATE_SCRIPT_OUTPUTS_MAX_SIZE)
    form_outputs = DictField()
    default_output = StrField(required_lazy=True)
    path_name = StrField(required_lazy=True)

    script_runtime = ChoiceField(default=settings.WORKER_TEMPLATE_DEFAULT_SCRIPT_RUNTIME, choices=settings.WORKER_TEMPLATE_SCRIPT_RUNTIMES, required_lazy=True)
    script_entry_point = StrField(required_lazy=True)

    script_source = StrField(min_size=settings.WORKER_TEMPLATE_SCRIPT_SOURCE_MIN_SIZE, max_size=settings.WORKER_TEMPLATE_SCRIPT_SOURCE_MAX_SIZE, required_lazy=True)
    script_visible_source = StrField(min_size=settings.WORKER_TEMPLATE_SCRIPT_SOURCE_MIN_SIZE, max_size=settings.WORKER_TEMPLATE_SCRIPT_SOURCE_MAX_SIZE)

    @staticmethod
    def get_id_prefix() -> str:
        """
        Get the prefix for the unique identifier for this entity.

        Returns:
            str: The prefix for the unique identifier.

        Raises:
            NotImplementedError: This method should be overridden in subclasses.
        """
        return settings.WORKER_TEMPLATE_ID_PREFIX

    def validate(self) -> bool:
        """
        Validate the entity properties.

        Raises:
            FieldValueError: If the entity properties are invalid.
            RequiredFieldError: If a required field is missing.

        Returns:
            bool: True if the entity properties are valid, False otherwise.

        Example usage:
            >>> entity = MyEntity()
            >>> entity.validate()
            Traceback (most recent call last):
                ...
            everysk.sdk.exceptions.RequiredFieldError: The field 'name' is required.
        """
        return self.get_response(self_obj=self)

    def _check_query(self, query: Query) -> bool:
        """
        Check the query object.

        Args:
            query (Query): The query object.

        Returns:
            Query: The query object.
        """
        return True

    def _check_entity_to_query(self) -> bool:
        """
        Check the entity object to query.

        Returns:
            bool: True if the entity object is valid.
        """
        if self.name and self.tags:
            raise SDKValueError("Can't filter by Name and Tags at the same time")

        return True

    def _mount_query(self, query: Query) -> Query:
        """
        Mount the query object.

        Args:
            query (Query): The query object.

        Returns:
            Query: The query object.
        """
        if self.name is not None:
            query = query.where('name', self.name)
        if self.tags:
            query = query.where('tags', self.tags)

        return query
