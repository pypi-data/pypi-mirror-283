from dataclasses import dataclass
from typing import Self, cast

from jsonalias import Json

from dbnomics_data_model.json_utils.dumping import create_default_dumper, dump_as_json_data
from dbnomics_data_model.json_utils.errors import JsonDumpError, JsonParseTypeError
from dbnomics_data_model.json_utils.loading import create_default_loader, load_json_data
from dbnomics_data_model.json_utils.types import JsonObject
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelDumpError, JsonModelParseError

dumper = create_default_dumper()
loader = create_default_loader()


@dataclass
class BaseJsonObjectModel:
    @classmethod
    def from_json_data(cls, data: Json) -> Self:
        try:
            return load_json_data(data, loader=loader, type_=cls)
        except JsonParseTypeError as exc:
            raise JsonModelParseError(data=data) from exc

    def to_json_data(self) -> JsonObject:
        try:
            data = dump_as_json_data(self, dumper=dumper)
        except JsonDumpError as exc:
            raise JsonModelDumpError(obj=self) from exc
        return cast(JsonObject, data)
