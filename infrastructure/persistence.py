from core.entities import DiagramState


class JSONRepository:
    @staticmethod
    def save(state: DiagramState, path: str):
        with open(path, "w") as f:
            f.write(state.model_dump_json(indent=4))

    @staticmethod
    def load(path: str) -> DiagramState:
        with open(path, "r") as f:
            return DiagramState.model_validate_json(f.read())
