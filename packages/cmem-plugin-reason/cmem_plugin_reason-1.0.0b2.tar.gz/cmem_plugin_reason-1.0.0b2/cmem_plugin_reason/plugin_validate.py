"""Ontology consistency validation workflow plugin module"""

import shlex
from datetime import UTC, datetime
from pathlib import Path
from subprocess import run
from time import time
from uuid import uuid4

import validators.url
from cmem.cmempy.dp.proxy.graph import get
from cmem.cmempy.workspace.projects.resources.resource import create_resource
from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Icon, Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities,
    Entity,
    EntityPath,
    EntitySchema,
)
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.types import BoolParameterType, StringParameterType
from cmem_plugin_base.dataintegration.utils import setup_cmempy_user_access
from pathvalidate import is_valid_filename

from cmem_plugin_reason.utils import (
    MAX_RAM_PERCENTAGE_DEFAULT,
    MAX_RAM_PERCENTAGE_PARAMETER,
    ONTOLOGY_GRAPH_IRI_PARAMETER,
    REASONER_PARAMETER,
    REASONERS,
    ROBOT,
    create_xml_catalog_file,
    get_graphs_tree,
    post_provenance,
    remove_temp,
    send_result,
)


@Plugin(
    label="Validate",
    description="Validates the consistency of an OWL ontology.",
    documentation="""A task validating the consistency of an OWL ontology and generating an
    explanation if inconsistencies are found. The explanation can be written to the project as a
    Markdown file and/or to a specified graph. The Markdown string is also provided as an output
    entity using the path "text". The following reasoners are supported: ELK, Expression
    Materializing Reasoner, HermiT, JFact, Structural Reasoner and Whelk.""",
    icon=Icon(package=__package__, file_name="validate.png"),
    parameters=[
        REASONER_PARAMETER,
        ONTOLOGY_GRAPH_IRI_PARAMETER,
        MAX_RAM_PERCENTAGE_PARAMETER,
        PluginParameter(
            param_type=BoolParameterType(),
            name="write_md",
            label="Write Markdown explanation file",
            description="Write Markdown file with explanation to project.",
            default_value=False,
        ),
        PluginParameter(
            param_type=BoolParameterType(),
            name="produce_graph",
            label="Produce output graph",
            description="Produce explanation graph.",
            default_value=False,
        ),
        PluginParameter(
            param_type=StringParameterType(),
            name="output_graph_iri",
            label="Output graph IRI",
            description="The IRI of the output graph for the inconsistency validation. ⚠️ Existing "
            "graphs will be overwritten.",
        ),
        PluginParameter(
            param_type=StringParameterType(),
            name="md_filename",
            label="Output filename",
            description="The filename of the Markdown file with the explanation of "
            "inconsistencies.⚠️ Existing files will be overwritten.",
        ),
        PluginParameter(
            param_type=BoolParameterType(),
            name="stop_at_inconsistencies",
            label="Stop at inconsistencies",
            description="Raise an error if inconsistencies are found. If enabled, the plugin does "
            "not output entities.",
            default_value=False,
        ),
    ],
)
class ValidatePlugin(WorkflowPlugin):
    """Validate plugin"""

    def __init__(  # noqa: PLR0913
        self,
        ontology_graph_iri: str = "",
        reasoner: str = "elk",
        produce_graph: bool = False,
        output_graph_iri: str = "",
        write_md: bool = False,
        md_filename: str = "",
        stop_at_inconsistencies: bool = False,
        max_ram_percentage: int = MAX_RAM_PERCENTAGE_DEFAULT,
    ) -> None:
        errors = ""
        if not validators.url(ontology_graph_iri):
            errors += 'Invalid IRI for parameter "Ontology graph IRI." '
        if produce_graph and not validators.url(output_graph_iri):
            errors += 'Invalid IRI for parameter "Output graph IRI". '
        if produce_graph and output_graph_iri == ontology_graph_iri:
            errors += "Output graph IRI cannot be the same as the Ontology graph IRI. "
        if reasoner not in REASONERS:
            errors += 'Invalid value for parameter "Reasoner". '
        if write_md and not is_valid_filename(md_filename):
            errors += 'Invalid filename for parameter "Output filename". '
        if max_ram_percentage not in range(1, 101):
            errors += 'Invalid value for parameter "Maximum RAM Percentage". '
        if errors:
            raise ValueError(errors[:-1])
        self.ontology_graph_iri = ontology_graph_iri
        self.reasoner = reasoner
        self.produce_graph = produce_graph
        self.output_graph_iri = output_graph_iri
        self.write_md = write_md
        self.stop_at_inconsistencies = stop_at_inconsistencies
        self.md_filename = md_filename if write_md else "mdfile.md"
        self.max_ram_percentage = max_ram_percentage
        self.temp = f"reason_{uuid4().hex}"

    def get_graphs(self, graphs: dict, context: ExecutionContext) -> None:
        """Get graphs from CMEM"""
        if not Path(self.temp).exists():
            Path(self.temp).mkdir(parents=True)
        for graph in graphs:
            with (Path(self.temp) / graphs[graph]).open("w", encoding="utf-8") as file:
                setup_cmempy_user_access(context.user)
                file.write(get(graph).text)

    def validate(self, graphs: dict) -> None:
        """Reason"""
        data_location = f"{self.temp}/{graphs[self.ontology_graph_iri]}"
        utctime = str(datetime.fromtimestamp(int(time()), tz=UTC))[:-6].replace(" ", "T") + "Z"

        cmd = (
            f"java -XX:MaxRAMPercentage={self.max_ram_percentage} -jar {ROBOT} "
            f'merge --input "{data_location}" '
            f"explain --reasoner {self.reasoner} -M inconsistency "
            f'--explanation "{self.temp}/{self.md_filename}"'
        )

        if self.produce_graph:
            cmd += (
                f' annotate --ontology-iri "{self.output_graph_iri}" '
                f'--language-annotation rdfs:label "Ontology Validation Result {utctime}" en '
                f"--language-annotation rdfs:comment "
                f'"Ontology validation of <{self.ontology_graph_iri}>" en '
                f'--link-annotation prov:wasDerivedFrom "{self.ontology_graph_iri}" '
                f'--typed-annotation dc:created "{utctime}" xsd:dateTime '
                f'--output "{self.temp}/output.ttl"'
            )

        response = run(shlex.split(cmd), check=False, capture_output=True)  # noqa: S603
        if response.returncode != 0:
            if response.stdout:
                raise OSError(response.stdout.decode())
            if response.stderr:
                raise OSError(response.stderr.decode())
            raise OSError("ROBOT error")

    def make_resource(self, context: ExecutionContext) -> None:
        """Make MD resource in project"""
        create_resource(
            project_name=context.task.project_id(),
            resource_name=self.md_filename,
            file_resource=(Path(self.temp) / self.md_filename).open("r"),
            replace=True,
        )

    def execute(self, inputs: tuple, context: ExecutionContext) -> Entities | None:  # noqa: ARG002
        """Run the workflow operator."""
        setup_cmempy_user_access(context.user)
        graphs = get_graphs_tree((self.ontology_graph_iri,))
        self.get_graphs(graphs, context)
        create_xml_catalog_file(self.temp, graphs)
        self.validate(graphs)

        if self.produce_graph:
            setup_cmempy_user_access(context.user)
            send_result(self.output_graph_iri, Path(self.temp) / "output.ttl")
            setup_cmempy_user_access(context.user)
            post_provenance(self, context)

        if self.write_md:
            setup_cmempy_user_access(context.user)
            self.make_resource(context)
        text = (Path(self.temp) / self.md_filename).read_text()

        remove_temp(self)

        if self.stop_at_inconsistencies and text != "No explanations found.":
            raise RuntimeError("Inconsistencies found in Ontology.")

        entities = [
            Entity(
                uri="https://eccenca.com/plugin_validateontology/md",
                values=[[text]],
            )
        ]
        schema = EntitySchema(
            type_uri="https://eccenca.com/plugin_validateontology/text",
            paths=[EntityPath(path="text")],
        )
        return Entities(entities=iter(entities), schema=schema)
