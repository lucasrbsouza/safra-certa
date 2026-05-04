from app.core.exceptions import InvalidCostDataError


class CropType:
    SOJA = "soja"
    MILHO = "milho"
    FEIJAO = "feijao"
    VALID: frozenset[str] = frozenset({SOJA, MILHO, FEIJAO})

    @classmethod
    def validate(cls, value: str) -> str:
        normalized = value.lower().strip()
        if normalized not in cls.VALID:
            raise InvalidCostDataError(
                f"Tipo de cultura '{value}' inválido. Opções: {sorted(cls.VALID)}"
            )
        return normalized
