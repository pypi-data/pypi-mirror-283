try:
    from .fluss import Fluss
    from .rath import FlussLinkComposition, FlussRath
    from rath.links.split import SplitLink
    from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
    from rath.contrib.fakts.links.graphql_ws import FaktsGraphQLWSLink
    from rath.contrib.herre.links.auth import HerreAuthLink
    from graphql import OperationType
    from herre import Herre
    from fakts import Fakts

    from arkitekt_next.service_registry import (
        get_default_service_builder_registry,
        Params,
    )
    from arkitekt_next.model import Requirement

    class ArkitektNextFluss(Fluss):
        rath: FlussRath

    def build_arkitekt_next_fluss(fakts: Fakts, herre: Herre, params: Params):
        return ArkitektNextFluss(
            rath=FlussRath(
                link=FlussLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(fakts_group="fluss", fakts=fakts),
                        right=FaktsGraphQLWSLink(fakts_group="fluss", fakts=fakts),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            )
        )

    service_builder_registry = get_default_service_builder_registry()
    service_builder_registry.register(
        "fluss",
        build_arkitekt_next_fluss,
        Requirement(
            service="live.arkitekt.fluss",
            description="An instance of ArkitektNext fluss to retrieve graphs from",
        ),
    )
    imported = True

    try:
        from rekuest_next.structures.default import (
            get_default_structure_registry,
            PortScope,
            id_shrink,
        )
        from rekuest_next.widgets import SearchWidget

        from fluss_next.api.schema import (
            FlowFragment,
            SearchFlowsQuery,
            aget_flow,
            RunFragment,
            arun,
            SearchRunsQuery,
        )

        structure_reg = get_default_structure_registry()
        structure_reg.register_as_structure(
            FlowFragment,
            identifier="@fluss/flow",
            scope=PortScope.GLOBAL,
            aexpand=aget_flow,
            ashrink=id_shrink,
            default_widget=SearchWidget(query=SearchFlowsQuery.Meta.document, ward="fluss"),
        )
        structure_reg.register_as_structure(
            RunFragment,
            identifier="@fluss/run",
            scope=PortScope.GLOBAL,
            aexpand=arun,
            ashrink=id_shrink,
            default_widget=SearchWidget(query=SearchRunsQuery.Meta.document, ward="fluss"),
        )
    except ImportError as e:
        raise e

except ImportError as e:
    imported = False
    raise e
