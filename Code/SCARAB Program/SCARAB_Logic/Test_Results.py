from dataclasses import dataclass

@dataclass
class test_result:
    def __init__(self):
        self.pins_ok: bool | None = None
        self.checksum_ok: bool | None = None
        self.retention_ok: bool | None = None