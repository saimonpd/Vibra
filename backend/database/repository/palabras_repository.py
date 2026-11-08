from pathlib import Path
import json
from datetime import datetime

class RepositorioPalabras:
    def __init__(self, ruta_fichero: Path):
        self.fichero = ruta_fichero

    def guardar(self, palabra:str, sentimiento: str, fecha: str) -> dict:
        """Añade una nueva palabra y su informacion al fichero JSONL."""
        registro = {
            "palabra": palabra,
            "sentimiento": sentimiento,
            "fecha": fecha
        }
        
        with open(self.fichero, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
            
        return registro

    def obtener_por_dia(self, dia: str | None = None) -> list:
        """Lee el fichero y filtra opcionalmente por día."""
        if not self.fichero.exists():
            return []
            
        resultado = []
        with open(self.fichero, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                registro = json.loads(linea)
                if dia is None or registro["fecha"].startswith(dia):
                    resultado.append(registro)
        return resultado

    def contar_registros(self) -> int:
        """Cuenta el total de registros en el fichero."""
        if not self.fichero.exists():
            return 0
        with open(self.fichero, "r", encoding="utf-8") as f:
            return sum(1 for linea in f if linea.strip())