# SPDX-License-Identifier: Apache-2.0

"""me-model wrapper."""

import logging
from pathlib import Path

import click
from entity_management.simulation import DetailedCircuit
from entity_management.util import get_entity, unquote_uri_path

from blue_cwl import registering, utils, validation
from blue_cwl.constants import DEFAULT_CIRCUIT_CONFIG_FILENAME
from blue_cwl.me_model.entity import MEModelConfig
from blue_cwl.me_model.recipe import build_me_model_recipe
from blue_cwl.me_model.staging import stage_me_model_config
from blue_cwl.nexus import get_distribution_as_dict
from blue_cwl.staging import stage_file
from blue_cwl.typing import StrOrPath
from blue_cwl.utils import get_partial_circuit_region_id
from blue_cwl.wrappers import common

L = logging.getLogger(__name__)


INPUT_POPULATION_COLUMNS = [
    "etype",
    "mtype",
    "region",
    "subregion",
    "morphology",
]


ASSIGN_PROPERTIES = ["model_template"]
ADAPT_PROPERTIES = [
    "dynamics_params/AIS_scaler",
    "dynamics_params/soma_scaler",
]
CURRENTS_PROPERTIES = [
    "dynamics_params/holding_current",
    "dynamics_params/input_resistance",
    "dynamics_params/threshold_current",
    "dynamics_params/resting_potential",
]


@click.group(name="me-model")
def app():
    """me-model app."""


@app.command(name="setup")
@click.option("--output-dir", required=True, help="Output directory path")
def setup_cli(output_dir):
    """Setup wrapper output directories."""
    common.setup_directories(output_dir=output_dir)


@app.command(name="stage")
@click.option("--configuration-id", required=True, help="me-model configuration id.")
@click.option("--circuit-id", required=True, help="Circuit id.")
@click.option("--stage-dir", required=True, help="Stagind directory")
def stage_cli(**kwargs):
    """Stage cli."""
    stage(**kwargs)


def stage(*, configuration_id, circuit_id, stage_dir):
    """Stage NEXUS resources to local files."""
    utils.create_dir(stage_dir)

    config_file = Path(stage_dir, "materialized_me_model_config.json")
    stage_me_model_config(
        dataset=get_distribution_as_dict(configuration_id, cls=MEModelConfig),
        staging_dir=Path(stage_dir, "me-model-config"),
        output_file=config_file,
    )
    L.debug("me-model config %s materialized at %s", configuration_id, config_file)

    circuit_file = Path(stage_dir, DEFAULT_CIRCUIT_CONFIG_FILENAME)
    _stage_circuit(
        partial_circuit=circuit_id,
        output_file=circuit_file,
    )
    L.debug("Circuit %s staged at %s", circuit_id, circuit_file)

    nodes_file, _, morphologies_dir = _get_biophysical_population_info(
        circuit_config_file=circuit_file,
        ext="asc",
    )

    staged_morphologies_dir = Path(stage_dir, "morphologies")
    stage_file(source=morphologies_dir, target=staged_morphologies_dir)
    L.debug("Staged %s -> %s", morphologies_dir, staged_morphologies_dir)

    staged_nodes_file = Path(stage_dir, "nodes.h5")
    stage_file(source=nodes_file, target=staged_nodes_file)
    L.debug("Staged %s -> %s", nodes_file, staged_nodes_file)


@app.command(name="recipe")
@click.option("--config-file", required=True, help="me-model configuration file")
@click.option("--output-file", required=True, help="Output recipe file")
def recipe_cli(**kwargs):
    """Generate me-model recipe."""
    recipe(**kwargs)


def recipe(*, config_file, output_file):
    """Generate me-model recipe."""
    configuration = utils.load_json(config_file)
    recipe_config = build_me_model_recipe(me_model_config=configuration)
    utils.write_json(data=recipe_config, filepath=output_file)


@app.command(name="register")
@click.option("--circuit-id", required=True)
@click.option("--circuit-file", required=True)
@click.option("--nodes-file", required=True)
@click.option("--hoc-dir", required=True)
@click.option("--output-dir", required=True)
@click.option("--output-resource-file", required=True)
def register_cli(**kwargs):
    """Register cli."""
    register(**kwargs)


def register(
    *,
    circuit_id: str,
    circuit_file: StrOrPath,
    nodes_file: StrOrPath,
    hoc_dir: StrOrPath,
    output_dir: StrOrPath,
    output_resource_file: StrOrPath,
) -> None:
    """Register new circuit with generated nodes and hoc directory.

    Args:
        circuit_id: The NEXUS resource id of the input DetailedCircuit.
        circuit_file: Staged circuit config file.
        nodes_file: Updated nodes file.
        hoc_dir: Biophysical models directory.
        output_dir: Output directory to use.
        output_resource_file: Optional output resource file to write the registered entity id.
    """
    config = utils.load_json(circuit_file)
    _, population_name = utils.get_biophysical_partial_population_from_config(config)

    L.info("Validating input nodes file...")
    validation.check_properties_in_population(
        population_name=population_name,
        nodes_file=nodes_file,
        property_names=INPUT_POPULATION_COLUMNS
        + ASSIGN_PROPERTIES
        + ADAPT_PROPERTIES
        + CURRENTS_PROPERTIES,
    )

    L.info("Generating updated circuit config...")
    output_circuit_config_file = Path(output_dir, DEFAULT_CIRCUIT_CONFIG_FILENAME)

    utils.write_circuit_config_with_data(
        config=config,
        population_name=population_name,
        population_data={
            "biophysical_neuron_models_dir": str(hoc_dir),
        },
        filepath=str(nodes_file),
        output_config_file=output_circuit_config_file,
    )

    validation.check_population_name_in_config(population_name, output_circuit_config_file)

    L.info("Registering DetailedCircuit...")
    circuit = _register_circuit(circuit_id, output_circuit_config_file)

    L.info("Writing circuit id to output resource file...")
    common.write_entity_id_to_file(entity=circuit, output_file=output_resource_file)


def _stage_circuit(partial_circuit, output_file):
    entity = get_entity(resource_id=partial_circuit, cls=DetailedCircuit)
    stage_file(
        source=unquote_uri_path(entity.circuitConfigPath.url),
        target=output_file,
        symbolic=True,
    )


def _get_biophysical_population_info(circuit_config_file, ext):
    config = utils.load_json(circuit_config_file)
    (
        nodes_file,
        node_population_name,
    ) = utils.get_biophysical_partial_population_from_config(config)
    morphologies_dir = utils.get_morphologies_dir(
        circuit_config=config,
        population_name=node_population_name,
        ext=ext,
    )
    return nodes_file, node_population_name, morphologies_dir


def _register_circuit(partial_circuit, output_circuit_config_file):
    partial_circuit = get_entity(resource_id=partial_circuit, cls=DetailedCircuit)

    circuit = registering.register_partial_circuit(
        name="Partial circuit with biohysical emodel properties",
        brain_region_id=get_partial_circuit_region_id(partial_circuit),
        atlas_release=partial_circuit.atlasRelease,
        description="Partial circuit with cell properties, morphologies, and biophysical models.",
        sonata_config_path=output_circuit_config_file,
    )

    return circuit
