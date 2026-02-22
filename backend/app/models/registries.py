class FakeRegistry:
    def __init__(self):
        self._registers = []

    def first(self):
        return self._registers[0] if len(self._registers) > 0 else None

    def last(self):
        return self._registers[-1] if len(self._registers) > 0 else None

    def all(self):
        return self._registers

    def append(self, item):
        self._registers.append(item)