from __future__ import annotations

from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import EmailStr, Field, conint, constr

from kelvin.api.client.data_model import DataModelBase
from kelvin.krn import KRN, KRNAsset, KRNAssetDataStream

from . import enum


class AppManagerAppPlannerRules(DataModelBase):
    """
    AppManagerAppPlannerRules object.

    Parameters
    ----------
    max_resources: Optional[int]
    cluster_sel_method: Optional[enum.ClusterSelMethod]
    cluster: Optional[str]
    reuse_workloads: Optional[bool]

    """

    max_resources: Optional[int] = Field(1, description="Maximum number of assets that a single workload can have.")
    cluster_sel_method: Optional[enum.ClusterSelMethod] = None
    cluster: Optional[str] = Field(None, description="Name of the cluster where the workload will be deployed.")
    reuse_workloads: Optional[bool] = Field(
        None, description="Whether to add Assets to existing workloads or create new ones."
    )


class Version(DataModelBase):
    """
    Version object.

    Parameters
    ----------
    created: Optional[datetime]
    id: Optional[str]
    updated: Optional[datetime]
    version: Optional[str]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when this version of the Application was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    id: Optional[str] = Field(
        None,
        description="Unique identifier for this version of the Application.",
        example="58ba052085dfd66545bf24a4957f6c8fd4af3c27",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when this version of the Application was last updated, formatted in RFC 3339.",
        example="2023-11-10T09:55:09.31857Z",
    )
    version: Optional[str] = Field(None, description="This version number of the Application.", example="1.0.8")


class AppManagerAppDetails(DataModelBase):
    """
    AppManagerAppDetails object.

    Parameters
    ----------
    created: Optional[datetime]
    description: Optional[str]
    latest_version: Optional[str]
    name: Optional[constr(max_length=64)]
    title: Optional[constr(max_length=64)]
    updated: Optional[datetime]
    versions: Optional[List[Version]]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Application was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    description: Optional[str] = Field(
        None,
        description="A full description of the purpose and characteristics of the Application.",
        example="""This model predicts the optimal settings for the compressor's operating parameters
. For example monitor its temperature and speed in order to maximize its efficiency and minimize energy consumption.""",
    )
    latest_version: Optional[str] = Field(
        None, description="The latest version number available for the Application.", example="1.0.8"
    )
    name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier `name` of the Application.", example="motor-speed-control"
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Application.", example="Motor Speed Control"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when the Application was last updated, formatted in RFC 3339.",
        example="2023-11-10T09:55:09.31857Z",
    )
    versions: Optional[List[Version]] = Field(
        None, description="Array of objects with information on each version of the Application."
    )


class AppManagerAppStatusResourceCount(DataModelBase):
    """
    AppManagerAppStatusResourceCount object.

    Parameters
    ----------
    running: Optional[int]
    total: Optional[int]

    """

    running: Optional[int] = Field(
        None,
        description="Total number of Applications of all versions together that have a status `running`.",
        example=8,
    )
    total: Optional[int] = Field(
        None, description="Total number of Applications of all versions together with any `status`.", example=10
    )


class AppManagerAppStatus(DataModelBase):
    """
    AppManagerAppStatus object.

    Parameters
    ----------
    last_seen: Optional[datetime]
    resource_count: Optional[AppManagerAppStatusResourceCount]
    status: Optional[enum.AppManagerAppStatus]

    """

    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when this version of the Application was last seen online, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    resource_count: Optional[AppManagerAppStatusResourceCount] = Field(
        None, description="Information on the total running and total Assets added to the Application."
    )
    status: Optional[enum.AppManagerAppStatus] = None


class AppManagerApp(DataModelBase):
    """
    AppManagerApp object.

    Parameters
    ----------
    app: Optional[AppManagerAppDetails]
    status: Optional[AppManagerAppStatus]
    updated: Optional[datetime]
    updated_by: Optional[KRN]

    """

    app: Optional[AppManagerAppDetails] = Field(
        None, description="All keys of the Application and a list of versions available."
    )
    status: Optional[AppManagerAppStatus] = Field(
        None,
        description="Group status of all Assets added to the Application, including a total count of assets currently running.",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Application keys were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    updated_by: Optional[KRN] = Field(
        None,
        description="User that made the last change to any Application keys. Sources are written in the krn format.",
        example="krn:user:person@example.com",
    )


class Parameter(DataModelBase):
    """
    Parameter object.

    Parameters
    ----------
    name: str
    value: Optional[Union[float, str, bool, Dict[str, Any]]]

    """

    name: str = Field(..., description="Parameter name.")
    value: Optional[Union[float, str, bool, Dict[str, Any]]] = Field(None, description="Parameter value.")


class AppManagerResourceParameters(DataModelBase):
    """
    AppManagerResourceParameters object.

    Parameters
    ----------
    resource: Optional[str]
    parameters: Optional[List[Parameter]]

    """

    resource: Optional[str] = Field(None, description="Resource (Asset) name.")
    parameters: Optional[List[Parameter]] = Field(None, description="Set of parameters for the Resource (Asset).")


class InstallManifestDataStreamMapItem(DataModelBase):
    """
    InstallManifestDataStreamMapItem object.

    Parameters
    ----------
    app: constr(max_length=64)
    datastream: constr(max_length=64)

    """

    app: constr(max_length=64) = Field(..., description="Name of the input/output used in the Application.")
    datastream: constr(max_length=64) = Field(
        ..., description="Name of the Data Stream linked to the input/output in the Application."
    )


class InstallManifestDeploymentDefaults(DataModelBase):
    """
    InstallManifestDeploymentDefaults object.

    Parameters
    ----------
    configuration: Optional[Dict[str, Any]]
    system: Optional[Dict[str, Any]]
    datastream_map: Optional[List[InstallManifestDataStreamMapItem]]

    """

    configuration: Optional[Dict[str, Any]] = Field(None, description="Application Configuration.")
    system: Optional[Dict[str, Any]] = Field(None, description="Kubernetes-related configurations.")
    datastream_map: Optional[List[InstallManifestDataStreamMapItem]] = Field(
        None, description="Mapping of Application inputs and outputs to Data Streams."
    )


class AppManagerAppVersion(DataModelBase):
    """
    AppManagerAppVersion object.

    Parameters
    ----------
    resources: Optional[List[KRNAsset]]

    """

    resources: Optional[List[KRNAsset]] = Field(
        None,
        description="A list of Assets running on the Application to perform the action requested. Partial names will be ignored. Each Asset name can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example=["krn:asset:bp_16", "krn:asset:bp_21"],
    )


class AppManagerAppVersionSummary(DataModelBase):
    """
    AppManagerAppVersionSummary object.

    Parameters
    ----------
    description: Optional[str]
    name: Optional[constr(max_length=64)]
    title: Optional[constr(max_length=64)]
    version: Optional[str]

    """

    description: Optional[str] = Field(
        None,
        description="A full description of the purpose and characteristics of the Application.",
        example="""This model predicts the optimal settings for the compressor's operating parameters
. For example monitor its temperature and speed in order to maximize its efficiency and minimize energy consumption.""",
    )
    name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` of the Application used by the Asset (`resource`).",
        example="motor-speed-control",
    )
    title: Optional[constr(max_length=64)] = Field(
        None,
        description="Display name (`title`) of the Application used by the Asset (`resource`).",
        example="Motor Speed Control",
    )
    version: Optional[str] = Field(
        None, description="The version number of the Application used by the Asset (`resource`).", example="1.0.8"
    )


class AppYaml(DataModelBase):
    """
    AppYaml object.

    Parameters
    ----------

    """


class AppVersion(DataModelBase):
    """
    AppVersion object.

    Parameters
    ----------
    created: Optional[datetime]
    id: Optional[str]
    payload: Optional[AppYaml]
    updated: Optional[datetime]
    version: Optional[str]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when this App version was first uploaded to the App Registry, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    id: Optional[str] = Field(
        None,
        description="Unique identifier for this version of the App in the App Registry.",
        example="58ba052085dfd66545bf24a4957f6c8fd4af3c27",
    )
    payload: Optional[AppYaml] = Field(
        None,
        description="Dictionary with keys for app inputs/outputs, info, spec version and system packages. Each key represents specific settings and parameters for the App.",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any App keys for this App version in the App Registry were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    version: Optional[str] = Field(None, description="Version number of this App in the App Registry.", example="1.2.0")


class App(DataModelBase):
    """
    App object.

    Parameters
    ----------
    created: Optional[datetime]
    description: Optional[constr(max_length=256)]
    latest_version: Optional[str]
    name: Optional[constr(max_length=64)]
    title: Optional[constr(max_length=64)]
    type: Optional[enum.AppType]
    updated: Optional[datetime]
    versions: Optional[List[AppVersion]]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the App was first uploaded to the App Registry, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    description: Optional[constr(max_length=256)] = Field(
        None,
        description="Description of the App in the App Registry.",
        example="""This application controls the speed of the beam pump motor in order to increase production for this type of artificial lift well. It uses values available from the control system such as Downhole Pressure, Motor Speed, Motor Torque and Choke position.
""",
    )
    latest_version: Optional[str] = Field(
        None, description="Latest version number of the App in the App Registry.", example="1.2.0"
    )
    name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier `name` of the App in the App Registry.", example="motor-speed-control"
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the App in the App Registry.", example="Motor Speed Control"
    )
    type: Optional[enum.AppType] = Field(
        None,
        description="Type of development used for the App. `kelvin` is Kelvin App using Python and `docker` is using the generic Dockerfile format.",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any App keys in the App Registry were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    versions: Optional[List[AppVersion]] = Field(
        None, description="Array of all App versions available in the App Registry."
    )


class AssetProperty(DataModelBase):
    """
    AssetProperty object.

    Parameters
    ----------
    name: Optional[constr(max_length=64)]
    title: Optional[constr(max_length=64)]
    value: Optional[Union[float, str, bool, Dict[str, Any]]]

    """

    name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` for the Asset Property. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="water-line-pressure",
    )
    title: Optional[constr(max_length=64)] = Field(
        None,
        description="Display name (title) for the Asset Property. You can use any character, numeric, space and special character in this key.",
        example="Water Line Pressure",
    )
    value: Optional[Union[float, str, bool, Dict[str, Any]]] = Field(
        None, description="Value for this Asset Property.", example=87
    )


class AssetStatusItem(DataModelBase):
    """
    AssetStatusItem object.

    Parameters
    ----------
    last_seen: Optional[datetime]
    state: Optional[enum.AssetState]

    """

    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when the Asset was last seen, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    state: Optional[enum.AssetState] = None


class Asset(DataModelBase):
    """
    Asset object.

    Parameters
    ----------
    asset_type_name: Optional[constr(max_length=64)]
    asset_type_title: Optional[constr(max_length=64)]
    created: Optional[datetime]
    name: Optional[constr(max_length=64)]
    properties: Optional[List[AssetProperty]]
    status: Optional[AssetStatusItem]
    title: Optional[constr(max_length=64)]
    updated: Optional[datetime]

    """

    asset_type_name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier `name` of the Asset Type linked to this Asset.", example="beam_pump"
    )
    asset_type_title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Asset Type linked to this Asset.", example="Beam Pump"
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Asset was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier `name` of the Asset.", example="well_01"
    )
    properties: Optional[List[AssetProperty]] = Field(
        None,
        description="Array of custom properties. These properties are not used by the Kelvin Platform and are for end-user use only.",
    )
    status: Optional[AssetStatusItem] = None
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Asset.", example="Well 01"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Asset keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class Property(DataModelBase):
    """
    Property object.

    Parameters
    ----------
    created: Optional[datetime]
    name: Optional[constr(max_length=64)]
    primitive_type: Optional[enum.PropertyType]
    title: Optional[constr(max_length=64)]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Asset Property Definition was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` for the Asset Property Definition. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="production_casing_depth",
    )
    primitive_type: Optional[enum.PropertyType] = Field(
        None, description="Property data type of the Asset Property Definition."
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Asset Property Definition.", example="Production Casing Depth"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Asset Property Definition keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class SimpleAsset(DataModelBase):
    """
    SimpleAsset object.

    Parameters
    ----------
    name: Optional[constr(max_length=64)]
    state: Optional[enum.AssetState]

    """

    name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` for the Asset. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="beam_pump",
    )
    state: Optional[enum.AssetState] = None


class AssetStatus(DataModelBase):
    """
    AssetStatus object.

    Parameters
    ----------
    data: Optional[List[SimpleAsset]]

    """

    data: Optional[List[SimpleAsset]] = Field(
        None,
        description="A dictionary with a data property that contains an array of all Assets and their corresponding current status (`state`).",
    )


class AssetType(DataModelBase):
    """
    AssetType object.

    Parameters
    ----------
    created: Optional[datetime]
    name: Optional[constr(max_length=64)]
    title: Optional[constr(max_length=64)]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Asset Type was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` for the Asset Type. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="beam_pump",
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Asset Type.", example="Beam Pump"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Asset Type keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class WorkloadStatus(DataModelBase):
    """
    WorkloadStatus object.

    Parameters
    ----------
    last_seen: Optional[datetime]
    message: Optional[str]
    state: Optional[enum.WorkloadStatus]
    warnings: Optional[List[str]]

    """

    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when the Workload was last seen by the Cloud, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    message: Optional[str] = Field(
        None, description="Descriptive, human-readable string for `state`.", example="Pending for deploy"
    )
    state: Optional[enum.WorkloadStatus] = Field(
        None, description="Current status of the Workload.", example="pending_deploy"
    )
    warnings: Optional[List[str]] = Field(
        None,
        description="All warnings received for any Workload operations.",
        example=[
            "back-off 5m0s restarting failed container=motor-speed-control-sjfhksdfhks67",
            "back-off 5m0s restarting failed container=gateway",
        ],
    )


class Bridge(DataModelBase):
    """
    Bridge object.

    Parameters
    ----------
    cluster_name: Optional[constr(max_length=64)]
    created: Optional[datetime]
    enabled: Optional[bool]
    name: Optional[constr(max_length=32)]
    node_name: Optional[constr(max_length=64)]
    payload: Optional[AppYaml]
    status: Optional[WorkloadStatus]
    title: Optional[str]
    updated: Optional[datetime]
    workload_name: Optional[constr(max_length=32)]
    app_name: Optional[constr(max_length=64)]
    app_version: Optional[str]

    """

    cluster_name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier `name` of the Cluster.", example="docs-demo-cluster-k3s"
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Bridge (Connection) was first created, formatted in RFC 3339.",
        example="2023-12-26T18:22:18.582724Z",
    )
    enabled: Optional[bool] = Field(
        None,
        description="If true, Bridge (Connection) `status` is set to `running` and will process I/O's. If false, Bridge (Connection) `status` is set to `stopped` but remains in Node on the Edge System.",
        example=True,
    )
    name: Optional[constr(max_length=32)] = Field(
        None, description="Unique identifier `name` of the Bridge (Connection).", example="motor-plc-opcua-connection"
    )
    node_name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` of the Node in the Cluster hosting the Bridge (Connection).",
        example="docs-demo-node-01",
    )
    payload: Optional[AppYaml] = Field(
        None,
        description="Dictionary with keys for configuration, language, logging level, metrics mapping, protocol, and system packages. Each key represents specific settings and parameters for the Bridge (Connection).",
    )
    status: Optional[WorkloadStatus] = None
    title: Optional[str] = Field(
        None, description="Display name (`title`) of the Bridge (Connection).", example="Motor PLC OPCUA Connection"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Bridge (Connection) keys were last updated, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    workload_name: Optional[constr(max_length=32)] = Field(
        None,
        description="Unique identifier `name` of the Workload that the Bridge (Connection) App is deployed as to the Cluster.",
        example="motor-plc-opcua-connection",
    )
    app_name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` of the App. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="test-app",
    )
    app_version: Optional[str] = Field(None, description="App version", example="1.2.0")


class ControlChangeFrom(DataModelBase):
    """
    ControlChangeFrom object.

    Parameters
    ----------
    value: Union[float, str, bool, Dict[str, Any]]
    timestamp: datetime

    """

    value: Union[float, str, bool, Dict[str, Any]]
    timestamp: datetime


class ControlChangeReport(DataModelBase):
    """
    ControlChangeReport object.

    Parameters
    ----------
    value: Union[float, str, bool, Dict[str, Any]]
    timestamp: datetime
    source: enum.ControlChangeSource

    """

    value: Union[float, str, bool, Dict[str, Any]]
    timestamp: datetime
    source: enum.ControlChangeSource


class ControlChangeReported(DataModelBase):
    """
    ControlChangeReported object.

    Parameters
    ----------
    before: Optional[ControlChangeReport]
    after: Optional[ControlChangeReport]

    """

    before: Optional[ControlChangeReport] = None
    after: Optional[ControlChangeReport] = None


class DataStreamDataType(DataModelBase):
    """
    DataStreamDataType object.

    Parameters
    ----------
    created: Optional[datetime]
    name: Optional[constr(max_length=64)]
    title: Optional[constr(max_length=64)]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Data Type was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier `name` of the Data Type.", example="number"
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Data Type.", example="Number"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Data Type keys were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )


class DataStreamSemanticType(DataModelBase):
    """
    DataStreamSemanticType object.

    Parameters
    ----------
    created: Optional[datetime]
    name: Optional[str]
    title: Optional[constr(max_length=64)]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Semantic Type was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    name: Optional[str] = Field(
        None, description="Unique identifier `name` of the Semantic Type.", example="mass_flow_rate"
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Semantic Type.", example="Mass Flow Rate"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Semantic Type keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class Unit(DataModelBase):
    """
    Unit object.

    Parameters
    ----------
    created: Optional[datetime]
    name: Optional[constr(max_length=64)]
    symbol: Optional[constr(max_length=16)]
    title: Optional[constr(max_length=64)]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Unit was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier `name` of the Unit.", example="degree_fahrenheit"
    )
    symbol: Optional[constr(max_length=16)] = Field(
        None,
        description="A brief and precise character or set of characters that symbolize a specific measurement of the Unit.",
        example="°F",
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Unit.", example="Degree Fahrenheit"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Unit keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class DataTag(DataModelBase):
    """
    DataTag object.

    Parameters
    ----------
    id: Optional[UUID]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    tag_name: Optional[constr(max_length=64)]
    resource: Optional[KRNAsset]
    source: Optional[KRN]
    description: Optional[constr(max_length=256)]
    contexts: Optional[List[KRN]]
    created: Optional[datetime]
    updated: Optional[datetime]

    """

    id: Optional[UUID] = Field(
        None,
        description="A unique random generated UUID as the key `id` for the Data Tag.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    start_date: Optional[datetime] = Field(
        None,
        description="Start date for the Data Tag. Time is based on UTC timezone, formatted in RFC 3339.",
        example="2024-02-06T18:22:18.582724Z",
    )
    end_date: Optional[datetime] = Field(
        None,
        description="End date for the Data Tag. Time is based on UTC timezone, formatted in RFC 3339.",
        example="2024-02-06T19:22:18.582724Z",
    )
    tag_name: Optional[constr(max_length=64)] = Field(
        None, description="Tag name to categorize the Data Tag", example="Valve Change"
    )
    resource: Optional[KRNAsset] = Field(
        None, description="The Asset that this Data Tag is related to.", example="krn:asset:well_01"
    )
    source: Optional[KRN] = Field(
        None,
        description="The process that created this Data Tag. This can be a user or an automated process like a workload, application, etc.",
        example="krn:wlappv:cluster1/app1/1.2.0",
    )
    description: Optional[constr(max_length=256)] = Field(
        None, description="Detailed description of the Data Tag.", example="A Valve was changed today."
    )
    contexts: Optional[List[KRN]] = Field(
        None,
        description="A list of associated resources with this Data Tag. This can be a datastream, application or any other valid resource in the Kelvin Platform.",
        example=["krn:datastream:temperature", "krn:appversion:smart-pcp/2.0.0"],
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Data Tag was created, formatted in RFC 3339.",
        example="2024-02-06T19:22:18.582724Z",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Data Tag keys were last updated, formatted in RFC 3339.",
        example="2024-02-06T19:22:18.582724Z",
    )


class Tag(DataModelBase):
    """
    Tag object.

    Parameters
    ----------
    name: Optional[constr(max_length=64)]
    metadata: Optional[Dict[str, Any]]
    created: Optional[datetime]
    updated: Optional[datetime]

    """

    name: Optional[constr(max_length=64)] = Field(None, description="Tag name", example="Valve Change")
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Detailed Attributes of the Tag. The structure of the `metadata` object can have any key/value structure and will depend on the required properties of the Tag.",
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Data Tag was created, formatted in RFC 3339.",
        example="2024-02-06T19:22:18.582724Z",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Data Tag keys were last updated, formatted in RFC 3339.",
        example="2024-02-06T19:22:18.582724Z",
    )


class FileStorage(DataModelBase):
    """
    FileStorage object.

    Parameters
    ----------
    file_id: Optional[str]
    file_name: Optional[constr(max_length=128)]
    file_size: Optional[int]
    checksum: Optional[str]
    source: Optional[str]
    created: Optional[datetime]
    metadata: Optional[Dict[str, Any]]

    """

    file_id: Optional[str] = Field(
        None, description="Generated UUID for a file", example="50FDD765-DBD7-4C7C-844D-E6211C9CD9E7"
    )
    file_name: Optional[constr(max_length=128)] = Field(None, description="Actual file name", example="test.csv")
    file_size: Optional[int] = Field(None, description="File size in bytes", example=300)
    checksum: Optional[str] = Field(
        None,
        description="File SHA256 checksum",
        example="e07de9b7a1788fe439bd1d9a114d1a3ee4eb5b29f8a9e11057f7c31d718c5614",
    )
    source: Optional[str] = Field(None, description="Resource that uploaded the file", example="krn:user:user1")
    created: Optional[datetime] = Field(
        None,
        description="UTC time representing when the file was uploaded, formatted in RFC 3339.",
        example="2024-02-20T22:22:18.582724Z",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="A free-form JSON object representing the files metadata",
        example={"property1": True, "property2": 2},
    )


class InstanceSettingsAppManagerPlannerRules(DataModelBase):
    """
    InstanceSettingsAppManagerPlannerRules object.

    Parameters
    ----------
    name: Optional[str]
    created: Optional[datetime]
    updated: Optional[datetime]
    payload: AppManagerAppPlannerRules

    """

    name: Optional[str] = Field(
        None,
        description="The name of the instance setting. This value is always the same as this endpoint only accesses this setting.",
    )
    created: Optional[datetime] = Field(None, description="Date and time at which the planner rule was created.")
    updated: Optional[datetime] = Field(None, description="Date and time at which the planner rule was last updated.")
    payload: AppManagerAppPlannerRules


class InstanceSettings(DataModelBase):
    """
    InstanceSettings object.

    Parameters
    ----------
    created: Optional[datetime]
    name: Optional[constr(max_length=64)]
    payload: Optional[Dict[str, Any]]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Instance Setting was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` of the Instance Setting.",
        example="core.ui.datastreams.asset-type.groups",
    )
    payload: Optional[Dict[str, Any]] = Field(
        None,
        description="The Instance Settings. The structure of this `payload` object depends on the type of Instance Setting being defined.",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Instance Settings keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class State(Enum):
    idle = "idle"
    downloading = "downloading"
    ready = "ready"


class UpgradeStatus(DataModelBase):
    """
    UpgradeStatus object.

    Parameters
    ----------
    message: Optional[str]
    state: Optional[State]

    """

    message: Optional[str] = Field(
        None, description="Any feedback messages about the current upgrade process.", example=""
    )
    state: Optional[State] = Field(None, description="Current state of the upgrade process.", example="downloading")


class VersionModel(DataModelBase):
    """
    VersionModel object.

    Parameters
    ----------
    k8s_version: Optional[str]
    kelvin_version: Optional[str]

    """

    k8s_version: Optional[str] = Field(
        None, description="Current version of k8s installed on the Cluster.", example="v1.24.10+k3s1"
    )
    kelvin_version: Optional[str] = Field(
        None, description="Current version of Kelvin Software installed on the Cluster.", example="4.0.0-rc2024.519"
    )


class OrchestrationCluster(DataModelBase):
    """
    OrchestrationCluster object.

    Parameters
    ----------
    created: Optional[datetime]
    forward_logs_buffer_size: Optional[conint(ge=1, le=20)]
    forward_logs_enabled: Optional[bool]
    join_script: Optional[str]
    last_seen: Optional[datetime]
    manifests_scrape_enabled: Optional[bool]
    manifests_scrape_interval: Optional[conint(ge=30, le=86400)]
    name: Optional[constr(max_length=64)]
    provision_script: Optional[str]
    ready: Optional[bool]
    service_account_token: Optional[str]
    status: Optional[enum.OrchestrationClusterStatus]
    sync_scrape_interval: Optional[conint(ge=10, le=86400)]
    telemetry_buffer_size: Optional[conint(ge=1, le=20)]
    telemetry_enabled: Optional[bool]
    telemetry_scrape_interval: Optional[conint(ge=1, le=3600)]
    title: Optional[constr(max_length=64)]
    type: Optional[enum.ClusterType]
    updated: Optional[datetime]
    upgrade_instantly_apply: Optional[bool]
    upgrade_pre_download: Optional[bool]
    upgrade_status: Optional[UpgradeStatus]
    version: Optional[VersionModel]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Cluster was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    forward_logs_buffer_size: Optional[conint(ge=1, le=20)] = Field(
        5,
        description="Size in gigabytes of the log storage in the Cluster when Cluster is offline. Any setting changes will delete all logs not yet transferred from the Cluster to Cloud.",
        example=10,
    )
    forward_logs_enabled: Optional[bool] = Field(
        True,
        description="Enable offline storage in the Cluster for log retention; transfers logs when Cluster is next online.",
        example=True,
    )
    join_script: Optional[str] = None
    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when the Cluster was last seen by the Cloud, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    manifests_scrape_enabled: Optional[bool] = Field(
        True, description="Enable auto update Kelvin Software running on the Cluster.", example=True
    )
    manifests_scrape_interval: Optional[conint(ge=30, le=86400)] = Field(
        86400,
        description="Frequency in seconds for checking updates in the Cloud for Kelvin Software running on the Cluster.",
        example=3600,
    )
    name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier key `name` of the Cluster.", example="aws-cluster"
    )
    provision_script: Optional[str] = Field(
        None,
        description="Provision script required to install the Kelvin Software at the edge.",
        example="bash <(curl -sfS https://{URL}/provision) --service-account bm9kZS1jbGllbnQt...",
    )
    ready: Optional[bool] = Field(
        None, description="Setting to inform Kelvin UI if the Cluster is ready.", example=True
    )
    service_account_token: Optional[str] = Field(
        None,
        description="Service account token for automated processes to authenticate with when performing actions in the Cluster.",
    )
    status: Optional[enum.OrchestrationClusterStatus] = None
    sync_scrape_interval: Optional[conint(ge=10, le=86400)] = Field(
        30,
        description="Frequency in seconds that the Cluster checks for new changes to apply to Workloads or Applications (deploy, start, stop, etc.)",
        example=3600,
    )
    telemetry_buffer_size: Optional[conint(ge=1, le=20)] = Field(
        5,
        description="Size in gigabytes of telemetry data storage in the Cluster when the Cluster is offline. Any setting changes will delete all logs not yet transferred from the Cluster to Cloud.",
        example=10,
    )
    telemetry_enabled: Optional[bool] = Field(
        True,
        description="Enable offline storage in the Cluster for telemetry data retention; transfers data when the Cluster is next online.",
    )
    telemetry_scrape_interval: Optional[conint(ge=1, le=3600)] = Field(
        30,
        description="Time interval in seconds to save each telemetry data. Any setting changes will delete all data not yet transferred from the Cluster to Cloud.",
        example=60,
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Cluster.", example="AWS Cluster"
    )
    type: Optional[enum.ClusterType] = Field(None, description="Type of Cluster deployed.")
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Cluster keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    upgrade_instantly_apply: Optional[bool] = Field(
        None,
        description="Option if upgrades should be applied automatically and instantly as soon as they are available in the Cluster.",
        example=True,
    )
    upgrade_pre_download: Optional[bool] = Field(
        None,
        description="Option for pre-downloading new Workloads or Application upgrades to the Cluster. Actual upgrade initiation requires manual action or having `instantly_apply` set to true.",
        example=True,
    )
    upgrade_status: Optional[UpgradeStatus] = Field(
        None, description="Current status and messages for any ongoing updates to the Cluster."
    )
    version: Optional[VersionModel] = Field(
        None, description="Current versions of the different core component software installed on the Cluster."
    )


class ParameterItemNoComment(DataModelBase):
    """
    ParameterItemNoComment object.

    Parameters
    ----------
    name: str
    value: Union[float, str, bool]

    """

    name: str = Field(..., description="Parameter name")
    value: Union[float, str, bool]


class ParameterItem(ParameterItemNoComment):
    """
    ParameterItem object.

    Parameters
    ----------
    comment: Optional[str]

    """

    comment: Optional[str] = Field(None, description="Comment regarding the parameter change action")


class ResourceParameters(DataModelBase):
    """
    ResourceParameters object.

    Parameters
    ----------
    resource: KRNAsset
    parameters: List[ParameterItem]

    """

    resource: KRNAsset = Field(..., description="The target resource to which the parameters are to be applied")
    parameters: List[ParameterItem]


class ParameterScheduleResourceParameter(DataModelBase):
    """
    ParameterScheduleResourceParameter object.

    Parameters
    ----------
    resource: str
    parameters: Dict[str, Union[float, str, bool]]

    """

    resource: str = Field(..., description="The resource (asset) name in KRN format")
    parameters: Dict[str, Union[float, str, bool]]


class Revert(DataModelBase):
    """
    Revert object.

    Parameters
    ----------
    scheduled_for: datetime
    resource_parameters: List[ParameterScheduleResourceParameter]

    """

    scheduled_for: datetime = Field(..., description="Date and time at which the parameters are to be reverted")
    resource_parameters: List[ParameterScheduleResourceParameter]


class ParameterScheduleBase(DataModelBase):
    """
    ParameterScheduleBase object.

    Parameters
    ----------
    app_name: str
    app_version: str
    scheduled_for: datetime
    resources: List[KRN]
    parameters: Dict[str, Union[float, str, bool]]
    comment: Optional[str]
    revert: Optional[Revert]

    """

    app_name: str = Field(..., description="The name of the application")
    app_version: str = Field(..., description="The version of the application")
    scheduled_for: datetime = Field(..., description="Date and time at which the parameters are to be applied")
    resources: List[KRN] = Field(..., min_items=1)
    parameters: Dict[str, Union[float, str, bool]]
    comment: Optional[str] = Field(None, description="Comment regarding the parameter change action")
    revert: Optional[Revert] = Field(None, description="Configuration to revert the parameters to the desired values")


class ParameterSchedule(ParameterScheduleBase):
    """
    ParameterSchedule object.

    Parameters
    ----------
    id: UUID
    state: enum.ParameterScheduleState
    original_resource_parameters: Optional[List[ParameterScheduleResourceParameter]]
    error_msg: Optional[str]
    created_at: datetime
    created_by: KRN
    applied_at: Optional[datetime]
    applied_by: Optional[KRN]
    reverted_at: Optional[datetime]
    reverted_by: Optional[KRN]

    """

    id: UUID = Field(..., description="Unique ID of the schedule")
    state: enum.ParameterScheduleState
    original_resource_parameters: Optional[List[ParameterScheduleResourceParameter]] = None
    error_msg: Optional[str] = Field(None, description="Error message if the schedule failed")
    created_at: datetime = Field(..., description="Date and time of the schedule creation")
    created_by: KRN = Field(..., description="Who/what created the schedule")
    applied_at: Optional[datetime] = Field(None, description="Date and time of the schedule creation")
    applied_by: Optional[KRN] = Field(None, description="Who/what applied the schedule")
    reverted_at: Optional[datetime] = Field(None, description="Date and time of the schedule creation")
    reverted_by: Optional[KRN] = Field(None, description="Who/what reverted the schedule")


class RecommendationControlChange(DataModelBase):
    """
    RecommendationControlChange object.

    Parameters
    ----------
    control_change_id: Optional[UUID]
    expiration_date: Optional[datetime]
    payload: Union[float, str, bool, Dict[str, Any]]
    resource: KRNAssetDataStream
    retries: Optional[int]
    timeout: Optional[int]
    trace_id: Optional[UUID]
    from_: Optional[ControlChangeFrom]

    """

    control_change_id: Optional[UUID] = Field(
        None,
        description="Unique identifier id for the Control Change request. This will only be returned when the Recommendation state is `applied` where the actions have been created and an id registered on the Server.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    expiration_date: Optional[datetime] = Field(
        None,
        description="UTC time when any the Control Change initiated will expire and the `status` automatically marked as `failed`, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    payload: Union[float, str, bool, Dict[str, Any]]
    resource: KRNAssetDataStream = Field(
        ...,
        description="The asset / data stream pair that this Control Change will be applied to.",
        example="krn:ad:bp_16/motor_speed_setpoint",
    )
    retries: Optional[int] = Field(
        0,
        description="Number of retry attempts to write the Control Change to the Bridge until a `processed` acknowledgment is received from the Bridge. If number of attempts exceeds `retries` then the Control Change Manager updates the Control Change key `state` with the value `failed`.",
        example=3,
    )
    timeout: Optional[int] = Field(
        300,
        description="Time in seconds the Control Change Manager will wait after sending the Control Change for the Bridge to send a `processed` acknowledgement reply before retry sending the Control Change.",
        example=600,
    )
    trace_id: Optional[UUID] = Field(
        None,
        description="Unique identifier id for the Control Change request.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    from_: Optional[ControlChangeFrom] = Field(None, alias="from")


class RecommendationActions(DataModelBase):
    """
    RecommendationActions object.

    Parameters
    ----------
    control_changes: Optional[List[RecommendationControlChange]]

    """

    control_changes: Optional[List[RecommendationControlChange]] = Field(
        None,
        description="An array of objects with Control Change information. If the Recommendation is `pending`, it will display creation information or if the Recommendation is `accepted` or `applied` it will show the Control Change status. Each Control Change does not need to be related to the `resource` of the Recommendation.",
    )


class RecommendationActionStatus(DataModelBase):
    """
    RecommendationActionStatus object.

    Parameters
    ----------
    message: Optional[str]
    success: Optional[bool]

    """

    message: Optional[str] = Field(
        None,
        description="If `success` is `true`, this contains a message of the action that has been performed. If `success` is `false`, this contains information why it failed.",
        example="Recommendation actions implemented",
    )
    success: Optional[bool] = Field(
        None,
        description="Response to signify if the actions have been initiated. `true` means the actions have been initiated and `false` means the actions failed to be initialized. This does not mean the actions have been completed successfully and you still need to followup monitoring each initiated action separately.",
        example=True,
    )


class RecommendationLog(DataModelBase):
    """
    RecommendationLog object.

    Parameters
    ----------
    created_at: Optional[datetime]
    email_list: Optional[List[EmailStr]]
    message: Optional[str]
    source: Optional[KRN]
    state: Optional[enum.RecommendationState]

    """

    created_at: Optional[datetime] = Field(
        None,
        description="UTC time when the log entry for the Recommendation was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    email_list: Optional[List[EmailStr]] = Field(
        None, description="Future feature.", example=["richard.teo@kelvininc.com", "user@example.com"]
    )
    message: Optional[str] = Field(
        None,
        description="A custom message related to the Recommendation or any actions that are taken.",
        example=" Recommendation accepted by Operator.",
    )
    source: Optional[KRN] = Field(
        None,
        description="The process that created this Recommendation. This can be a user or an automated process like a workload, application, etc.",
        example="krn:wlappv:aws-cluster/humidity-optimizer/1.1.0",
    )
    state: Optional[enum.RecommendationState] = Field(
        None, description="State of the Recommendation when the log was created."
    )


class Recommendation(DataModelBase):
    """
    Recommendation object.

    Parameters
    ----------
    actions: Optional[RecommendationActions]
    confidence: Optional[conint(ge=-2147483648, le=2147483647)]
    created: Optional[datetime]
    custom_identifier: Optional[str]
    description: Optional[str]
    expiration_date: Optional[datetime]
    id: Optional[UUID]
    logs: Optional[List[RecommendationLog]]
    metadata: Optional[Dict[str, Any]]
    resource: Optional[KRNAsset]
    resource_parameters: Optional[Dict[str, Any]]
    source: Optional[KRN]
    state: Optional[enum.RecommendationState]
    type: Optional[constr(max_length=64)]
    type_title: Optional[constr(max_length=64)]
    updated: Optional[datetime]

    """

    actions: Optional[RecommendationActions] = None
    confidence: Optional[conint(ge=-2147483648, le=2147483647)] = Field(
        None,
        description="Confidence level of the Recommendation. This is usually, but not mandatory, related to any machine learning model confidence results.",
        example=7,
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Recommendation was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    custom_identifier: Optional[str] = Field(
        None, description="An optional custom identifier for any purpose.", example="model-aws-ltsm-anomaly"
    )
    description: Optional[str] = Field(
        None,
        description="Detailed description of the Recommendation.",
        example="Beam pump speed AI optimizer application recommends a new value for the speed setpoint of the controller.",
    )
    expiration_date: Optional[datetime] = Field(
        None,
        description="UTC time when any the Recommendation will expire and the `status` automatically marked as `expired`, formatted in RFC 3339. The operator will not be able to take any further actions on this Recommendation. If no date is given, then the Recommendation will never expire.",
        example="2023-11-18T18:22:18.582724Z",
    )
    id: Optional[UUID] = Field(
        None,
        description="A unique random generated UUID as the key `id` for the Recommendation.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    logs: Optional[List[RecommendationLog]] = Field(
        None, description="A date ordered list of the updates performed on this Recommendation."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Custom dictionary keys/values for use by clients for anything useful and related to the Recommendation.",
    )
    resource: Optional[KRNAsset] = Field(
        None, description="The asset that this Recommendation is related to.", example="krn:asset:bp_16"
    )
    resource_parameters: Optional[Dict[str, Any]] = Field(None, description="resource_parameters")
    source: Optional[KRN] = Field(
        None,
        description="The process that created or last updated this Recommendation. This can be a user or an automated process like a workload, application, etc.",
        example="krn:wlappv:cluster1/app1/1.2.0",
    )
    state: Optional[enum.RecommendationState] = Field(None, description="Current `state` of the Recommendation.")
    type: Optional[constr(max_length=64)] = Field(
        None, description="The Recommendation Type `name` associated with the Recommendation.", example="decrease_speed"
    )
    type_title: Optional[constr(max_length=64)] = Field(
        None,
        description="The Recommendation Type `title` of its `name` associated with the Recommendation.",
        example="Decrease Speed",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Recommendation keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class RecommendationType(DataModelBase):
    """
    RecommendationType object.

    Parameters
    ----------
    created_at: Optional[datetime]
    description: Optional[str]
    name: Optional[constr(max_length=64)]
    title: Optional[constr(max_length=64)]
    updated_at: Optional[datetime]

    """

    created_at: Optional[datetime] = Field(
        None,
        description="UTC time when the Recommendation Type was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    description: Optional[str] = Field(
        None,
        description="Full description of the purpose for this Recommendation Type.",
        example="Recommendations that require a reduction in the speed set point.",
    )
    name: Optional[constr(max_length=64)] = Field(
        None,
        description="Unique identifier `name` for the Recommendation Type. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="decrease_speed",
    )
    title: Optional[constr(max_length=64)] = Field(
        None, description="Display name (`title`) of the Recommendation Type.", example="Decrease Speed"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="UTC time when any Recommendation Type keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class ThreadAttachment(DataModelBase):
    """
    ThreadAttachment object.

    Parameters
    ----------
    extension: Optional[str]
    filename: Optional[str]
    size: Optional[int]
    url: Optional[str]

    """

    extension: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None


class ThreadUserFollow(DataModelBase):
    """
    ThreadUserFollow object.

    Parameters
    ----------
    mute: Optional[bool]
    seen: Optional[bool]

    """

    mute: Optional[bool] = None
    seen: Optional[bool] = None


class KelvinMessage(DataModelBase):
    """
    KelvinMessage object.

    Parameters
    ----------
    id: UUID
    type: str
    resource: KRN
    source: KRN
    timestamp: datetime
    payload: Union[float, str, bool, Dict[str, Any]]

    """

    id: UUID = Field(
        ...,
        description="UUID string. It identifies the message itself, so it must be generated every time a new message is created, it can’t be copied to a new message.",
    )
    type: str = Field(..., description="Kelvin Message Type representing the message type.")
    resource: KRN = Field(
        ..., description="Kelvin Resource Name indicating the resource this message represents (asset, metric,...)."
    )
    source: KRN = Field(
        ...,
        description="Kelvin Resource Name representing the application that created the message, such as a KSDK app, a worker, the UI, etc.",
    )
    timestamp: datetime = Field(
        ...,
        description="UTC timestamp in RFC-3339 format. This is the time stamp of the data. In most cases, that means the current time stamp.",
    )
    payload: Union[float, str, bool, Dict[str, Any]] = Field(..., description="The value of the measurement.")


class TimeseriesData(DataModelBase):
    """
    TimeseriesData object.

    Parameters
    ----------
    created: Optional[datetime]
    data_type: Optional[str]
    fields: Optional[List[str]]
    last_timestamp: Optional[datetime]
    last_value: Optional[Union[float, str, bool, Dict[str, Any]]]
    resource: Optional[KRNAssetDataStream]
    source: Optional[KRN]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the `last_value` values were first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    data_type: Optional[str] = Field(None, description="Primitive data type of the `last_value` values.")
    fields: Optional[List[str]] = Field(
        None, description="Data `field` element name of each value in `last_value`.", example=["value"]
    )
    last_timestamp: Optional[datetime] = Field(
        None,
        description="UTC time when the time series data was last accessed, formatted in RFC 3339.",
        example="2023-11-10T09:55:08.627924Z",
    )
    last_value: Optional[Union[float, str, bool, Dict[str, Any]]] = Field(
        None, description="Most recent value received for each `field`."
    )
    resource: Optional[KRNAssetDataStream] = Field(
        None, description="Asset / Data Stream associated with `last_value`.", example="krn:ad:asset/data_stream"
    )
    source: Optional[KRN] = Field(
        None,
        description="Specifies the user or workload source for `last_value`.",
        example="krn:wlappv:cluster1/app1/1.2.0",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when the time series data was last updated, formatted in RFC 3339.",
        example="2023-11-10T09:55:09.31857Z",
    )


class UserSetting(DataModelBase):
    """
    UserSetting object.

    Parameters
    ----------
    created: Optional[datetime]
    payload: Optional[Dict[str, Any]]
    setting_name: Optional[constr(max_length=64)]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the User Setting was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    payload: Optional[Dict[str, Any]] = Field(
        None,
        description="The User Settings. The structure of this `payload` object depends on the type of User Setting being defined.",
    )
    setting_name: Optional[constr(max_length=64)] = Field(
        None, description="Unique identifier User Setting key `setting_name`.", example="kelvin-notifications"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any User Setting keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class NetworkingAddressItem(DataModelBase):
    """
    NetworkingAddressItem object.

    Parameters
    ----------
    address: Optional[IPv4Address]
    interface: Optional[str]
    port: Optional[conint(ge=1, le=65535)]

    """

    address: Optional[IPv4Address] = Field(None, description="IPV4 address to reach the Service.", example="172.0.0.2")
    interface: Optional[str] = Field(None, description="Interface responsible for hosting the Service.", example="eth0")
    port: Optional[conint(ge=1, le=65535)] = Field(
        None, description="Port designated for accessing the Service.", example=8080
    )


class Protocol(Enum):
    tcp = "tcp"
    udp = "udp"


class NetworkingItem(DataModelBase):
    """
    NetworkingItem object.

    Parameters
    ----------
    addresses: Optional[List[NetworkingAddressItem]]
    name: Optional[str]
    protocol: Optional[Protocol]

    """

    addresses: Optional[List[NetworkingAddressItem]] = Field(None, description="Array of ports exposed by the Service.")
    name: Optional[str] = Field(None, description="Unique identifier `name` of the Service.", example="http-service")
    protocol: Optional[Protocol] = Field(None, description="Protocol used by the Service.", example="tcp")


class StagedStatus(DataModelBase):
    """
    StagedStatus object.

    Parameters
    ----------
    message: Optional[str]
    state: Optional[enum.WorkloadStatus]
    warnings: Optional[List[str]]

    """

    message: Optional[str] = Field(
        None, description="Descriptive, human-readable string for `state`.", example="Pending for deploy"
    )
    state: Optional[enum.WorkloadStatus] = Field(
        None, description="Current status of the Staged Workload.", example="pending_deploy"
    )
    warnings: Optional[List[str]] = Field(
        None,
        description="All warnings received for any Staged Workload operations.",
        example=[
            "back-off 5m0s restarting failed container=motor-speed-control-sjfhksdfhks67",
            "back-off 5m0s restarting failed container=gateway",
        ],
    )


class WorkloadStaged(DataModelBase):
    """
    WorkloadStaged object.

    Parameters
    ----------
    ready: Optional[bool]
    app_version: Optional[str]
    payload: Optional[Dict[str, Any]]
    instantly_apply: Optional[bool]
    status: Optional[StagedStatus]

    """

    ready: Optional[bool] = Field(None, description="Staged workload ready to be applied.", example=True)
    app_version: Optional[str] = Field(
        None, description="Version Number of the Kelvin App used for the Staged Workload.", example="1.2.0"
    )
    payload: Optional[Dict[str, Any]] = Field(
        None, description="Internal Kelvin configuration information for deployment of the Staged Workload."
    )
    instantly_apply: Optional[bool] = Field(
        None, description="Whether the staged workload should be instantly applied or not.", example=True
    )
    status: Optional[StagedStatus] = None


class Workload(DataModelBase):
    """
    Workload object.

    Parameters
    ----------
    acp_name: Optional[constr(min_length=1, max_length=64)]
    app_name: Optional[constr(min_length=1, max_length=64)]
    app_version: Optional[str]
    cluster_name: Optional[constr(min_length=1, max_length=64)]
    created: Optional[datetime]
    download_status: Optional[enum.WorkloadDownloadStatus]
    enabled: Optional[bool]
    name: Optional[constr(min_length=1, max_length=32)]
    networking: Optional[List[NetworkingItem]]
    node_name: Optional[constr(min_length=1, max_length=64)]
    payload: Optional[Dict[str, Any]]
    pre_download: Optional[bool]
    status: Optional[WorkloadStatus]
    title: Optional[constr(min_length=1)]
    updated: Optional[datetime]
    staged: Optional[WorkloadStaged]

    """

    acp_name: Optional[constr(min_length=1, max_length=64)] = Field(
        None, description="[`Deprecated`] Unique identifier `name` of the Cluster.", example="docs-demo-cluster-k3s"
    )
    app_name: Optional[constr(min_length=1, max_length=64)] = Field(
        None,
        description="Unique identifier `name` of the Kelvin App in the App Registry.",
        example="motor-speed-control",
    )
    app_version: Optional[str] = Field(
        None, description="Version Number of the Kelvin App used for this Workload.", example="1.2.0"
    )
    cluster_name: Optional[constr(min_length=1, max_length=64)] = Field(
        None, description="Unique identifier `name` of the Cluster.", example="docs-demo-cluster-k3s"
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Workload was first created, formatted in RFC 3339.",
        example="2023-12-26T18:22:18.582724Z",
    )
    download_status: Optional[enum.WorkloadDownloadStatus] = None
    enabled: Optional[bool] = Field(
        None,
        description="If true, Workload `status` is set to `running` and will process I/O's. If false, Workload `status` is set to `stopped` but remains in Node on the Edge System.",
        example=True,
    )
    name: Optional[constr(min_length=1, max_length=32)] = Field(
        None, description="Unique identifier `name` of the Workload.", example="motor-speed-control-ubdhwnshdy67"
    )
    networking: Optional[List[NetworkingItem]] = Field(None, description="Array of services exposed by the workload.")
    node_name: Optional[constr(min_length=1, max_length=64)] = Field(
        None,
        description="Unique identifier `name` of the Node in the Cluster hosting the Workload.",
        example="docs-demo-node-01",
    )
    payload: Optional[Dict[str, Any]] = Field(
        None, description="Internal Kelvin configuration information for deployment of the Workload."
    )
    pre_download: Optional[bool] = Field(
        None,
        description="If true, deploy process is handled by Kelvin and all Workloads wil be downloaded to Edge System before deploy. If false, deploy process is handled by Kubernetes through default settings.",
        example=True,
    )
    status: Optional[WorkloadStatus] = None
    title: Optional[constr(min_length=1)] = Field(
        None, description="Display name (`title`) of the Workload.", example="Motor Speed Control"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Workload keys were last updated, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    staged: Optional[WorkloadStaged] = None


class ThreadContent(DataModelBase):
    """
    ThreadContent object.

    Parameters
    ----------
    attachments: Optional[List[ThreadAttachment]]
    mentions: Optional[List[str]]
    replies: Optional[List[ThreadReply]]
    text: Optional[str]

    """

    attachments: Optional[List[ThreadAttachment]] = None
    mentions: Optional[List[str]] = None
    replies: Optional[List[ThreadReply]] = None
    text: Optional[str] = None


class ThreadReply(DataModelBase):
    """
    ThreadReply object.

    Parameters
    ----------
    content: Optional[ThreadContent]
    created: Optional[datetime]
    id: Optional[str]
    updated: Optional[datetime]
    user_id: Optional[str]

    """

    content: Optional[ThreadContent] = None
    created: Optional[datetime] = None
    id: Optional[str] = None
    updated: Optional[datetime] = None
    user_id: Optional[str] = None


class Thread(DataModelBase):
    """
    Thread object.

    Parameters
    ----------
    content: Optional[ThreadContent]
    created: Optional[datetime]
    follows: Optional[Dict[str, ThreadUserFollow]]
    id: Optional[str]
    related_to: Optional[str]
    type: Optional[str]
    updated: Optional[datetime]
    user_id: Optional[str]

    """

    content: Optional[ThreadContent] = None
    created: Optional[datetime] = None
    follows: Optional[Dict[str, ThreadUserFollow]] = None
    id: Optional[str] = None
    related_to: Optional[str] = None
    type: Optional[str] = None
    updated: Optional[datetime] = None
    user_id: Optional[str] = None


ThreadContent.update_forward_refs()
