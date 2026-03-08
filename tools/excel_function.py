from dataclasses import dataclass


@dataclass
class ExcelFunction:
    func_name: str = ""
    func_type: str = ""
    func_desc: str = ""
    func_uuid: str = ""
    func_applies: list[str] = ""
    func_syntax: list[str] = ""
