from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path


class Command(BaseCommand):
    help = "Carga respaldo inicial de Material Control CM"

    def handle(self, *args, **kwargs):

        archivo = Path("respaldo_cm.json")

        if not archivo.exists():
            self.stdout.write(
                self.style.ERROR(
                    "No se encontró respaldo_cm.json"
                )
            )
            return

        self.stdout.write(
            self.style.WARNING(
                "Cargando respaldo..."
            )
        )

        call_command(
            "loaddata",
            str(archivo)
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Respaldo cargado correctamente"
            )
        )