import enum
import json

from typing import Dict, List, Optional, Callable, Tuple, Any


@enum.unique
class StringsLang(enum.StrEnum):
  en = 'en'
  ru = 'ru'


class StringsData:

  def __init__(self):
    self.locals: Dict[Any, Dict[str, str]] = {}

  def loadFiles(
    self,
    files: List[Tuple[str, str]],
  ):
    for locale, file in files:
      self.locals[locale] = json.loads(open(file, 'r', encoding='utf-8').read())


class Strings:

  def __init__(
    self,
    data: StringsData,
    langList: List[Any],
    onUnknownString: Optional[Callable] = None,
  ):
    self.data = data
    self.langList = langList
    self.onUnknownString = onUnknownString

  def setLang(self, lang: Any):
    if lang in self.langList:
      self.langList.remove(lang)
    self.langList.insert(0, lang)

  def __call__(self, string: str) -> str:
    for lang in self.langList:
      data = self.data.locals.get(lang)
      if data is None:
        continue
      value = data.get(string)
      if value is None:
        continue
      return value

    if self.onUnknownString is None:
      return string
    return self.onUnknownString(string)
