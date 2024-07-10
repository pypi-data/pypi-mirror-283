# SPDX-License-Identifier: Apache-2.0

"""Entities."""

from entity_management.base import Derivation
from entity_management.core import AttrOf, DataDownload, Entity, attributes

from blue_cwl.mmodel import schemas
from blue_cwl.validation import validate_schema


class MorphologyAssignmentConfig(Entity):
    """Morphology assignment config entity."""

    def to_model(self) -> schemas.MModelConfigRaw:
        """Return the config from the json distribution."""
        # pylint: disable=no-member
        dataset = self.distribution.as_dict()
        validate_schema(data=dataset, schema_name="morphology_assignment_config_distribution.yml")
        return schemas.MModelConfigRaw.from_dict(dataset)


@attributes(
    {
        "distribution": AttrOf(DataDownload),
        "derivation": AttrOf(Derivation, default=None),
    }
)
class CanonicalMorphologyModelConfig(Entity):
    """Canonical morphology model config."""

    def to_model(self) -> schemas.CanonicalDistributionConfig:
        """Return the config from the json distribution."""
        # pylint: disable=no-member
        dataset = self.distribution.as_dict()
        validate_schema(
            data=dataset, schema_name="canonical_morphology_model_config_distribution_v2.yml"
        )
        return schemas.CanonicalDistributionConfig(data=dataset)


@attributes(
    {
        "distribution": AttrOf(DataDownload),
        "derivation": AttrOf(Derivation, default=None),
    }
)
class PlaceholderMorphologyConfig(Entity):
    """Placeholder morphologies config."""

    def to_model(self) -> schemas.PlaceholderDistributionConfig:
        """Return the config from the json distribution."""
        # pylint: disable=no-member
        dataset = self.distribution.as_dict()
        validate_schema(
            data=dataset, schema_name="placeholder_morphology_config_distribution_v2.yml"
        )
        return schemas.PlaceholderDistributionConfig(data=dataset)
