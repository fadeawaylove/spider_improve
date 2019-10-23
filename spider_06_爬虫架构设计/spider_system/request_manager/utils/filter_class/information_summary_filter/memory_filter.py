from . import BaseFilter


class MemoryFilter(BaseFilter):

    def __init__(self, *args, **kwargs):
        super(MemoryFilter, self).__init__(*args, **kwargs)

    def _save(self, hash_value):
        self.storage.add(hash_value)
        return hash_value

    def _is_exists(self, hash_value):
        return hash_value in self.storage

    def _get_storage(self):
        return set()
