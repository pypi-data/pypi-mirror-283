import json
import sys


def codegen():
  keys = set()
  for file in sys.argv[1:]:
    data = open(file, 'r', encoding='utf-8').read()
    keys = keys.union(json.loads(data).keys())

  onePropertyTemplate = '  ' + '''
  @property
  def %s(self):
    return self('%s')
'''.strip()

  properties = [onePropertyTemplate % (key, key) for key in sorted(list(keys))]

  print('''
from typing import Optional, List, Callable

from simloc import StringsData, Strings


class AppStrings(Strings):

  def __init__(
    self,
    data: StringsData,
    langList: List[str],
    onUnknownString: Optional[Callable] = None,
  ):
    super().__init__(data, langList, onUnknownString)

'''.strip() + '\n\n' + '\n\n'.join(properties))
