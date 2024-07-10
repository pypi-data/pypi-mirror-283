import os
import filecmp
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
from copy import deepcopy

import voxcell
import libsonata
import tempfile
import pytest
import pandas as pd
from pandas import testing as pdt
import numpy as np
from numpy import testing as npt

from blue_cwl import utils as tested
from blue_cwl.exceptions import CWLWorkflowError
from blue_cwl import constants
from blue_cwl.variant import Variant


DATA_DIR = Path(__file__).parent / "data"


def test_cwd():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tdir:
        tdir = Path(tdir).resolve()

        with tested.cwd(tdir):
            assert os.getcwd() == str(tdir)
        assert os.getcwd() == str(cwd)


@pytest.fixture
def io_data():
    return {
        "version": "v2.0",
        "neurons": [
            {
                "density": 100000,
                "region": "@3$",
                "traits": {
                    "layer": 3,
                    "mtype": "L23_MC",
                    "etype": {"bAC": 0.7, "bNAC": 0.3},
                },
            },
            {
                "density": 100000,
                "region": "@5$",
                "traits": {"layer": 5, "mtype": "L5_TPC:A", "etype": {"cADpyr": 1.0}},
            },
        ],
    }


def test_create_dir(tmp_path):
    directory = Path(tmp_path / "sub")

    assert not directory.exists()

    path = tested.create_dir(directory)
    assert path == directory
    assert path.exists()

    file = path / "file.txt"
    file.write_text("foo")

    # already exists
    path = tested.create_dir(directory)
    assert path == directory
    assert path.exists()

    # check that the directory is not cleaned
    assert file.exists()
    assert file.read_text() == "foo"


def test_load_yaml(io_data):
    yaml_file = DATA_DIR / "test_file.yml"
    data = tested.load_yaml(yaml_file)
    assert data == io_data


def test_write_yaml(io_data):
    with tempfile.NamedTemporaryFile(suffix=".yml") as tfile:
        tested.write_yaml(data=io_data, filepath=tfile.name)
        filecmp.cmp(tfile.name, DATA_DIR / "test_file.yml")


def test_load_json(io_data):
    json_file = DATA_DIR / "test_file.json"
    data = tested.load_json(json_file)
    assert data == io_data


def test_write_json(io_data):
    with tempfile.NamedTemporaryFile(suffix=".json") as tfile:
        tested.write_yaml(data=io_data, filepath=tfile.name)
        filecmp.cmp(tfile.name, DATA_DIR / "test_file.json")


def test_run_circuit_build_phase():
    with patch("subprocess.run"):
        tested.run_circuit_build_phase(
            bioname_dir="bioname-dir",
            cluster_config_file="some-path",
            phase="place_cells",
            output_dir=".",
        )


def test_build_manifest__default_parameters():
    res = tested.build_manifest(
        region="my-region",
        atlas_dir="my-atlas-dir",
    )
    assert res == {
        "common": {
            "atlas": "my-atlas-dir",
            "region": "my-region",
            "node_population_name": "my-region_neurons",
            "edge_population_name": "my-region_neurons__chemical_synapse",
            "morph_release": "",
            "synthesis": False,
            "partition": ["left", "right"],
        },
        **constants.DEFAULT_CIRCUIT_BUILD_PARAMETERS,
    }


def test_build_manifest__default_parameters_with_release():
    res = tested.build_manifest(
        region="my-region",
        atlas_dir="my-atlas-dir",
        morphology_release_dir="morph-dir",
    )
    assert res == {
        "common": {
            "atlas": "my-atlas-dir",
            "region": "my-region",
            "node_population_name": "my-region_neurons",
            "edge_population_name": "my-region_neurons__chemical_synapse",
            "morph_release": "morph-dir",
            "synthesis": False,
            "partition": ["left", "right"],
        },
        **constants.DEFAULT_CIRCUIT_BUILD_PARAMETERS,
    }


def test_build_manifest__custom_parameters():
    custom_parameters = {
        "step1": {"a": 1},
        "step2": {"b": 2},
    }

    res = tested.build_manifest(
        region="my-region",
        atlas_dir="my-atlas-dir",
        parameters=custom_parameters,
    )
    assert res == {
        "common": {
            "atlas": "my-atlas-dir",
            "region": "my-region",
            "node_population_name": "my-region_neurons",
            "edge_population_name": "my-region_neurons__chemical_synapse",
            "morph_release": "",
            "synthesis": False,
            "partition": ["left", "right"],
        },
        **custom_parameters,
    }


def teste_add_properties_to_node_population():
    with tempfile.TemporaryDirectory() as tdir:
        tdir = Path(tdir)

        test_path = tdir / "nodes.h5"

        shutil.copyfile(DATA_DIR / "nodes.h5", test_path)

        property1 = [1, 2, 3]
        property2 = ["a", "a", "b"]
        property3 = ["1", "1", "1"]

        properties = {"p1": property1, "p2": property2, "p3": property3}

        tested.write_node_population_with_properties(
            nodes_file=DATA_DIR / "nodes.h5",
            population_name="default",
            properties=properties,
            output_file=test_path,
        )

        population = voxcell.CellCollection.load_sonata(test_path, population_name="default")

        npt.assert_array_equal(population.properties["p1"], property1)
        npt.assert_array_equal(population.properties["p2"], property2)
        npt.assert_array_equal(population.properties["p3"], property3)


@pytest.fixture
def config_nodes_1():
    return {
        "version": 2,
        "manifest": {"$BASE_DIR": "."},
        "networks": {
            "nodes": [
                {
                    "nodes_file": "some-path",
                    "populations": {
                        "a-pop": {
                            "type": "biophysical",
                            "partial": ["cell-properties"],
                        }
                    },
                }
            ]
        },
    }


@pytest.fixture
def config_nodes_2(config_nodes_1):
    config = deepcopy(config_nodes_1)
    config["networks"]["nodes"].append(
        {
            "nodes_file": "some-path",
            "populations": {
                "b-pop": {
                    "type": "biophysical",
                    "partial": ["cell-properties", "morphologies"],
                    "morphologies_dir": "morph-path",
                }
            },
        }
    )
    return config


def test_get_biophysical_partial_population_from_config(config_nodes_1):
    nodes_file, population_name = tested.get_biophysical_partial_population_from_config(
        config_nodes_1
    )
    assert nodes_file == "some-path"
    assert population_name == "a-pop"


def test_get_biophysical_partial_population_from_config__raises():
    config = {
        "version": 2,
        "manifest": {"$BASE_DIR": "."},
        "networks": {
            "nodes": [
                {
                    "nodes_file": "some-path",
                    "populations": {
                        "a-pop": {
                            "type": "not-biophysical",
                            "partial": ["cell-properties"],
                        }
                    },
                }
            ]
        },
    }
    with pytest.raises(CWLWorkflowError, match="No biophysical population found in config"):
        tested.get_biophysical_partial_population_from_config(config)


@pytest.mark.parametrize("config", ["config_nodes_1", "config_nodes_2"])
def test_update_circuit_config_population__no_population(config, request):
    with pytest.raises(CWLWorkflowError, match="Population name John not in config."):
        tested.update_circuit_config_population(
            request.getfixturevalue(config),
            population_name="John",
            population_data={},
            filepath=None,
        )


def _check_population_changes(
    old_config, new_config, population_name, updated_nodes_file, updated_data
):
    for network_type, network_data in old_config["networks"].items():
        for i, entry in enumerate(network_data):
            new_entry = new_config["networks"][network_type][i]
            old_populations = entry["populations"]
            new_populations = new_entry["populations"]
            if population_name in old_populations:
                assert new_entry["nodes_file"] == updated_nodes_file
                for population_name, population_data in old_populations.items():
                    assert population_name in new_populations
                    new_population_data = new_populations[population_name]
                    for key, value in population_data.items():
                        if key in updated_data:
                            # updated values
                            assert new_population_data[key] == updated_data[key]
                        else:
                            # should remain unchanged
                            assert new_population_data[key] == value
            else:
                # ensure that irrelevant data has remained the same
                assert new_config["networks"][network_type][i] == entry


@pytest.mark.parametrize("config_fixture", ["config_nodes_1", "config_nodes_2"])
def test_update_circuit_config_population__node_population__add_morphologies_dir(
    config_fixture, request
):
    config = request.getfixturevalue(config_fixture)

    res = tested.update_circuit_config_population(
        config,
        population_name="a-pop",
        population_data={
            "partial": ["morphologies"],
            "morphologies_dir": "new-morph-path",
        },
        filepath="new-path",
    )
    _check_population_changes(
        old_config=config,
        new_config=res,
        population_name="a-pop",
        updated_nodes_file="new-path",
        updated_data={
            "partial": ["cell-properties", "morphologies"],
            "morphologies_dir": "new-morph-path",
        },
    )


def test_update_circuit_config_population__node_population__add_emodels__1(
    config_nodes_1,
):
    res = tested.update_circuit_config_population(
        config_nodes_1,
        population_name="a-pop",
        population_data={
            "partial": ["emodels"],
            "biophysical_neuron_models_dir": "new-emodels-dir",
        },
        filepath="new-path",
    )
    _check_population_changes(
        old_config=config_nodes_1,
        new_config=res,
        population_name="a-pop",
        updated_nodes_file="new-path",
        updated_data={
            "partial": ["cell-properties", "emodels"],
            "biophysical_models_dir": "new-emodels-dir",
        },
    )


def test_update_circuit_config_population__node_population__add_emodels_2(
    config_nodes_2,
):
    res = tested.update_circuit_config_population(
        config_nodes_2,
        population_name="b-pop",
        population_data={
            "partial": ["emodels"],
            "biophysical_neuron_models_dir": "new-emodels-dir",
        },
        filepath="new-path",
    )
    _check_population_changes(
        old_config=config_nodes_2,
        new_config=res,
        population_name="b-pop",
        updated_nodes_file="new-path",
        updated_data={
            "partial": ["cell-properties", "morphologies", "emodels"],
            "biophysical_models_dir": "new-emodels-dir",
        },
    )


def test_update_circuit_config_population__node_population__add_emodels__3(
    config_nodes_2,
):
    res = tested.update_circuit_config_population(
        config_nodes_2,
        population_name="a-pop",
        population_data={
            "partial": ["emodels"],
            "biophysical_neuron_models_dir": "new-emodels-dir",
        },
        filepath="new-path",
    )
    _check_population_changes(
        old_config=config_nodes_2,
        new_config=res,
        population_name="a-pop",
        updated_nodes_file="new-path",
        updated_data={
            "partial": ["cell-properties", "emodels"],
            "biophysical_models_dir": "new-emodels-dir",
        },
    )


def test_write_circuit_config_with_data(tmp_path):
    out_file = Path(tmp_path, "circuit_config.json")

    mock_config = {"foo": "bar"}
    with patch("blue_cwl.utils.update_circuit_config_population", return_value=mock_config):
        tested.write_circuit_config_with_data(None, None, None, None, output_config_file=out_file)

    res = tested.load_json(out_file)
    assert res == mock_config


def test_arrow_io():
    df = pd.DataFrame({"a": [1, 2, 3], "b": pd.Categorical(["a", "b", "b"]), "c": [0.1, 0.2, 0.3]})
    with tempfile.NamedTemporaryFile(suffix=".arrow") as tfile:
        filepath = tfile.name
        tested.write_arrow(filepath=filepath, dataframe=df)
        new_df = tested.load_arrow(filepath=filepath)

    pdt.assert_frame_equal(df, new_df)


def test_arrow_io__empty():
    df = pd.DataFrame(
        {
            "a": np.array([], dtype=np.float32),
            "b": np.array([], dtype=np.int64),
            "c": np.array([], dtype=bool),
        }
    )
    with tempfile.NamedTemporaryFile(suffix=".arrow") as tfile:
        filepath = tfile.name
        tested.write_arrow(filepath=filepath, dataframe=df)
        new_df = tested.load_arrow(filepath=filepath)

    pdt.assert_frame_equal(df, new_df)


def test_load_arrow__empty_dataset():
    res = tested.load_arrow(DATA_DIR / "empty_variant_overrides.arrow")

    expected_columns = [
        "side",
        "source_region",
        "source_mtype",
        "target_region",
        "target_mtype",
        "variant",
    ]

    assert res.columns.tolist() == expected_columns
    assert len(res) == 0

    for name in expected_columns:
        c = res[name]
        assert c.dtype == pd.CategoricalDtype(categories=[], ordered=False)


@pytest.fixture
def cells_100():
    nodes_file = DATA_DIR / "nodes_100.h5"
    return voxcell.CellCollection.load_sonata(nodes_file, "root__neurons")


def test_bisect_cell_collection_by_properties(cells_100):
    properties = {"mtype": ["GEN_mtype"], "region": ["CA3", "MMl", "VPL", "BLAa"]}

    splits = tested.bisect_cell_collection_by_properties(cells_100, properties)

    actual_indices = np.sort(np.concatenate([s.properties["split_index"] for s in splits]))
    npt.assert_array_equal(actual_indices, cells_100.properties.index.values)


def test_bisect_cell_collection_by_properties__one_split(cells_100):
    properties = {
        "mtype": cells_100.properties.mtype.unique().tolist(),
        "region": cells_100.properties.region.unique().tolist(),
    }

    splits = tested.bisect_cell_collection_by_properties(cells_100, properties)

    pdt.assert_frame_equal(splits[0].properties, cells_100.properties)
    assert "split_index" not in splits[0].properties
    assert splits[1] is None


def test_bisect_recombine_cycle(cells_100):
    properties = {"mtype": ["GEN_mtype"], "region": ["CA3", "MMl", "VPL", "BLAa"]}

    splits = tested.bisect_cell_collection_by_properties(cells_100, properties)

    res = tested.merge_cell_collections(splits, population_name=cells_100.population_name)

    assert cells_100.population_name == res.population_name
    assert cells_100.orientation_format == res.orientation_format
    npt.assert_allclose(cells_100.positions, res.positions)
    pdt.assert_frame_equal(cells_100.properties, res.properties)


@pytest.fixture
def variant_1():
    return Variant.from_registry("testing", "position", "v0.3.1")


@pytest.fixture
def variant_2():
    return Variant.from_registry("testing", "position", "v1")


@pytest.fixture
def variant_3():
    return Variant.from_registry("testing", "connectome", "v1")


@pytest.fixture
def variant_4():
    return Variant.from_registry("testing", "connectome_filtering", "v1")


def test_build_variant_allocation_command__wout_subtasks__wout_env_vars(tmp_path, variant_1):
    res = tested.build_variant_allocation_command("echo foo", variant_1)

    assert res == (
        "stdbuf -oL -eL salloc --partition=prod_small --nodes=1 --exclusive --time=1:00:00 "
        "--ntasks=1 --ntasks-per-node=1 --cpus-per-task=1 "
        "srun echo foo"
    )


def test_build_variant_allocation_command__wout_subtasks__with_env_vars(tmp_path, variant_2):
    res = tested.build_variant_allocation_command("echo foo", variant_2)

    assert res == (
        "stdbuf -oL -eL salloc --partition=prod_small --nodes=1 --exclusive --time=1:00:00 "
        "--ntasks=1 --ntasks-per-node=1 --cpus-per-task=1 "
        "srun env foo=1 bar=test echo foo"
    )


def test_build_variant_allocation_command__with_subtasks__with_env_vars(tmp_path, variant_3):
    res = tested.build_variant_allocation_command("echo foo", variant_3)

    assert res == (
        "stdbuf -oL -eL salloc --partition=prod --nodes=300 --ntasks-per-node=1 "
        "--cpus-per-task=40 --exclusive --time=1-00:00:00 --mem=0 --account=proj134 "
        "srun env OMP_NUM_THREADS=40 MPI_OPENMP_INTEROP=1 echo foo"
    )


def test_build_variant_allocation_command__with_subtasks__wout_env_vars(tmp_path, variant_4):
    res = tested.build_variant_allocation_command("echo foo", variant_4)

    assert res == (
        "stdbuf -oL -eL salloc --partition=prod --account=proj134 --nodes=20 "
        "--time=12:00:00 --ntasks-per-node=1 --mem=0 --exclusive --constraint=nvme "
        "srun echo foo"
    )


@pytest.fixture
def morph_config():
    return {
        "version": 2,
        "manifest": {"$BASE_DIR": "."},
        "networks": {
            "nodes": [
                {
                    "nodes_file": "some-path",
                    "populations": {
                        "a-pop": {
                            "type": "not-biophysical",
                            "partial": ["cell-properties"],
                            "morphologies_dir": "swc",
                            "alternate_morphologies": {
                                "h5v1": "h5",
                                "neurolucida-asc": "asc",
                            },
                        }
                    },
                }
            ]
        },
    }


def test_morphologies_dir__swc(morph_config):
    res = tested.get_morphologies_dir(morph_config, "a-pop", "swc")
    assert res == "swc"


def test_morphologies_dir__h5(morph_config):
    res = tested.get_morphologies_dir(morph_config, "a-pop", "h5")
    assert res == "h5"


def test_morphologies_dir__asc(morph_config):
    res = tested.get_morphologies_dir(morph_config, "a-pop", "asc")
    assert res == "asc"


def test_get_variant_resources_config__default(variant_1):
    res = tested._get_variant_resources_config(variant_1)

    assert res == {
        "partition": "prod_small",
        "nodes": 1,
        "exclusive": True,
        "time": "1:00:00",
        "ntasks": 1,
        "ntasks_per_node": 1,
        "cpus_per_task": 1,
    }


def test_get_variant_resources_config__subtask(variant_4):
    res1 = tested._get_variant_resources_config(variant_4, sub_task_index=0)
    res2 = tested._get_variant_resources_config(variant_4, sub_task_index=1)

    assert res1 == {
        "partition": "prod",
        "account": "proj134",
        "nodes": 20,
        "time": "16:00:00",
        "ntasks_per_node": 1,
        "mem": 0,
        "exclusive": True,
        "constraint": "nvme",
    }
    assert res2 == {
        "partition": "prod",
        "nodes": 100,
        "ntasks_per_node": 10,
        "cpus_per_task": 4,
        "exclusive": True,
        "time": "8:00:00",
        "mem": 0,
        "account": "proj134",
    }
