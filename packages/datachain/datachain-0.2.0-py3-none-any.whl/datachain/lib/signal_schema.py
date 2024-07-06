import copy
from collections.abc import Iterator, Sequence
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional, Union, get_args, get_origin

from pydantic import create_model

from datachain.lib.arrow import Source
from datachain.lib.feature import (
    DATACHAIN_TO_TYPE,
    DEFAULT_DELIMITER,
    Feature,
    FeatureType,
    convert_type_to_datachain,
)
from datachain.lib.feature_registry import Registry
from datachain.lib.file import File, TextFile
from datachain.lib.image import ImageFile
from datachain.lib.utils import DataChainParamsError
from datachain.lib.webdataset import TarStream, WDSAllFile, WDSBasic
from datachain.lib.webdataset_laion import Laion, WDSLaion

if TYPE_CHECKING:
    from datachain.catalog import Catalog


# TODO fix hardcoded Feature class names with://github.com/iterative/dvcx/issues/1625
NAMES_TO_TYPES = {
    "int": int,
    "str": str,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "bytes": bytes,
    "datetime": datetime,
    "WDSLaion": WDSLaion,
    "Laion": Laion,
    "Source": Source,
    "File": File,
    "ImageFile": ImageFile,
    "TextFile": TextFile,
    "TarStream": TarStream,
    "WDSBasic": WDSBasic,
    "WDSAllFile": WDSAllFile,
}


class SignalSchemaError(DataChainParamsError):
    pass


class SignalResolvingError(SignalSchemaError):
    def __init__(self, path: Optional[list[str]], msg: str):
        name = " '" + ".".join(path) + "'" if path else ""
        super().__init__(f"cannot resolve signal name{name}: {msg}")


class SignalResolvingTypeError(SignalResolvingError):
    def __init__(self, method: str, field):
        super().__init__(
            None,
            f"{method} supports only `str` type"
            f" while '{field}' has type '{type(field)}'",
        )


class SignalSchema:
    def __init__(self, values: dict[str, FeatureType]):
        self.values = values
        self.tree = self._build_tree()

    @staticmethod
    def from_column_types(col_types: dict[str, Any]) -> "SignalSchema":
        signals: dict[str, FeatureType] = {}
        for field, type_ in col_types.items():
            type_ = DATACHAIN_TO_TYPE.get(type_, None)
            if type_ is None:
                raise SignalSchemaError(
                    f"signal schema cannot be obtained for column '{field}':"
                    f" unsupported type '{type_}'"
                )
            signals[field] = type_
        return SignalSchema(signals)

    def serialize(self) -> dict[str, str]:
        signals = {}
        for name, fr_type in self.values.items():
            if Feature.is_feature(fr_type):
                signals[name] = fr_type._name()  # type: ignore[union-attr]
            else:
                orig = get_origin(fr_type)
                args = get_args(fr_type)
                # Check if fr_type is Optional
                if orig == Union and len(args) == 2 and (type(None) in args):
                    fr_type = args[0]
                signals[name] = fr_type.__name__
        return signals

    @staticmethod
    def deserialize(schema: dict[str, str]) -> "SignalSchema":
        if not isinstance(schema, dict):
            raise SignalSchemaError(f"cannot deserialize signal schema: {schema}")

        signals: dict[str, FeatureType] = {}
        for signal, type_name in schema.items():
            try:
                fr = NAMES_TO_TYPES.get(type_name)
                if not fr:
                    type_name, version = Registry.parse_name_version(type_name)
                    fr = Registry.get(type_name, version)
            except TypeError as err:
                raise SignalSchemaError(
                    f"cannot deserialize '{signal}': {err}"
                ) from err

            if not fr:
                raise SignalSchemaError(
                    f"cannot deserialize '{signal}': unsupported type '{type_name}'"
                )
            signals[signal] = fr

        return SignalSchema(signals)

    def to_udf_spec(self) -> dict[str, Any]:
        res = {}
        for path, type_, has_subtree, _ in self.get_flat_tree():
            if not has_subtree:
                db_name = DEFAULT_DELIMITER.join(path)
                res[db_name] = convert_type_to_datachain(type_)
        return res

    def row_to_objs(self, row: Sequence[Any]) -> list[FeatureType]:
        objs = []
        pos = 0
        for fr_type in self.values.values():
            if Feature.is_feature(fr_type):
                j, pos = fr_type._unflatten_to_json_pos(row, pos)  # type: ignore[union-attr]
                objs.append(fr_type(**j))
            else:
                objs.append(row[pos])
                pos += 1
        return objs  # type: ignore[return-value]

    def contains_file(self) -> bool:
        return any(
            fr._is_file  # type: ignore[union-attr]
            for fr in self.values.values()
            if Feature.is_feature(fr)
        )

    def slice(self, keys: Sequence[str]) -> "SignalSchema":
        return SignalSchema({k: v for k, v in self.values.items() if k in keys})

    def row_to_features(self, row: Sequence, catalog: "Catalog") -> list[FeatureType]:
        res = []
        pos = 0
        for fr_cls in self.values.values():
            if not Feature.is_feature(fr_cls):
                res.append(row[pos])
                pos += 1
            else:
                json, pos = fr_cls._unflatten_to_json_pos(row, pos)  # type: ignore[union-attr]
                obj = fr_cls(**json)
                if isinstance(obj, File):
                    obj._set_stream(catalog)
                res.append(obj)
        return res

    def db_signals(self) -> list[str]:
        return [
            DEFAULT_DELIMITER.join(path)
            for path, _, has_subtree, _ in self.get_flat_tree()
            if not has_subtree
        ]

    def resolve(self, *names: str) -> "SignalSchema":
        schema = {}
        for field in names:
            if not isinstance(field, str):
                raise SignalResolvingTypeError("select()", field)
            schema[field] = self._find_in_tree(field.split("."))

        return SignalSchema(schema)

    def _find_in_tree(self, path: list[str]) -> FeatureType:
        curr_tree = self.tree
        curr_type = None
        i = 0
        while curr_tree is not None and i < len(path):
            if val := curr_tree.get(path[i], None):
                curr_type, curr_tree = val
            else:
                curr_type = None
            i += 1

        if curr_type is None:
            raise SignalResolvingError(path, "is not found")

        return curr_type

    def select_except_signals(self, *args: str) -> "SignalSchema":
        schema = copy.deepcopy(self.values)
        for field in args:
            if not isinstance(field, str):
                raise SignalResolvingTypeError("select_except()", field)

            if field not in self.values:
                raise SignalResolvingError(
                    field.split("."),
                    "select_except() error - the feature name does not exist or "
                    "inside of feature (not supported)",
                )
            del schema[field]

        return SignalSchema(schema)

    def clone_without_file_signals(self) -> "SignalSchema":
        schema = copy.deepcopy(self.values)

        for signal in File._datachain_column_types:
            if signal in schema:
                del schema[signal]
        return SignalSchema(schema)

    def merge(
        self,
        right_schema: "SignalSchema",
        rname: str,
    ) -> "SignalSchema":
        schema_right = {
            rname + key if key in self.values else key: type_
            for key, type_ in right_schema.values.items()
        }

        return SignalSchema(self.values | schema_right)

    def get_file_signals(self) -> Iterator[str]:
        for path, type_, has_subtree, _ in self.get_flat_tree():
            if has_subtree and issubclass(type_, File):
                yield ".".join(path)

    def get_file_signals_values(self, row: dict[str, Any]) -> dict[str, Any]:
        """
        Method that returns values with clean field names (without prefix) for
        all file signals found in this schema for some row
        Output example:
        {
            laion.file: {
                "source": "s3://ldb-public",
                "name": "dog.jpg",
                ...
            },
            meta.file: {
                "source": "s3://datacomp",
                "name": "cat.jpg",
                ...
            }
        }
        """
        res = {}

        for file_signals in self.get_file_signals():
            prefix = file_signals.replace(".", DEFAULT_DELIMITER) + DEFAULT_DELIMITER
            res[file_signals] = {
                c_name.removeprefix(prefix): c_value
                for c_name, c_value in row.items()
                if c_name.startswith(prefix)
                and DEFAULT_DELIMITER not in c_name.removeprefix(prefix)
            }

        return res

    def create_model(self, name: str) -> type[Feature]:
        fields = {key: (value, None) for key, value in self.values.items()}

        return create_model(
            name,
            __base__=(Feature,),  # type: ignore[call-overload]
            **fields,
        )

    def _build_tree(self) -> dict[str, Any]:
        res = {}

        for name, val in self.values.items():
            subtree = val.build_tree() if Feature.is_feature(val) else None  # type: ignore[union-attr]
            res[name] = (val, subtree)

        return res

    def get_flat_tree(self) -> Iterator[tuple[list[str], type, bool, int]]:
        yield from self._get_flat_tree(self.tree, [], 0)

    def _get_flat_tree(
        self, tree: dict, prefix: list[str], depth: int
    ) -> Iterator[tuple[list[str], type, bool, int]]:
        for name, (type_, substree) in tree.items():
            suffix = name.split(".")
            new_prefix = prefix + suffix
            has_subtree = substree is not None
            yield new_prefix, type_, has_subtree, depth
            if substree is not None:
                yield from self._get_flat_tree(substree, new_prefix, depth + 1)

    def print_tree(self, indent: int = 4, start_at: int = 0):
        for path, type_, _, depth in self.get_flat_tree():
            total_indent = start_at + depth * indent
            print(" " * total_indent, f"{path[-1]}:", SignalSchema._type_to_str(type_))

            if get_origin(type_) is list:
                args = get_args(type_)
                if len(args) > 0 and Feature.is_feature(args[0]):
                    sub_schema = SignalSchema({"* list of": args[0]})
                    sub_schema.print_tree(indent=indent, start_at=total_indent + indent)

    @staticmethod
    def _type_to_str(type_):
        if get_origin(type_) == Union:
            args = get_args(type_)
            formatted_types = ", ".join(SignalSchema._type_to_str(arg) for arg in args)
            return f"Union[{formatted_types}]"
        if get_origin(type_) == Optional:
            args = get_args(type_)
            type_str = SignalSchema._type_to_str(args[0])
            return f"Optional[{type_str}]"
        if get_origin(type_) is list:
            args = get_args(type_)
            type_str = SignalSchema._type_to_str(args[0])
            return f"list[{type_str}]"
        if get_origin(type_) is dict:
            args = get_args(type_)
            type_str = SignalSchema._type_to_str(args[0])
            vals = f", {SignalSchema._type_to_str(args[1])}" if len(args) > 1 else ""
            return f"dict[{type_str}{vals}]"
        return type_.__name__
