from typing import Dict, Callable, Any, List
from abc import ABC, abstractmethod
import re
from .typeMap import typeMap
import json


def structureKJSONList(data: Any) -> Any:
    if not isinstance(data, list):
        return data

    def dfsTransform(data: Any, saveList: List[Any]) -> Any:
        returnValue = data
        if isinstance(data, list):
            for value in range(len(data)):
                data[value] = dfsTransform(data[value], saveList)
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = dfsTransform(value, saveList)
        if isinstance(data, str):
            result = re.match(r"^(.*)::([a-zA-Z\d]+)$", data, flags=re.S)
            if result == None:
                raise ValueError(
                    "Invalid K-JSON data which is string but could not be parsed"
                )
            result = result.groups()
            if len(result) < 2:
                raise ValueError("Invalid K-JSON data which has unknown type")
            data = result[0]
            ty = result[1]
            flag = False
            for key, value in typeMap.items():
                if key == ty:
                    flag = True
                    returnValue = value.replacer(data, saveList)
            if not flag:
                raise ValueError("Invalid K-JSON data which has unknown type")
        return returnValue

    return dfsTransform(data, data)[0]


def parse(data: str) -> Any:
    try:
        dataList = json.loads(data)
        return structureKJSONList(dataList)
    except:
        raise ValueError("Invalid K-JSON data")


def normalizeToKJSONList(obj: Any) -> Any:
    saveList: List[Any] = []
    dataMap: List[Any] = []

    def dfsTransform(obj: Any) -> Any:
        for key, value in typeMap.items():
            result = value.matcher(obj, saveList, dataMap, dfsTransform)
            if result != None:
                return f"{result}::{key}"
        return obj

    result = dfsTransform(obj)
    return saveList if len(saveList) else result


def stringify(data: Any) -> str:
    return json.dumps(normalizeToKJSONList(data))
