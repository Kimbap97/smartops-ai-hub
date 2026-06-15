document
    .getElementById('ai-automation-form')
    .addEventListener('submit', async e => {
        e.preventDefault();

        const textInput = document.getElementById('ai-raw-input').value.trim();
        const consoleOutput = document.getElementById('ai-console-output');
        const sqlTableBody = document.getElementById('sql-table-body');
        const noDataRow = document.getElementById('no-data-row');

        if (!textInput) {
            alert('Por favor introduce una cadena de texto para procesar.');
            return;
        }

        // Activando estado de carga visual en la consola
        consoleOutput.innerHTML = `
        <div class="console-placeholder">
            <div class="pulse-icon">⚡</div>
            <p>Ejecutando algoritmos analíticos e inyectando datos...</p>
        </div>
    `;

        try {
            const response = await fetch('/api/process/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ text: textInput }),
            });

            const result = await response.json();

            if (result.success) {
                const ai = result.ai_analysis;

                // 1. Pintar dinámicamente el resultado analítico de la IA
                consoleOutput.innerHTML = `
                <div class="ai-output-box">
                    <h4>Pipeline Ejecutado con Éxito</h4>
                    <div class="ai-stat"><strong>Categoría:</strong> ${ai.category}</div>
                    <div class="ai-stat"><strong>Sentimiento Predictivo:</strong> ${ai.sentiment}</div>
                    <div class="ai-stat"><strong>Acción de Automatización:</strong> ${ai.suggested_action}</div>
                    <div class="ai-stat"><strong>Confianza del Modelo:</strong> ${(ai.confidence_score * 100).toFixed(0)}%</div>
                    <hr style="border:0; border-top:1px solid #222f44; margin:1rem 0;">
                    <div class="ai-stat" style="font-size:0.8rem; color:#94a3b8;">
                        <strong>Log NoSQL (MongoDB ID):</strong> <span class="mono-text">${result.mongo_id}</span>
                    </div>
                    <div class="ai-stat" style="font-size:0.8rem; color:#94a3b8;">
                        <strong>Estado Cluster Mongo:</strong> <span style="color:#10b981;">${result.mongo_status}</span>
                    </div>
                </div>
            `;

                // 2. Insertar inmediatamente la nueva fila relacional en la tabla SQL (UI interactiva)
                if (noDataRow) noDataRow.remove();

                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                <td>#${result.sql_id}</td>
                <td>Clasificación Automática por IA</td>
                <td><span class="tag-cat">${ai.category}</span></td>
                <td>${ai.sentiment}</td>
                <td class="mono-text">${result.mongo_id.substring(0, 15)}...</td>
            `;
                sqlTableBody.insertBefore(newRow, sqlTableBody.firstChild);

                // Limpiar formulario
                document.getElementById('ai-raw-input').value = '';
            } else {
                showError(consoleOutput, result.error);
            }
        } catch (err) {
            showError(consoleOutput, 'Error crítico de conexión de red.');
        }
    });

function showError(container, message) {
    container.innerHTML = `
        <div class="console-placeholder" style="color:#ef4444;">
            <div>❌</div>
            <p style="margin-top:10px;">${message}</p>
        </div>
    `;
}

// Función estándar para leer cookies de Django (CSRF Token)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}
