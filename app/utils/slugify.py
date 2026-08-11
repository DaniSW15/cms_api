import re
import unicodedata


def slugify(value: str) -> str:
    """
    Convierte un texto en un slug válido para URLs:
    - Quita acentos
    - Pasa a minúsculas
    - Reemplaza espacios y símbolos por guiones
    - Quita guiones duplicados
    """
    # Normaliza acentos: é → e, ñ → n
    text = unicodedata.normalize("NFKD", value)
    text = text.encode("ascii", "ignore").decode("utf-8")

    # Minúsculas y reemplaza no-alfanuméricos por guiones
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-_")

    return text
