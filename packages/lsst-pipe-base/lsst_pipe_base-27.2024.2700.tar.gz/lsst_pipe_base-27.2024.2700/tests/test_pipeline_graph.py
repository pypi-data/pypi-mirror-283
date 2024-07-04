# This file is part of pipe_base.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Tests of things related to the GraphBuilder class."""

import copy
import io
import logging
import pickle
import textwrap
import unittest
from typing import Any

import lsst.pipe.base.automatic_connection_constants as acc
import lsst.utils.tests
from lsst.daf.butler import DataCoordinate, DatasetRef, DatasetType, DimensionUniverse, StorageClassFactory
from lsst.daf.butler.registry import MissingDatasetTypeError
from lsst.pipe.base.pipeline_graph import (
    ConnectionTypeConsistencyError,
    DuplicateOutputError,
    Edge,
    EdgesChangedError,
    IncompatibleDatasetTypeError,
    NodeKey,
    NodeType,
    PipelineGraph,
    PipelineGraphError,
    TaskImportMode,
    UnresolvedGraphError,
    visualization,
)
from lsst.pipe.base.tests.mocks import (
    DynamicConnectionConfig,
    DynamicTestPipelineTask,
    DynamicTestPipelineTaskConfig,
    get_mock_name,
)

_LOG = logging.getLogger(__name__)


class MockRegistry:
    """A test-utility stand-in for lsst.daf.butler.Registry that just knows
    how to get dataset types.
    """

    def __init__(self, dimensions: DimensionUniverse, dataset_types: dict[str, DatasetType]) -> None:
        self.dimensions = dimensions
        self._dataset_types = dataset_types

    def getDatasetType(self, name: str) -> DatasetType:
        try:
            return self._dataset_types[name]
        except KeyError:
            raise MissingDatasetTypeError(name) from None


class PipelineGraphTestCase(unittest.TestCase):
    """Tests for the `PipelineGraph` class.

    Tests for `PipelineGraph.resolve` are mostly in
    `PipelineGraphResolveTestCase` later in this file.
    """

    def setUp(self) -> None:
        # Simple test pipeline has two tasks, 'a' and 'b', with dataset types
        # 'input', 'intermediate', and 'output'.  There are no dimensions on
        # any of those.  We add tasks in reverse order to better test sorting.
        # There is one labeled task subset, 'only_b', with just 'b' in it.
        # We copy the configs so the originals (the instance attributes) can
        # be modified and reused after the ones passed in to the graph are
        # frozen.
        self.description = "A pipeline for PipelineGraph unit tests."
        self.graph = PipelineGraph()
        self.graph.description = self.description
        self.b_config = DynamicTestPipelineTaskConfig()
        self.b_config.init_inputs["in_schema"] = DynamicConnectionConfig(dataset_type_name="schema")
        self.b_config.inputs["input1"] = DynamicConnectionConfig(dataset_type_name="intermediate_1")
        self.b_config.outputs["output1"] = DynamicConnectionConfig(dataset_type_name="output_1")
        self.graph.add_task("b", DynamicTestPipelineTask, copy.deepcopy(self.b_config))
        self.a_config = DynamicTestPipelineTaskConfig()
        self.a_config.init_outputs["out_schema"] = DynamicConnectionConfig(dataset_type_name="schema")
        self.a_config.inputs["input1"] = DynamicConnectionConfig(dataset_type_name="input_1")
        self.a_config.outputs["output1"] = DynamicConnectionConfig(dataset_type_name="intermediate_1")
        self.graph.add_task("a", DynamicTestPipelineTask, copy.deepcopy(self.a_config))
        self.graph.add_task_subset("only_b", ["b"])
        self.subset_description = "A subset with only task B in it."
        self.graph.task_subsets["only_b"].description = self.subset_description
        self.dimensions = DimensionUniverse()
        self.maxDiff = None

    def test_unresolved_accessors(self) -> None:
        """Test attribute accessors, iteration, and simple methods on a graph
        that has not had `PipelineGraph.resolve` called on it.
        """
        self.check_base_accessors(self.graph)
        self.assertEqual(
            repr(self.graph.tasks["a"]), "a (lsst.pipe.base.tests.mocks.DynamicTestPipelineTask)"
        )

    def test_sorting(self) -> None:
        """Test sort methods on PipelineGraph."""
        self.assertFalse(self.graph.has_been_sorted)
        self.assertFalse(self.graph.is_sorted)
        self.graph.sort()
        self.check_sorted(self.graph)

    def test_unresolved_xgraph_export(self) -> None:
        """Test exporting an unresolved PipelineGraph to networkx in various
        ways.
        """
        self.check_make_xgraph(self.graph, resolved=False)
        self.check_make_bipartite_xgraph(self.graph, resolved=False)
        self.check_make_task_xgraph(self.graph, resolved=False)
        self.check_make_dataset_type_xgraph(self.graph, resolved=False)

    def test_unresolved_stream_io(self) -> None:
        """Test round-tripping an unresolved PipelineGraph through in-memory
        serialization.
        """
        stream = io.BytesIO()
        self.graph._write_stream(stream)
        stream.seek(0)
        roundtripped = PipelineGraph._read_stream(stream)
        self.check_make_xgraph(roundtripped, resolved=False)

    def test_unresolved_file_io(self) -> None:
        """Test round-tripping an unresolved PipelineGraph through file
        serialization.
        """
        with lsst.utils.tests.getTempFilePath(".json.gz") as filename:
            self.graph._write_uri(filename)
            roundtripped = PipelineGraph._read_uri(filename)
        self.check_make_xgraph(roundtripped, resolved=False)

    def test_unresolved_pickle(self) -> None:
        """Test that unresolved PipelineGraph objects can be pickled."""
        self.check_make_xgraph(pickle.loads(pickle.dumps(self.graph)), resolved=False)

    def test_unresolved_deferred_import_io(self) -> None:
        """Test round-tripping an unresolved PipelineGraph through
        serialization, without immediately importing tasks on read.
        """
        stream = io.BytesIO()
        self.graph._write_stream(stream)
        stream.seek(0)
        roundtripped = PipelineGraph._read_stream(stream, import_mode=TaskImportMode.DO_NOT_IMPORT)
        self.check_make_xgraph(roundtripped, resolved=False, imported_and_configured=False)
        self.check_make_xgraph(
            pickle.loads(pickle.dumps(roundtripped)), resolved=False, imported_and_configured=False
        )
        # Check that we can still resolve the graph without importing tasks.
        roundtripped.resolve(MockRegistry(self.dimensions, {}))
        self.check_make_xgraph(roundtripped, resolved=True, imported_and_configured=False)
        roundtripped._import_and_configure(TaskImportMode.ASSUME_CONSISTENT_EDGES)
        self.check_make_xgraph(roundtripped, resolved=True, imported_and_configured=True)

    def test_resolved_accessors(self) -> None:
        """Test attribute accessors, iteration, and simple methods on a graph
        that has had `PipelineGraph.resolve` called on it.

        This includes the accessors available on unresolved graphs as well as
        new ones, and we expect the resolved graph to be sorted as well.
        """
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        self.check_base_accessors(self.graph)
        self.check_sorted(self.graph)
        self.assertEqual(
            repr(self.graph.tasks["a"]), "a (lsst.pipe.base.tests.mocks.DynamicTestPipelineTask, {})"
        )
        self.assertEqual(self.graph.tasks["a"].dimensions, self.dimensions.empty)
        self.assertEqual(repr(self.graph.dataset_types["input_1"]), "input_1 (_mock_StructuredDataDict, {})")
        self.assertEqual(self.graph.dataset_types["input_1"].key, NodeKey(NodeType.DATASET_TYPE, "input_1"))
        self.assertEqual(self.graph.dataset_types["input_1"].dimensions, self.dimensions.empty)
        self.assertEqual(self.graph.dataset_types["input_1"].storage_class_name, "_mock_StructuredDataDict")
        self.assertEqual(self.graph.dataset_types["input_1"].storage_class.name, "_mock_StructuredDataDict")

    def test_resolved_xgraph_export(self) -> None:
        """Test exporting a resolved PipelineGraph to networkx in various
        ways.
        """
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        self.check_make_xgraph(self.graph, resolved=True)
        self.check_make_bipartite_xgraph(self.graph, resolved=True)
        self.check_make_task_xgraph(self.graph, resolved=True)
        self.check_make_dataset_type_xgraph(self.graph, resolved=True)

    def test_resolved_stream_io(self) -> None:
        """Test round-tripping a resolved PipelineGraph through in-memory
        serialization.
        """
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        stream = io.BytesIO()
        self.graph._write_stream(stream)
        stream.seek(0)
        roundtripped = PipelineGraph._read_stream(stream)
        self.check_make_xgraph(roundtripped, resolved=True)

    def test_resolved_file_io(self) -> None:
        """Test round-tripping a resolved PipelineGraph through file
        serialization.
        """
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        with lsst.utils.tests.getTempFilePath(".json.gz") as filename:
            self.graph._write_uri(filename)
            roundtripped = PipelineGraph._read_uri(filename)
        self.check_make_xgraph(roundtripped, resolved=True)

    def test_resolved_pickle(self) -> None:
        """Test that resolved PipelineGraph objects can be pickled."""
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        self.check_make_xgraph(pickle.loads(pickle.dumps(self.graph)), resolved=True)

    def test_resolved_deferred_import_io(self) -> None:
        """Test round-tripping a resolved PipelineGraph through serialization,
        without immediately importing tasks on read.
        """
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        stream = io.BytesIO()
        self.graph._write_stream(stream)
        stream.seek(0)
        roundtripped = PipelineGraph._read_stream(stream, import_mode=TaskImportMode.DO_NOT_IMPORT)
        self.check_make_xgraph(roundtripped, resolved=True, imported_and_configured=False)
        self.check_make_xgraph(
            pickle.loads(pickle.dumps(roundtripped)), resolved=True, imported_and_configured=False
        )
        roundtripped._import_and_configure(TaskImportMode.REQUIRE_CONSISTENT_EDGES)
        self.check_make_xgraph(roundtripped, resolved=True, imported_and_configured=True)

    def test_unresolved_copies(self) -> None:
        """Test making copies of an unresolved PipelineGraph."""
        copy1 = self.graph.copy()
        self.assertIsNot(copy1, self.graph)
        self.check_make_xgraph(copy1, resolved=False)
        copy2 = copy.copy(self.graph)
        self.assertIsNot(copy2, self.graph)
        self.check_make_xgraph(copy2, resolved=False)
        copy3 = copy.deepcopy(self.graph)
        self.assertIsNot(copy3, self.graph)
        self.check_make_xgraph(copy3, resolved=False)

    def test_resolved_copies(self) -> None:
        """Test making copies of a resolved PipelineGraph."""
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        copy1 = self.graph.copy()
        self.assertIsNot(copy1, self.graph)
        self.check_make_xgraph(copy1, resolved=True)
        copy2 = copy.copy(self.graph)
        self.assertIsNot(copy2, self.graph)
        self.check_make_xgraph(copy2, resolved=True)
        copy3 = copy.deepcopy(self.graph)
        self.assertIsNot(copy3, self.graph)
        self.check_make_xgraph(copy3, resolved=True)

    def check_base_accessors(self, graph: PipelineGraph) -> None:
        """Run parameterized tests that check attribute access, iteration, and
        simple methods.

        The given graph must be unchanged from the one defined in `setUp`,
        other than sorting.
        """
        self.assertEqual(graph.description, self.description)
        self.assertEqual(graph.tasks.keys(), {"a", "b"})
        self.assertEqual(
            graph.dataset_types.keys(),
            {
                "schema",
                "input_1",
                "intermediate_1",
                "output_1",
                "a_config",
                "a_log",
                "a_metadata",
                "b_config",
                "b_log",
                "b_metadata",
            },
        )
        self.assertEqual(graph.task_subsets.keys(), {"only_b"})
        self.assertEqual(
            {edge.nodes + (repr(edge),) for edge in graph.iter_edges(init=False)},
            {
                (
                    NodeKey(NodeType.DATASET_TYPE, "input_1"),
                    NodeKey(NodeType.TASK, "a"),
                    "input_1 -> a (input1)",
                ),
                (
                    NodeKey(NodeType.TASK, "a"),
                    NodeKey(NodeType.DATASET_TYPE, "intermediate_1"),
                    "a -> intermediate_1 (output1)",
                ),
                (
                    NodeKey(NodeType.DATASET_TYPE, "intermediate_1"),
                    NodeKey(NodeType.TASK, "b"),
                    "intermediate_1 -> b (input1)",
                ),
                (
                    NodeKey(NodeType.TASK, "b"),
                    NodeKey(NodeType.DATASET_TYPE, "output_1"),
                    "b -> output_1 (output1)",
                ),
                (NodeKey(NodeType.TASK, "a"), NodeKey(NodeType.DATASET_TYPE, "a_log"), "a -> a_log (_log)"),
                (
                    NodeKey(NodeType.TASK, "a"),
                    NodeKey(NodeType.DATASET_TYPE, "a_metadata"),
                    "a -> a_metadata (_metadata)",
                ),
                (NodeKey(NodeType.TASK, "b"), NodeKey(NodeType.DATASET_TYPE, "b_log"), "b -> b_log (_log)"),
                (
                    NodeKey(NodeType.TASK, "b"),
                    NodeKey(NodeType.DATASET_TYPE, "b_metadata"),
                    "b -> b_metadata (_metadata)",
                ),
            },
        )
        self.assertEqual(
            {edge.nodes + (repr(edge),) for edge in graph.iter_edges(init=True)},
            {
                (
                    NodeKey(NodeType.TASK_INIT, "a"),
                    NodeKey(NodeType.DATASET_TYPE, "schema"),
                    "a -> schema (out_schema)",
                ),
                (
                    NodeKey(NodeType.DATASET_TYPE, "schema"),
                    NodeKey(NodeType.TASK_INIT, "b"),
                    "schema -> b (in_schema)",
                ),
                (
                    NodeKey(NodeType.TASK_INIT, "a"),
                    NodeKey(NodeType.DATASET_TYPE, "a_config"),
                    "a -> a_config (_config)",
                ),
                (
                    NodeKey(NodeType.TASK_INIT, "b"),
                    NodeKey(NodeType.DATASET_TYPE, "b_config"),
                    "b -> b_config (_config)",
                ),
            },
        )
        self.assertEqual(
            {(node_type, name) for node_type, name, _ in graph.iter_nodes()},
            {
                NodeKey(NodeType.TASK, "a"),
                NodeKey(NodeType.TASK, "b"),
                NodeKey(NodeType.TASK_INIT, "a"),
                NodeKey(NodeType.TASK_INIT, "b"),
                NodeKey(NodeType.DATASET_TYPE, "schema"),
                NodeKey(NodeType.DATASET_TYPE, "input_1"),
                NodeKey(NodeType.DATASET_TYPE, "intermediate_1"),
                NodeKey(NodeType.DATASET_TYPE, "output_1"),
                NodeKey(NodeType.DATASET_TYPE, "a_config"),
                NodeKey(NodeType.DATASET_TYPE, "a_log"),
                NodeKey(NodeType.DATASET_TYPE, "a_metadata"),
                NodeKey(NodeType.DATASET_TYPE, "b_config"),
                NodeKey(NodeType.DATASET_TYPE, "b_log"),
                NodeKey(NodeType.DATASET_TYPE, "b_metadata"),
            },
        )
        self.assertEqual({name for name, _ in graph.iter_overall_inputs()}, {"input_1"})
        self.assertEqual({edge.task_label for edge in graph.consuming_edges_of("input_1")}, {"a"})
        self.assertEqual({edge.task_label for edge in graph.consuming_edges_of("intermediate_1")}, {"b"})
        self.assertEqual({edge.task_label for edge in graph.consuming_edges_of("output_1")}, set())
        self.assertEqual({node.label for node in graph.consumers_of("input_1")}, {"a"})
        self.assertEqual({node.label for node in graph.consumers_of("intermediate_1")}, {"b"})
        self.assertEqual({node.label for node in graph.consumers_of("output_1")}, set())

        self.assertIsNone(graph.producing_edge_of("input_1"))
        self.assertEqual(graph.producing_edge_of("intermediate_1").task_label, "a")
        self.assertEqual(graph.producing_edge_of("output_1").task_label, "b")
        self.assertIsNone(graph.producer_of("input_1"))
        self.assertEqual(graph.producer_of("intermediate_1").label, "a")
        self.assertEqual(graph.producer_of("output_1").label, "b")

        self.assertEqual(graph.inputs_of("a").keys(), {"input_1"})
        self.assertEqual(graph.inputs_of("b").keys(), {"intermediate_1"})
        self.assertEqual(graph.inputs_of("a", init=True).keys(), set())
        self.assertEqual(graph.inputs_of("b", init=True).keys(), {"schema"})
        self.assertEqual(graph.outputs_of("a").keys(), {"intermediate_1", "a_log", "a_metadata"})
        self.assertEqual(graph.outputs_of("b").keys(), {"output_1", "b_log", "b_metadata"})
        self.assertEqual(
            graph.outputs_of("a", include_automatic_connections=False).keys(), {"intermediate_1"}
        )
        self.assertEqual(graph.outputs_of("b", include_automatic_connections=False).keys(), {"output_1"})
        self.assertEqual(graph.outputs_of("a", init=True).keys(), {"schema", "a_config"})
        self.assertEqual(
            graph.outputs_of("a", init=True, include_automatic_connections=False).keys(), {"schema"}
        )
        self.assertEqual(graph.outputs_of("b", init=True).keys(), {"b_config"})
        self.assertEqual(graph.outputs_of("b", init=True, include_automatic_connections=False).keys(), set())

        self.assertTrue(repr(self.graph).startswith(f"PipelineGraph({self.description!r}, tasks="))
        self.assertEqual(
            repr(graph.task_subsets["only_b"]), f"only_b: {self.subset_description!r}, tasks={{b}}"
        )

    def check_sorted(self, graph: PipelineGraph) -> None:
        """Run a battery of tests on a PipelineGraph that must be
        deterministically sorted.

        The given graph must be unchanged from the one defined in `setUp`,
        other than sorting.
        """
        self.assertTrue(graph.has_been_sorted)
        self.assertTrue(graph.is_sorted)
        self.assertEqual(
            [(node_type, name) for node_type, name, _ in graph.iter_nodes()],
            [
                # We only advertise that the order is topological and
                # deterministic, so this test is slightly over-specified; there
                # are other orders that are consistent with our guarantees.
                NodeKey(NodeType.DATASET_TYPE, "input_1"),
                NodeKey(NodeType.TASK_INIT, "a"),
                NodeKey(NodeType.DATASET_TYPE, "a_config"),
                NodeKey(NodeType.DATASET_TYPE, "schema"),
                NodeKey(NodeType.TASK_INIT, "b"),
                NodeKey(NodeType.DATASET_TYPE, "b_config"),
                NodeKey(NodeType.TASK, "a"),
                NodeKey(NodeType.DATASET_TYPE, "a_log"),
                NodeKey(NodeType.DATASET_TYPE, "a_metadata"),
                NodeKey(NodeType.DATASET_TYPE, "intermediate_1"),
                NodeKey(NodeType.TASK, "b"),
                NodeKey(NodeType.DATASET_TYPE, "b_log"),
                NodeKey(NodeType.DATASET_TYPE, "b_metadata"),
                NodeKey(NodeType.DATASET_TYPE, "output_1"),
            ],
        )
        # Most users should only care that the tasks and dataset types are
        # topologically sorted.
        self.assertEqual(list(graph.tasks), ["a", "b"])
        self.assertEqual(
            list(graph.dataset_types),
            [
                "input_1",
                "a_config",
                "schema",
                "b_config",
                "a_log",
                "a_metadata",
                "intermediate_1",
                "b_log",
                "b_metadata",
                "output_1",
            ],
        )
        # __str__ and __repr__ of course work on unsorted mapping views, too,
        # but the order of elements is then nondeterministic and hard to test.
        self.assertEqual(repr(self.graph.tasks), "TaskMappingView({a, b})")
        self.assertEqual(
            repr(self.graph.dataset_types),
            (
                "DatasetTypeMappingView({input_1, a_config, schema, b_config, a_log, a_metadata, "
                "intermediate_1, b_log, b_metadata, output_1})"
            ),
        )

    def check_make_xgraph(
        self, graph: PipelineGraph, resolved: bool, imported_and_configured: bool = True
    ) -> None:
        """Check that the given graph exports as expected to networkx.

        The given graph must be unchanged from the one defined in `setUp`,
        other than being resolved (if ``resolved=True``) or round-tripped
        through serialization without tasks being imported (if
        ``imported_and_configured=False``).
        """
        xgraph = graph.make_xgraph()
        expected_edges = (
            {edge.key for edge in graph.iter_edges()}
            | {edge.key for edge in graph.iter_edges(init=True)}
            | {
                (NodeKey(NodeType.TASK_INIT, "a"), NodeKey(NodeType.TASK, "a"), Edge.INIT_TO_TASK_NAME),
                (NodeKey(NodeType.TASK_INIT, "b"), NodeKey(NodeType.TASK, "b"), Edge.INIT_TO_TASK_NAME),
            }
        )
        test_edges = set(xgraph.edges)
        self.assertEqual(test_edges, expected_edges)
        expected_nodes = {
            NodeKey(NodeType.TASK_INIT, "a"): self.get_expected_task_init_node(
                "a", resolved, imported_and_configured=imported_and_configured
            ),
            NodeKey(NodeType.TASK, "a"): self.get_expected_task_node(
                "a", resolved, imported_and_configured=imported_and_configured
            ),
            NodeKey(NodeType.TASK_INIT, "b"): self.get_expected_task_init_node(
                "b", resolved, imported_and_configured=imported_and_configured
            ),
            NodeKey(NodeType.TASK, "b"): self.get_expected_task_node(
                "b", resolved, imported_and_configured=imported_and_configured
            ),
            NodeKey(NodeType.DATASET_TYPE, "a_config"): self.get_expected_config_node("a", resolved),
            NodeKey(NodeType.DATASET_TYPE, "b_config"): self.get_expected_config_node("b", resolved),
            NodeKey(NodeType.DATASET_TYPE, "a_log"): self.get_expected_log_node("a", resolved),
            NodeKey(NodeType.DATASET_TYPE, "b_log"): self.get_expected_log_node("b", resolved),
            NodeKey(NodeType.DATASET_TYPE, "a_metadata"): self.get_expected_metadata_node("a", resolved),
            NodeKey(NodeType.DATASET_TYPE, "b_metadata"): self.get_expected_metadata_node("b", resolved),
            NodeKey(NodeType.DATASET_TYPE, "schema"): self.get_expected_connection_node(
                "schema", resolved, is_initial_query_constraint=False
            ),
            NodeKey(NodeType.DATASET_TYPE, "input_1"): self.get_expected_connection_node(
                "input_1", resolved, is_initial_query_constraint=True
            ),
            NodeKey(NodeType.DATASET_TYPE, "intermediate_1"): self.get_expected_connection_node(
                "intermediate_1", resolved, is_initial_query_constraint=False
            ),
            NodeKey(NodeType.DATASET_TYPE, "output_1"): self.get_expected_connection_node(
                "output_1", resolved, is_initial_query_constraint=False
            ),
        }
        test_nodes = dict(xgraph.nodes.items())
        self.assertEqual(set(test_nodes.keys()), set(expected_nodes.keys()))
        for key, expected_node in expected_nodes.items():
            test_node = test_nodes[key]
            self.assertEqual(expected_node, test_node, key)

    def check_make_bipartite_xgraph(self, graph: PipelineGraph, resolved: bool) -> None:
        """Check that the given graph's init-only or runtime subset exports as
        expected to networkx.

        The given graph must be unchanged from the one defined in `setUp`,
        other than being resolved (if ``resolved=True``).
        """
        run_xgraph = graph.make_bipartite_xgraph()
        self.assertEqual(set(run_xgraph.edges), {edge.key for edge in graph.iter_edges()})
        self.assertEqual(
            dict(run_xgraph.nodes.items()),
            {
                NodeKey(NodeType.TASK, "a"): self.get_expected_task_node("a", resolved),
                NodeKey(NodeType.TASK, "b"): self.get_expected_task_node("b", resolved),
                NodeKey(NodeType.DATASET_TYPE, "a_log"): self.get_expected_log_node("a", resolved),
                NodeKey(NodeType.DATASET_TYPE, "b_log"): self.get_expected_log_node("b", resolved),
                NodeKey(NodeType.DATASET_TYPE, "a_metadata"): self.get_expected_metadata_node("a", resolved),
                NodeKey(NodeType.DATASET_TYPE, "b_metadata"): self.get_expected_metadata_node("b", resolved),
                NodeKey(NodeType.DATASET_TYPE, "input_1"): self.get_expected_connection_node(
                    "input_1", resolved, is_initial_query_constraint=True
                ),
                NodeKey(NodeType.DATASET_TYPE, "intermediate_1"): self.get_expected_connection_node(
                    "intermediate_1", resolved, is_initial_query_constraint=False
                ),
                NodeKey(NodeType.DATASET_TYPE, "output_1"): self.get_expected_connection_node(
                    "output_1", resolved, is_initial_query_constraint=False
                ),
            },
        )
        init_xgraph = graph.make_bipartite_xgraph(
            init=True,
        )
        self.assertEqual(set(init_xgraph.edges), {edge.key for edge in graph.iter_edges(init=True)})
        self.assertEqual(
            dict(init_xgraph.nodes.items()),
            {
                NodeKey(NodeType.TASK_INIT, "a"): self.get_expected_task_init_node("a", resolved),
                NodeKey(NodeType.TASK_INIT, "b"): self.get_expected_task_init_node("b", resolved),
                NodeKey(NodeType.DATASET_TYPE, "schema"): self.get_expected_connection_node(
                    "schema", resolved, is_initial_query_constraint=False
                ),
                NodeKey(NodeType.DATASET_TYPE, "a_config"): self.get_expected_config_node("a", resolved),
                NodeKey(NodeType.DATASET_TYPE, "b_config"): self.get_expected_config_node("b", resolved),
            },
        )

    def check_make_task_xgraph(self, graph: PipelineGraph, resolved: bool) -> None:
        """Check that the given graph's task-only projection exports as
        expected to networkx.

        The given graph must be unchanged from the one defined in `setUp`,
        other than being resolved (if ``resolved=True``).
        """
        run_xgraph = graph.make_task_xgraph()
        self.assertEqual(set(run_xgraph.edges), {(NodeKey(NodeType.TASK, "a"), NodeKey(NodeType.TASK, "b"))})
        self.assertEqual(
            dict(run_xgraph.nodes.items()),
            {
                NodeKey(NodeType.TASK, "a"): self.get_expected_task_node("a", resolved),
                NodeKey(NodeType.TASK, "b"): self.get_expected_task_node("b", resolved),
            },
        )
        init_xgraph = graph.make_task_xgraph(
            init=True,
        )
        self.assertEqual(
            set(init_xgraph.edges),
            {(NodeKey(NodeType.TASK_INIT, "a"), NodeKey(NodeType.TASK_INIT, "b"))},
        )
        self.assertEqual(
            dict(init_xgraph.nodes.items()),
            {
                NodeKey(NodeType.TASK_INIT, "a"): self.get_expected_task_init_node("a", resolved),
                NodeKey(NodeType.TASK_INIT, "b"): self.get_expected_task_init_node("b", resolved),
            },
        )

    def check_make_dataset_type_xgraph(self, graph: PipelineGraph, resolved: bool) -> None:
        """Check that the given graph's dataset-type-only projection exports as
        expected to networkx.

        The given graph must be unchanged from the one defined in `setUp`,
        other than being resolved (if ``resolved=True``).
        """
        run_xgraph = graph.make_dataset_type_xgraph()
        self.assertEqual(
            set(run_xgraph.edges),
            {
                (NodeKey(NodeType.DATASET_TYPE, "input_1"), NodeKey(NodeType.DATASET_TYPE, "intermediate_1")),
                (NodeKey(NodeType.DATASET_TYPE, "input_1"), NodeKey(NodeType.DATASET_TYPE, "a_log")),
                (NodeKey(NodeType.DATASET_TYPE, "input_1"), NodeKey(NodeType.DATASET_TYPE, "a_metadata")),
                (
                    NodeKey(NodeType.DATASET_TYPE, "intermediate_1"),
                    NodeKey(NodeType.DATASET_TYPE, "output_1"),
                ),
                (NodeKey(NodeType.DATASET_TYPE, "intermediate_1"), NodeKey(NodeType.DATASET_TYPE, "b_log")),
                (
                    NodeKey(NodeType.DATASET_TYPE, "intermediate_1"),
                    NodeKey(NodeType.DATASET_TYPE, "b_metadata"),
                ),
            },
        )
        self.assertEqual(
            dict(run_xgraph.nodes.items()),
            {
                NodeKey(NodeType.DATASET_TYPE, "a_log"): self.get_expected_log_node("a", resolved),
                NodeKey(NodeType.DATASET_TYPE, "b_log"): self.get_expected_log_node("b", resolved),
                NodeKey(NodeType.DATASET_TYPE, "a_metadata"): self.get_expected_metadata_node("a", resolved),
                NodeKey(NodeType.DATASET_TYPE, "b_metadata"): self.get_expected_metadata_node("b", resolved),
                NodeKey(NodeType.DATASET_TYPE, "input_1"): self.get_expected_connection_node(
                    "input_1", resolved, is_initial_query_constraint=True
                ),
                NodeKey(NodeType.DATASET_TYPE, "intermediate_1"): self.get_expected_connection_node(
                    "intermediate_1", resolved, is_initial_query_constraint=False
                ),
                NodeKey(NodeType.DATASET_TYPE, "output_1"): self.get_expected_connection_node(
                    "output_1", resolved, is_initial_query_constraint=False
                ),
            },
        )
        init_xgraph = graph.make_dataset_type_xgraph(init=True)
        self.assertEqual(
            set(init_xgraph.edges),
            {(NodeKey(NodeType.DATASET_TYPE, "schema"), NodeKey(NodeType.DATASET_TYPE, "b_config"))},
        )
        self.assertEqual(
            dict(init_xgraph.nodes.items()),
            {
                NodeKey(NodeType.DATASET_TYPE, "schema"): self.get_expected_connection_node(
                    "schema", resolved, is_initial_query_constraint=False
                ),
                NodeKey(NodeType.DATASET_TYPE, "a_config"): self.get_expected_config_node("a", resolved),
                NodeKey(NodeType.DATASET_TYPE, "b_config"): self.get_expected_config_node("b", resolved),
            },
        )

    def get_expected_task_node(
        self, label: str, resolved: bool, imported_and_configured: bool = True
    ) -> dict[str, Any]:
        """Construct a networkx-export task node for comparison."""
        result = self.get_expected_task_init_node(
            label, resolved, imported_and_configured=imported_and_configured
        )
        if resolved:
            result["dimensions"] = self.dimensions.empty
        result["raw_dimensions"] = frozenset()
        return result

    def get_expected_task_init_node(
        self, label: str, resolved: bool, imported_and_configured: bool = True
    ) -> dict[str, Any]:
        """Construct a networkx-export task init for comparison."""
        result = {
            "task_class_name": "lsst.pipe.base.tests.mocks.DynamicTestPipelineTask",
            "bipartite": 1,
        }
        if imported_and_configured:
            result["task_class"] = DynamicTestPipelineTask
            result["config"] = getattr(self, f"{label}_config")
        return result

    def get_expected_config_node(self, label: str, resolved: bool) -> dict[str, Any]:
        """Construct a networkx-export init-output config dataset type node for
        comparison.
        """
        if not resolved:
            return {"bipartite": 0}
        else:
            return {
                "dataset_type": DatasetType(
                    acc.CONFIG_INIT_OUTPUT_TEMPLATE.format(label=label),
                    self.dimensions.empty,
                    acc.CONFIG_INIT_OUTPUT_STORAGE_CLASS,
                ),
                "is_initial_query_constraint": False,
                "is_prerequisite": False,
                "dimensions": self.dimensions.empty,
                "storage_class_name": acc.CONFIG_INIT_OUTPUT_STORAGE_CLASS,
                "bipartite": 0,
            }

    def get_expected_log_node(self, label: str, resolved: bool) -> dict[str, Any]:
        """Construct a networkx-export output log dataset type node for
        comparison.
        """
        if not resolved:
            return {"bipartite": 0}
        else:
            return {
                "dataset_type": DatasetType(
                    acc.LOG_OUTPUT_TEMPLATE.format(label=label),
                    self.dimensions.empty,
                    acc.LOG_OUTPUT_STORAGE_CLASS,
                ),
                "is_initial_query_constraint": False,
                "is_prerequisite": False,
                "dimensions": self.dimensions.empty,
                "storage_class_name": acc.LOG_OUTPUT_STORAGE_CLASS,
                "bipartite": 0,
            }

    def get_expected_metadata_node(self, label: str, resolved: bool) -> dict[str, Any]:
        """Construct a networkx-export output metadata dataset type node for
        comparison.
        """
        if not resolved:
            return {"bipartite": 0}
        else:
            return {
                "dataset_type": DatasetType(
                    acc.METADATA_OUTPUT_TEMPLATE.format(label=label),
                    self.dimensions.empty,
                    acc.METADATA_OUTPUT_STORAGE_CLASS,
                ),
                "is_initial_query_constraint": False,
                "is_prerequisite": False,
                "dimensions": self.dimensions.empty,
                "storage_class_name": acc.METADATA_OUTPUT_STORAGE_CLASS,
                "bipartite": 0,
            }

    def get_expected_connection_node(
        self, name: str, resolved: bool, *, is_initial_query_constraint: bool
    ) -> dict[str, Any]:
        """Construct a networkx-export dataset type node for comparison."""
        if not resolved:
            return {"bipartite": 0}
        else:
            return {
                "dataset_type": DatasetType(
                    name,
                    self.dimensions.empty,
                    get_mock_name("StructuredDataDict"),
                ),
                "is_initial_query_constraint": is_initial_query_constraint,
                "is_prerequisite": False,
                "dimensions": self.dimensions.empty,
                "storage_class_name": get_mock_name("StructuredDataDict"),
                "bipartite": 0,
            }

    def test_construct_with_data_coordinate(self) -> None:
        """Test constructing a graph with a DataCoordinate.

        Since this creates a graph with DimensionUniverse, all tasks added to
        it should have resolved dimensions, but not (yet) resolved dataset
        types.  We use that to test a few other operations in that state.
        """
        data_id = DataCoordinate.standardize(instrument="I", universe=self.dimensions)
        graph = PipelineGraph(data_id=data_id)
        self.assertEqual(graph.universe, self.dimensions)
        self.assertEqual(graph.data_id, data_id)
        graph.add_task("b1", DynamicTestPipelineTask, self.b_config)
        self.assertEqual(graph.tasks["b1"].dimensions, self.dimensions.empty)
        # Still can't group by dimensions, because the dataset types aren't
        # resolved.
        with self.assertRaises(UnresolvedGraphError):
            graph.group_by_dimensions()
        # Transferring a node from this graph to ``self.graph`` should
        # unresolve the dimensions.
        self.graph.add_task_nodes([graph.tasks["b1"]])
        self.assertIsNot(self.graph.tasks["b1"], graph.tasks["b1"])
        self.assertFalse(self.graph.tasks["b1"].has_resolved_dimensions)
        # Do the opposite transfer, which should resolve dimensions.
        graph.add_task_nodes([self.graph.tasks["a"]])
        self.assertIsNot(self.graph.tasks["a"], graph.tasks["a"])
        self.assertTrue(graph.tasks["a"].has_resolved_dimensions)

    def test_group_by_dimensions(self) -> None:
        """Test PipelineGraph.group_by_dimensions."""
        with self.assertRaises(UnresolvedGraphError):
            self.graph.group_by_dimensions()
        self.a_config.dimensions = ["visit"]
        self.a_config.outputs["output1"].dimensions = ["visit"]
        self.a_config.prerequisite_inputs["prereq1"] = DynamicConnectionConfig(
            dataset_type_name="prereq_1",
            multiple=True,
            dimensions=["htm7"],
            is_calibration=True,
        )
        self.b_config.dimensions = ["htm7"]
        self.b_config.inputs["input1"].dimensions = ["visit"]
        self.b_config.inputs["input1"].multiple = True
        self.b_config.outputs["output1"].dimensions = ["htm7"]
        self.graph.reconfigure_tasks(a=self.a_config, b=self.b_config)
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        visit_dims = self.dimensions.conform(["visit"])
        htm7_dims = self.dimensions.conform(["htm7"])
        expected = {
            self.dimensions.empty.as_group(): (
                {},
                {
                    "schema": self.graph.dataset_types["schema"],
                    "input_1": self.graph.dataset_types["input_1"],
                    "a_config": self.graph.dataset_types["a_config"],
                    "b_config": self.graph.dataset_types["b_config"],
                },
            ),
            visit_dims: (
                {"a": self.graph.tasks["a"]},
                {
                    "a_log": self.graph.dataset_types["a_log"],
                    "a_metadata": self.graph.dataset_types["a_metadata"],
                    "intermediate_1": self.graph.dataset_types["intermediate_1"],
                },
            ),
            htm7_dims: (
                {"b": self.graph.tasks["b"]},
                {
                    "b_log": self.graph.dataset_types["b_log"],
                    "b_metadata": self.graph.dataset_types["b_metadata"],
                    "output_1": self.graph.dataset_types["output_1"],
                },
            ),
        }
        self.assertEqual(self.graph.group_by_dimensions(), expected)
        expected[htm7_dims][1]["prereq_1"] = self.graph.dataset_types["prereq_1"]
        self.assertEqual(self.graph.group_by_dimensions(prerequisites=True), expected)

    def test_add_and_remove(self) -> None:
        """Tests for adding and removing tasks and task subsets from a
        PipelineGraph.
        """
        original = self.graph.copy()
        # Can't remove a task while it's still in a subset.
        with self.assertRaises(PipelineGraphError):
            self.graph.remove_tasks(["b"], drop_from_subsets=False)
        self.assertEqual(original.diff_tasks(self.graph), [])
        # ...unless you remove the subset.
        self.graph.remove_task_subset("only_b")
        self.assertFalse(self.graph.task_subsets)
        ((b, referencing_subsets),) = self.graph.remove_tasks(["b"], drop_from_subsets=False)
        self.assertFalse(referencing_subsets)
        self.assertEqual(self.graph.tasks.keys(), {"a"})
        self.assertEqual(
            original.diff_tasks(self.graph),
            ["Pipelines have different tasks: A & ~B = ['b'], B & ~A = []."],
        )
        # Add that task back in.
        self.graph.add_task_nodes([b])
        self.assertEqual(self.graph.tasks.keys(), {"a", "b"})
        # Add the subset back in.
        self.graph.add_task_subset("only_b", {"b"})
        self.assertEqual(self.graph.task_subsets.keys(), {"only_b"})
        # Resolve the graph's dataset types and task dimensions.
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        self.assertTrue(self.graph.dataset_types.is_resolved("input_1"))
        self.assertTrue(self.graph.dataset_types.is_resolved("output_1"))
        self.assertTrue(self.graph.dataset_types.is_resolved("schema"))
        self.assertTrue(self.graph.dataset_types.is_resolved("intermediate_1"))
        # Remove the task while removing it from the subset automatically. This
        # should also unresolve (only) the referenced dataset types and drop
        # any datasets no longer attached to any task.
        self.assertEqual(self.graph.tasks.keys(), {"a", "b"})
        ((b, referencing_subsets),) = self.graph.remove_tasks(["b"], drop_from_subsets=True)
        self.assertEqual(referencing_subsets, {"only_b"})
        self.assertEqual(self.graph.tasks.keys(), {"a"})
        self.assertTrue(self.graph.dataset_types.is_resolved("input_1"))
        self.assertNotIn("output1", self.graph.dataset_types)
        self.assertFalse(self.graph.dataset_types.is_resolved("schema"))
        self.assertFalse(self.graph.dataset_types.is_resolved("intermediate_1"))

    def test_reconfigure(self) -> None:
        """Tests for PipelineGraph.reconfigure."""
        original = self.graph.copy()
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        self.b_config.outputs["output1"].storage_class = "TaskMetadata"
        with self.assertRaises(ValueError):
            # Can't check and assume together.
            self.graph.reconfigure_tasks(
                b=self.b_config, assume_edges_unchanged=True, check_edges_unchanged=True
            )
        # Check that graph is unchanged after error.
        self.check_base_accessors(self.graph)
        with self.assertRaises(EdgesChangedError):
            self.graph.reconfigure_tasks(b=self.b_config, check_edges_unchanged=True)
        self.check_base_accessors(self.graph)
        self.assertEqual(original.diff_tasks(self.graph), [])
        # Make a change that does affect edges; this will unresolve most
        # dataset types.
        self.graph.reconfigure_tasks(b=self.b_config)
        self.assertTrue(self.graph.dataset_types.is_resolved("input_1"))
        self.assertFalse(self.graph.dataset_types.is_resolved("output_1"))
        self.assertFalse(self.graph.dataset_types.is_resolved("schema"))
        self.assertFalse(self.graph.dataset_types.is_resolved("intermediate_1"))
        self.assertEqual(
            original.diff_tasks(self.graph),
            [
                "Output b.output1 has storage class '_mock_StructuredDataDict' in A, "
                "but '_mock_TaskMetadata' in B."
            ],
        )
        # Resolving again will pick up the new storage class
        self.graph.resolve(MockRegistry(self.dimensions, {}))
        self.assertEqual(
            self.graph.dataset_types["output_1"].storage_class_name, get_mock_name("TaskMetadata")
        )

    def check_visualization(self, graph: PipelineGraph, expected: str, **kwargs: Any) -> None:
        """Run pipeline graph visualization with the given kwargs and check
        that the output is the given expected string.

        Parameters
        ----------
        graph : `lsst.pipe.base.pipeline_graph.PipelineGraph`
            Pipeline graph to visualize.
        expected : `str`
            Expected output of the visualization.  Will be passed through
            `textwrap.dedent`, to allow it to be written with triple-quotes.
        **kwargs
            Forwarded to `lsst.pipe.base.pipeline_graph.visualization.show`.
        """
        stream = io.StringIO()
        visualization.show(graph, stream, **kwargs)
        self.assertEqual(textwrap.dedent(expected), stream.getvalue())

    def test_unresolved_visualization(self) -> None:
        """Test pipeline graph text-based visualization on unresolved
        graphs.
        """
        self.check_visualization(
            self.graph,
            """
            ■  a
            │
            ■  b
            """,
            merge_input_trees=0,
            merge_output_trees=0,
            merge_intermediates=False,
        )
        self.check_visualization(
            self.graph,
            """
            ○  input_1
            │
            ■  a
            │
            ○  intermediate_1
            │
            ■  b
            │
            ○  output_1
            """,
            dataset_types=True,
        )

    def test_resolved_visualization(self) -> None:
        """Test pipeline graph text-based visualization on resolved graphs."""
        self.graph.resolve(MockRegistry(dimensions=self.dimensions, dataset_types={}))
        self.check_visualization(
            self.graph,
            """
            ■  a: {} DynamicTestPipelineTask
            │
            ■  b: {} DynamicTestPipelineTask
            """,
            task_classes="concise",
            merge_input_trees=0,
            merge_output_trees=0,
            merge_intermediates=False,
        )
        self.check_visualization(
            self.graph,
            """
            ○  input_1: {} _mock_StructuredDataDict
            │
            ■  a: {} lsst.pipe.base.tests.mocks.DynamicTestPipelineTask
            │
            ○  intermediate_1: {} _mock_StructuredDataDict
            │
            ■  b: {} lsst.pipe.base.tests.mocks.DynamicTestPipelineTask
            │
            ○  output_1: {} _mock_StructuredDataDict
            """,
            task_classes="full",
            dataset_types=True,
        )


def _have_example_storage_classes() -> bool:
    """Check whether some storage classes work as expected.

    Given that these have registered converters, it shouldn't actually be
    necessary to import be able to those types in order to determine that
    they're convertible, but the storage class machinery is implemented such
    that types that can't be imported can't be converted, and while that's
    inconvenient here it's totally fine in non-testing scenarios where you only
    care about a storage class if you can actually use it.
    """
    getter = StorageClassFactory().getStorageClass
    return (
        getter("ArrowTable").can_convert(getter("ArrowAstropy"))
        and getter("ArrowAstropy").can_convert(getter("ArrowTable"))
        and getter("ArrowTable").can_convert(getter("DataFrame"))
        and getter("DataFrame").can_convert(getter("ArrowTable"))
    )


class PipelineGraphResolveTestCase(unittest.TestCase):
    """More extensive tests for PipelineGraph.resolve and its primate helper
    methods.

    These are in a separate TestCase because they utilize a different `setUp`
    from the rest of the `PipelineGraph` tests.
    """

    def setUp(self) -> None:
        self.a_config = DynamicTestPipelineTaskConfig()
        self.b_config = DynamicTestPipelineTaskConfig()
        self.dimensions = DimensionUniverse()
        self.maxDiff = None

    def make_graph(self) -> PipelineGraph:
        graph = PipelineGraph()
        graph.add_task("a", DynamicTestPipelineTask, self.a_config)
        graph.add_task("b", DynamicTestPipelineTask, self.b_config)
        return graph

    def test_prerequisite_inconsistency(self) -> None:
        """Test that we raise an exception when one edge defines a dataset type
        as a prerequisite and another does not.

        This test will hopefully someday go away (along with
        `DatasetTypeNode.is_prerequisite`) when the QuantumGraph generation
        algorithm becomes more flexible.
        """
        self.a_config.prerequisite_inputs["p"] = DynamicConnectionConfig(dataset_type_name="d")
        self.b_config.inputs["i"] = DynamicConnectionConfig(dataset_type_name="d")
        graph = self.make_graph()
        with self.assertRaises(ConnectionTypeConsistencyError):
            graph.resolve(MockRegistry(self.dimensions, {}))

    def test_prerequisite_inconsistency_reversed(self) -> None:
        """Same as `test_prerequisite_inconsistency`, with the order the edges
        are added to the graph reversed.
        """
        self.a_config.inputs["i"] = DynamicConnectionConfig(dataset_type_name="d")
        self.b_config.prerequisite_inputs["p"] = DynamicConnectionConfig(dataset_type_name="d")
        graph = self.make_graph()
        with self.assertRaises(ConnectionTypeConsistencyError):
            graph.resolve(MockRegistry(self.dimensions, {}))

    def test_prerequisite_output(self) -> None:
        """Test that we raise an exception when one edge defines a dataset type
        as a prerequisite but another defines it as an output.
        """
        self.a_config.prerequisite_inputs["p"] = DynamicConnectionConfig(dataset_type_name="d")
        self.b_config.outputs["o"] = DynamicConnectionConfig(dataset_type_name="d")
        graph = self.make_graph()
        with self.assertRaises(ConnectionTypeConsistencyError):
            graph.resolve(MockRegistry(self.dimensions, {}))

    def test_skypix_missing(self) -> None:
        """Test that we raise an exception when one edge uses the "skypix"
        dimension as a placeholder but the dataset type is not registered.
        """
        self.a_config.prerequisite_inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d", dimensions={"skypix"}
        )
        graph = self.make_graph()
        with self.assertRaises(MissingDatasetTypeError):
            graph.resolve(MockRegistry(self.dimensions, {}))

    def test_skypix_inconsistent(self) -> None:
        """Test that we raise an exception when one edge uses the "skypix"
        dimension as a placeholder but the rest of the dimensions are
        inconsistent with the registered dataset type.
        """
        self.a_config.prerequisite_inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d", dimensions={"skypix", "visit"}
        )
        graph = self.make_graph()
        with self.assertRaises(IncompatibleDatasetTypeError):
            graph.resolve(
                MockRegistry(
                    self.dimensions,
                    {
                        "d": DatasetType(
                            "d",
                            dimensions=self.dimensions.conform(["htm7"]),
                            storageClass="StructuredDataDict",
                        )
                    },
                )
            )
        with self.assertRaises(IncompatibleDatasetTypeError):
            graph.resolve(
                MockRegistry(
                    self.dimensions,
                    {
                        "d": DatasetType(
                            "d",
                            dimensions=self.dimensions.conform(["htm7", "visit", "skymap"]),
                            storageClass="StructuredDataDict",
                        )
                    },
                )
            )

    def test_duplicate_outputs(self) -> None:
        """Test that we raise an exception when a dataset type node would have
        two write edges.
        """
        self.a_config.outputs["o"] = DynamicConnectionConfig(dataset_type_name="d")
        self.b_config.outputs["o"] = DynamicConnectionConfig(dataset_type_name="d")
        graph = self.make_graph()
        with self.assertRaises(DuplicateOutputError):
            graph.resolve(MockRegistry(self.dimensions, {}))

    def test_component_of_unregistered_parent(self) -> None:
        """Test that we raise an exception when a component dataset type's
        parent is not registered.
        """
        self.a_config.inputs["i"] = DynamicConnectionConfig(dataset_type_name="d.c")
        graph = self.make_graph()
        with self.assertRaises(MissingDatasetTypeError):
            graph.resolve(MockRegistry(self.dimensions, {}))

    def test_undefined_component(self) -> None:
        """Test that we raise an exception when a component dataset type's
        parent is registered, but its storage class does not have that
        component.
        """
        self.a_config.inputs["i"] = DynamicConnectionConfig(dataset_type_name="d.c")
        graph = self.make_graph()
        with self.assertRaises(IncompatibleDatasetTypeError):
            graph.resolve(
                MockRegistry(
                    self.dimensions,
                    {"d": DatasetType("d", self.dimensions.empty, get_mock_name("StructuredDataDict"))},
                )
            )

    @unittest.skipUnless(
        _have_example_storage_classes(), "Arrow/Astropy/Pandas storage classes are not available."
    )
    def test_bad_component_storage_class(self) -> None:
        """Test that we raise an exception when a component dataset type's
        parent is registered, but does not have that component.
        """
        self.a_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d.schema", storage_class="StructuredDataDict"
        )
        graph = self.make_graph()
        with self.assertRaises(IncompatibleDatasetTypeError):
            graph.resolve(
                MockRegistry(
                    self.dimensions,
                    {"d": DatasetType("d", self.dimensions.empty, get_mock_name("ArrowTable"))},
                )
            )

    def test_input_storage_class_incompatible_with_registry(self) -> None:
        """Test that we raise an exception when an input connection's storage
        class is incompatible with the registry definition.
        """
        self.a_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="StructuredDataList"
        )
        graph = self.make_graph()
        with self.assertRaises(IncompatibleDatasetTypeError):
            graph.resolve(
                MockRegistry(
                    self.dimensions,
                    {"d": DatasetType("d", self.dimensions.empty, get_mock_name("StructuredDataDict"))},
                )
            )

    def test_output_storage_class_incompatible_with_registry(self) -> None:
        """Test that we raise an exception when an output connection's storage
        class is incompatible with the registry definition.
        """
        self.a_config.outputs["o"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="StructuredDataList"
        )
        graph = self.make_graph()
        with self.assertRaises(IncompatibleDatasetTypeError):
            graph.resolve(
                MockRegistry(
                    self.dimensions,
                    {"d": DatasetType("d", self.dimensions.empty, get_mock_name("StructuredDataDict"))},
                )
            )

    def test_input_storage_class_incompatible_with_output(self) -> None:
        """Test that we raise an exception when an input connection's storage
        class is incompatible with the storage class of the output connection.
        """
        self.a_config.outputs["o"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="StructuredDataDict"
        )
        self.b_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="StructuredDataList"
        )
        graph = self.make_graph()
        with self.assertRaises(IncompatibleDatasetTypeError):
            graph.resolve(MockRegistry(self.dimensions, {}))

    def test_ambiguous_storage_class(self) -> None:
        """Test that we raise an exception when two input connections define
        the same dataset with different storage classes (even compatible ones)
        and there is no output connection or registry definition to take
        precedence.
        """
        self.a_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="StructuredDataDict"
        )
        self.b_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="StructuredDataList"
        )
        graph = self.make_graph()
        with self.assertRaises(MissingDatasetTypeError):
            graph.resolve(MockRegistry(self.dimensions, {}))

    @unittest.skipUnless(
        _have_example_storage_classes(), "Arrow/Astropy/Pandas storage classes are not available."
    )
    def test_inputs_compatible_with_registry(self) -> None:
        """Test successful resolution of a dataset type where input edges have
        different but compatible storage classes and the dataset type is
        already registered.
        """
        self.a_config.inputs["i"] = DynamicConnectionConfig(dataset_type_name="d", storage_class="ArrowTable")
        self.b_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="ArrowAstropy"
        )
        graph = self.make_graph()
        dataset_type = DatasetType("d", self.dimensions.empty, get_mock_name("DataFrame"))
        graph.resolve(MockRegistry(self.dimensions, {"d": dataset_type}))
        self.assertEqual(graph.dataset_types["d"].dataset_type, dataset_type)
        a_i = graph.tasks["a"].inputs["i"]
        b_i = graph.tasks["b"].inputs["i"]
        self.assertEqual(
            a_i.adapt_dataset_type(dataset_type),
            dataset_type.overrideStorageClass(get_mock_name("ArrowTable")),
        )
        self.assertEqual(
            b_i.adapt_dataset_type(dataset_type),
            dataset_type.overrideStorageClass(get_mock_name("ArrowAstropy")),
        )
        data_id = DataCoordinate.make_empty(self.dimensions)
        ref = DatasetRef(dataset_type, data_id, run="r")
        a_ref = a_i.adapt_dataset_ref(ref)
        b_ref = b_i.adapt_dataset_ref(ref)
        self.assertEqual(a_ref, ref.overrideStorageClass(get_mock_name("ArrowTable")))
        self.assertEqual(b_ref, ref.overrideStorageClass(get_mock_name("ArrowAstropy")))
        self.assertEqual(graph.dataset_types["d"].generalize_ref(a_ref), ref)
        self.assertEqual(graph.dataset_types["d"].generalize_ref(b_ref), ref)

    @unittest.skipUnless(
        _have_example_storage_classes(), "Arrow/Astropy/Pandas storage classes are not available."
    )
    def test_output_compatible_with_registry(self) -> None:
        """Test successful resolution of a dataset type where an output edge
        has a different but compatible storage class from the dataset type
        already registered.
        """
        self.a_config.outputs["o"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="ArrowTable"
        )
        graph = self.make_graph()
        dataset_type = DatasetType("d", self.dimensions.empty, get_mock_name("DataFrame"))
        graph.resolve(MockRegistry(self.dimensions, {"d": dataset_type}))
        self.assertEqual(graph.dataset_types["d"].dataset_type, dataset_type)
        a_o = graph.tasks["a"].outputs["o"]
        self.assertEqual(
            a_o.adapt_dataset_type(dataset_type),
            dataset_type.overrideStorageClass(get_mock_name("ArrowTable")),
        )
        data_id = DataCoordinate.make_empty(self.dimensions)
        ref = DatasetRef(dataset_type, data_id, run="r")
        a_ref = a_o.adapt_dataset_ref(ref)
        self.assertEqual(a_ref, ref.overrideStorageClass(get_mock_name("ArrowTable")))
        self.assertEqual(graph.dataset_types["d"].generalize_ref(a_ref), ref)

    @unittest.skipUnless(
        _have_example_storage_classes(), "Arrow/Astropy/Pandas storage classes are not available."
    )
    def test_inputs_compatible_with_output(self) -> None:
        """Test successful resolution of a dataset type where an input edge has
        a different but compatible storage class from the output edge, and
        the dataset type is not registered.
        """
        self.a_config.outputs["o"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="ArrowTable"
        )
        self.b_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="ArrowAstropy"
        )
        graph = self.make_graph()
        a_o = graph.tasks["a"].outputs["o"]
        b_i = graph.tasks["b"].inputs["i"]
        graph.resolve(MockRegistry(self.dimensions, {}))
        self.assertEqual(graph.dataset_types["d"].storage_class_name, get_mock_name("ArrowTable"))
        self.assertEqual(
            a_o.adapt_dataset_type(graph.dataset_types["d"].dataset_type),
            graph.dataset_types["d"].dataset_type,
        )
        self.assertEqual(
            b_i.adapt_dataset_type(graph.dataset_types["d"].dataset_type),
            graph.dataset_types["d"].dataset_type.overrideStorageClass(get_mock_name("ArrowAstropy")),
        )
        data_id = DataCoordinate.make_empty(self.dimensions)
        ref = DatasetRef(graph.dataset_types["d"].dataset_type, data_id, run="r")
        a_ref = a_o.adapt_dataset_ref(ref)
        b_ref = b_i.adapt_dataset_ref(ref)
        self.assertEqual(a_ref, ref)
        self.assertEqual(b_ref, ref.overrideStorageClass(get_mock_name("ArrowAstropy")))
        self.assertEqual(graph.dataset_types["d"].generalize_ref(a_ref), ref)
        self.assertEqual(graph.dataset_types["d"].generalize_ref(b_ref), ref)

    @unittest.skipUnless(
        _have_example_storage_classes(), "Arrow/Astropy/Pandas storage classes are not available."
    )
    def test_component_resolved_by_input(self) -> None:
        """Test successful resolution of a component dataset type due to
        another input referencing the parent dataset type.
        """
        self.a_config.inputs["i"] = DynamicConnectionConfig(dataset_type_name="d", storage_class="ArrowTable")
        self.b_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d.schema", storage_class="ArrowSchema"
        )
        graph = self.make_graph()
        parent_dataset_type = DatasetType("d", self.dimensions.empty, get_mock_name("ArrowTable"))
        graph.resolve(MockRegistry(self.dimensions, {}))
        self.assertEqual(graph.dataset_types["d"].dataset_type, parent_dataset_type)
        a_i = graph.tasks["a"].inputs["i"]
        b_i = graph.tasks["b"].inputs["i"]
        self.assertEqual(b_i.dataset_type_name, "d.schema")
        self.assertEqual(a_i.adapt_dataset_type(parent_dataset_type), parent_dataset_type)
        self.assertEqual(
            b_i.adapt_dataset_type(parent_dataset_type),
            parent_dataset_type.makeComponentDatasetType("schema"),
        )
        data_id = DataCoordinate.make_empty(self.dimensions)
        ref = DatasetRef(parent_dataset_type, data_id, run="r")
        a_ref = a_i.adapt_dataset_ref(ref)
        b_ref = b_i.adapt_dataset_ref(ref)
        self.assertEqual(a_ref, ref)
        self.assertEqual(b_ref, ref.makeComponentRef("schema"))
        self.assertEqual(graph.dataset_types["d"].generalize_ref(a_ref), ref)
        self.assertEqual(graph.dataset_types["d"].generalize_ref(b_ref), ref)

    @unittest.skipUnless(
        _have_example_storage_classes(), "Arrow/Astropy/Pandas storage classes are not available."
    )
    def test_component_resolved_by_output(self) -> None:
        """Test successful resolution of a component dataset type due to
        an output connection referencing the parent dataset type.
        """
        self.a_config.outputs["o"] = DynamicConnectionConfig(
            dataset_type_name="d", storage_class="ArrowTable"
        )
        self.b_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d.schema", storage_class="ArrowSchema"
        )
        graph = self.make_graph()
        parent_dataset_type = DatasetType("d", self.dimensions.empty, get_mock_name("ArrowTable"))
        graph.resolve(MockRegistry(self.dimensions, {}))
        self.assertEqual(graph.dataset_types["d"].dataset_type, parent_dataset_type)
        a_o = graph.tasks["a"].outputs["o"]
        b_i = graph.tasks["b"].inputs["i"]
        self.assertEqual(b_i.dataset_type_name, "d.schema")
        self.assertEqual(a_o.adapt_dataset_type(parent_dataset_type), parent_dataset_type)
        self.assertEqual(
            b_i.adapt_dataset_type(parent_dataset_type),
            parent_dataset_type.makeComponentDatasetType("schema"),
        )
        data_id = DataCoordinate.make_empty(self.dimensions)
        ref = DatasetRef(parent_dataset_type, data_id, run="r")
        a_ref = a_o.adapt_dataset_ref(ref)
        b_ref = b_i.adapt_dataset_ref(ref)
        self.assertEqual(a_ref, ref)
        self.assertEqual(b_ref, ref.makeComponentRef("schema"))
        self.assertEqual(graph.dataset_types["d"].generalize_ref(a_ref), ref)
        self.assertEqual(graph.dataset_types["d"].generalize_ref(b_ref), ref)

    @unittest.skipUnless(
        _have_example_storage_classes(), "Arrow/Astropy/Pandas storage classes are not available."
    )
    def test_component_resolved_by_registry(self) -> None:
        """Test successful resolution of a component dataset type due to
        the parent dataset type already being registered.
        """
        self.b_config.inputs["i"] = DynamicConnectionConfig(
            dataset_type_name="d.schema", storage_class="ArrowSchema"
        )
        graph = self.make_graph()
        parent_dataset_type = DatasetType("d", self.dimensions.empty, get_mock_name("ArrowTable"))
        graph.resolve(MockRegistry(self.dimensions, {"d": parent_dataset_type}))
        self.assertEqual(graph.dataset_types["d"].dataset_type, parent_dataset_type)
        b_i = graph.tasks["b"].inputs["i"]
        self.assertEqual(b_i.dataset_type_name, "d.schema")
        self.assertEqual(
            b_i.adapt_dataset_type(parent_dataset_type),
            parent_dataset_type.makeComponentDatasetType("schema"),
        )
        data_id = DataCoordinate.make_empty(self.dimensions)
        ref = DatasetRef(parent_dataset_type, data_id, run="r")
        b_ref = b_i.adapt_dataset_ref(ref)
        self.assertEqual(b_ref, ref.makeComponentRef("schema"))
        self.assertEqual(graph.dataset_types["d"].generalize_ref(b_ref), ref)


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
