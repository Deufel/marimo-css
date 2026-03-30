from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Issue:
    file: str
    line: int
    level: str  # "warn" | "error"
    msg: str

@dataclass
class Report:
    properties: list = field(default_factory=list)
    layers_declared: list = field(default_factory=list)
    layers_used: dict = field(default_factory=lambda: defaultdict(list))
    var_decls: set = field(default_factory=set)
    var_refs: set = field(default_factory=set)
    issues: list = field(default_factory=list)
    total_lines: int = 0
    total_bytes: int = 0

    @property
    def errors(self) -> int:
        return sum(1 for i in self.issues if i.level == "error")

    @property
    def warns(self) -> int:
        return sum(1 for i in self.issues if i.level == "warn")
