# SPDX-License-Identifier: Apache-2.0

"""Nexus stuff."""

import logging
import os
from datetime import datetime
from functools import wraps

import jwt
import requests
from entity_management import nexus, state
from entity_management.core import DataDownload, Entity

from blue_cwl.exceptions import CWLRegistryError
from blue_cwl.typing import StrOrPath
from blue_cwl.utils import get_obj

L = logging.getLogger(__name__)

# Renew the token if it expires in 5 minutes from now
SECONDS_TO_EXPIRATION = 5 * 60


TEntity = type[Entity]


def get_distribution(
    id_or_entity: str | Entity,
    *,
    cls: TEntity = Entity,
    encoding_format: str | None = None,
    base: str | None = None,
    org: str | None = None,
    proj: str | None = None,
    token: str | None = None,
) -> DataDownload:
    """Return the distribution's location path from the resource.

    Args:
        id_or_entity: Either the id to retrieve the entity or the entity.
        cls: entity-management class to instantiate. Default is Entity.
        encoding_format: The format to match in case of multiple distributions.
        base: The nexus base endpoint. If None entity-management's runtime base is used.
        org: The nexus organization. If None entity-management's runtime org is used.
        proj: The nexus project. If None entity-management's runtime proj is used.
        token: Optional OAuth token. If None entity-management's runtime token is used.

    Returns:
        Instantiated entity from given id.

    Raises:
        CWLRegistryError:
            * If entity is not found.
            * If multiple distributions and no matching encoding format.

    Note:
        A resource may have many distributions with a different encoding format. If that's the case
        the encoding format argument is mandatory to select the respective distribution.
    """
    entity = get_obj(id_or_entity, cls=cls, base=base, org=org, proj=proj, token=token)
    distribution = entity.distribution

    if isinstance(distribution, list):
        if len(distribution) > 1:
            for d in distribution:
                if d.encodingFormat == encoding_format:
                    return d
            raise CWLRegistryError(
                f"Multiple distributions in resource {entity.get_id()}.\n"
                f"Encoding format {encoding_format} did not correspond to any distribution."
            )
        return distribution[0]

    if encoding_format and encoding_format != distribution.encodingFormat:
        raise CWLRegistryError(
            f"Entity {entity.get_id()} distribution's "
            f"encoding format '{encoding_format}' does not match "
            f"distribution's format '{distribution.encodingFormat}'"
        )

    return entity.distribution


def get_distribution_location_path(
    id_or_entity: str | TEntity,
    *,
    cls: TEntity = Entity,
    encoding_format: str | None = None,
    base: str | None = None,
    org: str | None = None,
    proj: str | None = None,
    token: str | None = None,
) -> str:
    """Return the distribution's location path from the resource.

    Args:
        id_or_entity: Either the id to retrieve the entity or the entity.
        cls: entity-management class to instantiate. Default is Entity.
        encoding_format: The encoding format of the distribution. Example: application/json
        base: The nexus base endpoint. If None entity-management's runtime base is used.
        org: The nexus organization. If None entity-management's runtime org is used.
        proj: The nexus project. If None entity-management's runtime proj is used.
        token: Optional OAuth token. If None entity-management's runtime token is used.

    Returns:
        Instantiated entity from given id.

    Raises:
        CWLRegistryError if entity is not found.

    Note:
        A resource may have many distributions with a different encoding format. If that's the case
        the encoding format argument is mandatory to select the respective distribution.
    """
    distribution = get_distribution(
        id_or_entity,
        cls=cls,
        encoding_format=encoding_format,
        base=base,
        org=org,
        proj=proj,
        token=token,
    )
    return distribution.get_location_path(use_auth=token)


def download_distribution(
    id_or_entity: str | TEntity,
    *,
    output_dir: StrOrPath,
    filename: str | None = None,
    cls: TEntity = Entity,
    encoding_format: str | None = None,
    base: str | None = None,
    org: str | None = None,
    proj: str | None = None,
    token: str | None = None,
) -> str:
    """Download an entity's distribution.

    Args:
        id_or_entity: Either the id to retrieve the entity or the entity.
        cls: entity-management class to instantiate. Default is Entity.
        output_dir: Output directory to download the distribution to.
        filename: Filename to use. Resource's file name is used by default.
        encoding_format: The format to choose if many.
        encoding_format: The format to match in case of multiple distributions.
        base: The nexus base endpoint. If None entity-management's runtime base is used.
        org: The nexus organization. If None entity-management's runtime org is used.
        proj: The nexus project. If None entity-management's runtime proj is used.
        token: Optional OAuth token. If None entity-management's runtime token is used.

    Returns:
        Instantiated entity from given id.

    Raises:
        CWLRegistryError if entity is not found.
    """
    distribution = get_distribution(
        id_or_entity,
        cls=cls,
        encoding_format=encoding_format,
        base=base,
        org=org,
        proj=proj,
        token=token,
    )
    path = distribution.download(
        path=str(output_dir),
        file_name=filename,
        use_auth=token,
    )
    return str(path)


def get_distribution_as_dict(
    id_or_entity: str | TEntity,
    *,
    cls: TEntity = Entity,
    base: str | None = None,
    org: str | None = None,
    proj: str | None = None,
    token: str | None = None,
) -> dict:
    """Return the distribution json payload as a dictionary.

    Args:
        id_or_entity: Either the id to retrieve the entity or the entity.
        cls: entity-management class to instantiate. Default is Entity.
        base: The nexus base endpoint. If None entity-management's runtime base is used.
        org: The nexus organization. If None entity-management's runtime org is used.
        proj: The nexus project. If None entity-management's runtime proj is used.
        token: Optional OAuth token. If None entity-management's runtime token is used.

    Returns:
        Instantiated entity from given id.

    Raises:
        CWLRegistryError if entity is not found.
    """
    distribution = get_distribution(
        id_or_entity,
        cls=cls,
        encoding_format="application/json",
        base=base,
        org=org,
        proj=proj,
        token=token,
    )
    return distribution.as_dict(use_auth=token)


def get_region_acronym(
    resource_id: str,
    *,
    base: str | None = None,
    token: str | None = None,
) -> str:
    """Retrieve the hierarchy acronym from a KG registered region."""
    return nexus.load_by_id(
        resource_id=resource_id,
        cross_bucket=False,
        base=base,
        org="neurosciencegraph",
        proj="datamodels",
        token=token,
    )["notation"]


def _decode(token: str) -> dict:
    """Decode the token, and return its contents."""
    return jwt.decode(token, options={"verify_signature": False})


def _has_expired(token: str) -> bool:
    """Check if the token has expired or is going to expire in 'SECONDS_TO_EXPIRATION'."""
    expiration_time = _decode(token)["exp"]
    return datetime.timestamp(datetime.now()) + SECONDS_TO_EXPIRATION > expiration_time


def _refresh_token_on_failure(func):
    """Refresh access token on failure and try again."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Decorator function."""
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e1:
            if e1.response.status_code == 401 and state.has_offline_token():
                kwargs["token"] = state.refresh_token()
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e2:
                    nexus._print_nexus_error(e2)  # pylint: disable=protected-access
                    raise
            nexus._print_nexus_error(e1)  # pylint: disable=protected-access
            raise

    return wrapper


def _get_valid_token(token: str | None = None, force_refresh: bool = False) -> str:
    """Return a valid token if possible."""
    if token is None:
        token = state.get_token()
    else:
        state.set_token(token)

    # the access token can only be refreshed if an offline/refresh token is available
    if (force_refresh or _has_expired(token)) and state.has_offline_token():
        return state.refresh_token()

    return token


def get_forge(
    nexus_base: str | None = None,
    nexus_org: str | None = None,
    nexus_project: str | None = None,
    nexus_token: str | None = None,
    force_refresh: bool = False,
):  # pragma: no cover
    """Create a KnowledgeGraphForge instance.

    Args:
        nexus_base: The nexus instance endpoint.
        nexus_org: The nexus organization.
        nexus_project: The nexus project.
        nexus_token: The OAUth token.
        force_refresh: Whether to attempt renew the token (Requires offline token).

    Returns:
        KnowledgeGraphForge instance
    """
    from kgforge.core import KnowledgeGraphForge  # pylint: disable=import-error

    nexus_base = nexus_base or os.getenv("NEXUS_BASE")
    nexus_org = nexus_org or state.get_org()
    nexus_project = nexus_project or state.get_proj()
    nexus_token = _get_valid_token(nexus_token, force_refresh)

    return _refresh_token_on_failure(KnowledgeGraphForge)(
        configuration="https://raw.githubusercontent.com/BlueBrain/nexus-forge/master/examples/notebooks/use-cases/prod-forge-nexus.yml",
        bucket=f"{nexus_org}/{nexus_project}",
        endpoint=nexus_base,
        searchendpoints={
            "sparql": {
                "endpoint": "https://bbp.epfl.ch/neurosciencegraph/data/views/aggreg-sp/dataset"
            },
            "elastic": {
                "endpoint": "https://bbp.epfl.ch/neurosciencegraph/data/views/aggreg-es/dataset",
                "mapping": "https://bbp.epfl.ch/neurosciencegraph/data/views/es/dataset",
                "default_str_keyword_field": "keyword",
            },
        },
        token=nexus_token,
    )


def forge_to_config(forge) -> tuple[str, str, str, str]:
    """Get nexus configuration from forge instance.

    Args:
        forge: The KnowledgeGraphForge instance.

    Returns:
        (base, org, proj, token) tuple
    """
    store = forge._store  # pylint: disable=protected-access
    org, proj = store.bucket.split("/")
    return (
        store.endpoint,
        org,
        proj,
        store.token,
    )


def get_resource(forge, resource_id: str):
    """Get resource from knowledge graph.

    Args:
        forge: The KnowledgeGraphForge instance.
        resource_id: The string id of the resource to retrieve.

    Returns:
        kgforge resource.

    Raises:
        CWLRegistryError if resource is not found.
    """
    resource = forge.retrieve(resource_id, cross_bucket=True)

    if resource is None:
        # pylint: disable=protected-access
        raise CWLRegistryError(
            f"Resource id {resource_id} could not be retrieved.\n"
            f"endpoint: {forge._store.endpoint}\n"
            f"bucket  : {forge._store.bucket}"
        )
    return resource
