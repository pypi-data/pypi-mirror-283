import inspect
import types
from typing import Dict, Any, Callable, Optional


class Storage(Dict):

  def __call__(self, providerFun: Any, **kwargs) -> Any:
    if inspect.isclass(providerFun):
      return providerFun.provider(self, **kwargs)
    return providerFun(self, **kwargs)


_storage: Optional[Storage] = None


def storage() -> Storage:
  global _storage  # pylint: disable=W0603
  if _storage is None:
    _storage = Storage()
  return _storage


# decorator
def provider(fun_or_class: Any):
  if isinstance(fun_or_class, types.FunctionType):

    def wrapper(ref: Optional[Storage] = None, **kwargs) -> Any:
      ref = ref or storage()
      key = _calculate_key(fun_or_class, **kwargs)

      value = ref.get(key)
      if value is None:
        value = fun_or_class(ref, **kwargs)
        ref[key] = value
      return value

    return wrapper

  else:

    @provider
    def fun(ref: Storage, **kwargs):
      return fun_or_class(ref, **kwargs)

    fun_or_class.provider = fun
    return fun_or_class


def _calculate_key(fun: Callable, **kwargs) -> str:
  key = str(hash(fun))
  for k, v in kwargs.items():
    key += f'_{k}_{hash(v)}'
  return key
