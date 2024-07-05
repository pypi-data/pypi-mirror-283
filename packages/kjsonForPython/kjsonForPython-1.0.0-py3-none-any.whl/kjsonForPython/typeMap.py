from typing import Dict, Callable, Any, List
from abc import ABC, abstractmethod
import datetime


class KDate(datetime.datetime):
    isKDate = True


class NaN:
    def __str__(self):
        return "<KJsonValue: NaN>"

    pass


class SpecialValueType(ABC):
    @abstractmethod
    def matcher(
        self,
        target: Any,
        saveList: List[Any],
        dataMap: List[Any],
        dfsTransform: Callable[[Any], Any],
    ) -> None | str:
        pass

    def replacer(self, value: str, saveList: List[Any]) -> Any:
        pass


class KJsonDate(SpecialValueType):
    def matcher(
        self,
        target,
        saveList,
        dataMap,
        dfsTransform,
    ):
        if isinstance(target, datetime.datetime) and not isinstance(saveList, KDate):
            return str(target.timestamp() * 1000)
        return None

    def replacer(self, value, saveList):
        return datetime.datetime.fromtimestamp(int(value) / 1000)


class KJsonKDate(SpecialValueType):
    def matcher(
        self,
        target,
        saveList,
        dataMap,
        dfsTransform,
    ):
        if isinstance(target, KDate):
            return str(target.timestamp() * 1000)
        return None

    def replacer(self, value, saveList):
        return KDate.fromtimestamp(int(value) / 1000)


class KJsonNaN(SpecialValueType):
    def matcher(
        self,
        target,
        saveList,
        dataMap,
        dfsTransform,
    ) -> None | str:
        if isinstance(target, NaN):
            return ""
        return None

    def replacer(self, value: str, saveList: List[Any]):
        return NaN()


class KJsonTypeNull(SpecialValueType):

    def matcher(
        self,
        target,
        saveList,
        dataMap,
        dfsTransform,
    ) -> None | str:
        if target is None:
            return ""
        return None

    def replacer(self, value, saveList: List[Any]):
        return None


class KJsonString(SpecialValueType):

    def matcher(
        self,
        target,
        saveList,
        dataMap,
        dfsTransform,
    ) -> None | str:
        if isinstance(target, str):
            return target
        return None

    def replacer(self, value: str, saveList: List[Any]):
        return value


class KJsonArray(SpecialValueType):
    def matcher(
        self,
        target,
        saveList,
        dataMap,
        dfsTransform,
    ) -> None | str:
        if not isinstance(target, list):
            return None
        try:
            return str(dataMap.index(target))
        except:
            pass
        id=len(dataMap)
        saveList.append(None)
        dataMap.append(target)
        saveList[id]=[dfsTransform(item) for item in target]
        return str(id)

    def replacer(self, value: str, saveList: List[Any]):
        print(saveList)
        return saveList[int(value)]

class KJsonObject(SpecialValueType):
    def matcher(
        self,
        target,
        saveList,
        dataMap,
        dfsTransform,
    ) -> None | str:
        if not isinstance(target, dict):
            return None
        try:
            return str(dataMap.index(target))
        except:
            pass
        id=len(dataMap)
        saveList.append(None)
        dataMap.append(target)
        saveList[id]={key:dfsTransform(value) for key,value in target.items()}
        return str(id)

    def replacer(self, value: str, saveList: List[Any]):
        return saveList[int(value)]

typeMap: Dict[str, SpecialValueType] = {
    "date": KJsonDate(),
    "kdate": KJsonKDate(),
    "nan": KJsonNaN(),
    "null": KJsonTypeNull(),
    "string": KJsonString(),
    "array": KJsonArray(),
    "object": KJsonObject(),
}
