import abc
import json
import pathlib
from openalex import OpenAlex, Work


class LibraryCache(abc.ABC):

    @abc.abstractmethod
    def get_work(self, work_id: str): ...

    @abc.abstractmethod
    def set_work(self, work_id: str, work: dict): ...

    @abc.abstractmethod
    def list_works(self): ...


def _with_cache(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            with open(self.cache_file, "r") as f:
                self._cache = json.load(f)
        except FileNotFoundError:
            self._cache = {}
        return func(*args, **kwargs)

    return wrapper


def _save_cache(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        func(*args, **kwargs)
        with open(self.cache_file, "w") as f:
            json.dump(self._cache, f, default=str)

    return wrapper


class JSONLibraryCache(LibraryCache):

    def __init__(self, cache_file: str | pathlib.Path):
        self.cache_file = cache_file
        self._cache = {}

    @_with_cache
    def get_work(self, work_id: str):
        return self._cache.get(work_id)

    @_with_cache
    @_save_cache
    def set_work(self, work_id: str, work: Work):
        self._cache[work_id] = work.to_dict()

    @_with_cache
    def list_works(self):
        return self._cache.values()


class LibraryManager:

    def __init__(
        self, mailto: str, cache_file: str | pathlib.Path, use_cache: bool = True
    ):
        self._mailto = mailto
        if isinstance(cache_file, str):
            cache_file = pathlib.Path(cache_file)
        if not cache_file.exists():
            cache_file.parent.mkdir(parents=True, exist_ok=True)
        if cache_file.suffix != ".json":
            raise ValueError("Cache file must be a json file")

        self.cache = JSONLibraryCache(cache_file)
        self.cache_file = cache_file
        self.use_cache = use_cache

    def get_work_by_search(self, search_term: str):
        # Check cache
        if self.use_cache:
            for work in self.cache.list_works():
                # TODO: Fuzzy search
                # if search_term.lower() in work["title"].lower():
                #     return Work(**work)
                terms_are_in_title = [
                    1
                    for term in search_term.split()
                    if term.lower() in work["title"].lower()
                ]
                if len(terms_are_in_title) / len(search_term.split()) > 0.80:
                    return Work(**work)
        oa = OpenAlex(mailto=self._mailto)
        work = oa.get_work_by_search(search_term)
        if self.use_cache:
            self.cache.set_work(work.id, work)
        return work
