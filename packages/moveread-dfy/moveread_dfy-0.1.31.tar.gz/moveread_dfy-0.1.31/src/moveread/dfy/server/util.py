from typing import TypeVar, Generic, Callable, Iterable
from time import time

K = TypeVar('K')
T = TypeVar('T')

class TimedIterableCache(Generic[K, T]):
  def __init__(self, get: Callable[[K], Iterable[T]], *, ttl_secs: float, max_entries: int):
    self._get = get
    self.ttl_secs = ttl_secs
    self._cache: dict[K, tuple[list[T], float]] = {}
    self.max_entries = max_entries

  def insert(self, k: K, access_time: float | None = None) -> Iterable[T]:
    access_time = access_time or time()
    if len(self._cache) >= self.max_entries:
      older_client = min(self._cache.keys(), key=self._cache.__getitem__)
      del self._cache[older_client]
    
    def gen():
      stored = []
      for x in self._get(k):
        stored.append(x)
        yield x
      self._cache[k] = stored, access_time

    yield from gen()


  def __getitem__(self, key: K) -> Iterable[T]:
    now = time()
    if key not in self._cache or now - self._cache[key][1] > self.ttl_secs:
      yield from self.insert(key, now)
    else:
      yield from self._cache[key][0]