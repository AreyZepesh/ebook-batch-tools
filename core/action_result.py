from dataclasses import dataclass, field

@dataclass
class ActionResult():
    change_confirmed: bool = field(default=False)
    safe_to_remove_source: bool = field(default=False)

    def can_remove_source(self):
        return self.change_confirmed and self.safe_to_remove_source