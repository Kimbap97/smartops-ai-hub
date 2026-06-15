import json
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

# Importamos las herramientas de SQL y MongoDB que creamos antes
from .models import AIAutomationSummary  # <-- SQL
from .mongo_db import MongoDBManager     # <-- MongoDB
from .ai_engine import AIEngineOrchestrator

def dashboard_index(request):
    """Llama a SQL para traer los últimos 5 registros y mostrarlos en el HTML"""
    recent_actions = AIAutomationSummary.objects.all().order_by('-created_at')[:5]
    return render(request, 'dashboard.html', {'recent_actions': recent_actions})

def process_automation_api(request):
    """API que unifica y coordina los datos de la IA, MongoDB y SQL"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        raw_text = data.get('text', '').strip()

        if not raw_text:
            return JsonResponse({'success': False, 'error': 'Texto vacío'}, status=400)

        # Paso 1: Procesar con el motor de IA
        ai_result = AIEngineOrchestrator.analyze_text(raw_text)

        # Paso 2: LLAMADA A MONGODB (Guardamos el payload completo y flexible)
        mongo_payload = {
            "raw_input": raw_text,
            "ai_analysis": ai_result,
            "execution_timestamp": datetime.utcnow().isoformat()
        }
        mongo_manager = MongoDBManager()
        id_de_mongo = mongo_manager.save_log(mongo_payload) # <-- Guardado en NoSQL ejecutado

        # Paso 3: LLAMADA A SQL (Guardamos el resumen estructurado vinculando el ID de Mongo)
        sql_summary = AIAutomationSummary.objects.create(
            category_detected=ai_result['category'],
            sentiment_score=ai_result['sentiment'],
            mongo_log_id=id_de_mongo # <-- Vinculación hecha en SQL
        )

        # Devolvemos la respuesta al Frontend (JavaScript)
        return JsonResponse({
            'success': True,
            'mongo_id': id_de_mongo,
            'sql_id': sql_summary.id,
            'ai_analysis': ai_result
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
