from django.db import models

class AIAutomationSummary(models.Model):
    """
    TABLA SQL: Guarda datos críticos, relacionales y estructurados.
    Ideal para métricas rápidas, paneles de control y auditorías.
    """
    action_name = models.CharField(max_length=150, default="Clasificación Automática por IA")
    category_detected = models.CharField(max_length=100)
    sentiment_score = models.CharField(max_length=50)

    # ESTE ES EL VÍNCULO: Guardamos el ID de MongoDB aquí para conectar ambas bases de datos
    mongo_log_id = models.CharField(
        max_length=100,
        help_text="Clave foránea lógica que apunta al documento detallado en MongoDB"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category_detected} - {self.created_at}"
