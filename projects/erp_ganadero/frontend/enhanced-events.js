// Enhanced Event Forms with Dynamic Fields
// Add this to your index.html to enable enhanced event entry

const EVENT_FIELDS = {
    birth: [
        { name: 'calf_weight_kg', label: 'Peso del Becerro (kg)', type: 'number', required: true },
        { name: 'calf_gender', label: 'Sexo del Becerro', type: 'select', options: [{ value: 'M', label: 'Macho' }, { value: 'F', label: 'Hembra' }], required: true },
        { name: 'calf_arete', label: 'Arete del Becerro', type: 'text', required: true },
        { name: 'complications', label: 'Complicaciones', type: 'text', required: false },
        { name: 'birth_type', label: 'Tipo de Parto', type: 'select', options: [{ value: 'natural', label: 'Natural' }, { value: 'assisted', label: 'Asistido' }, { value: 'cesarean', label: 'Cesárea' }], required: true }
    ],
    sale: [
        { name: 'buyer_name', label: 'Comprador', type: 'text', required: true },
        { name: 'sale_weight_kg', label: 'Peso (kg)', type: 'number', required: true },
        { name: 'price_per_kg', label: 'Precio por kg (MXN)', type: 'number', required: true },
        { name: 'total_price', label: 'Precio Total (MXN)', type: 'number', readonly: true, calculated: true },
        { name: 'payment_terms', label: 'Términos de Pago', type: 'select', options: [{ value: 'cash', label: 'Contado' }, { value: 'credit', label: 'Crédito' }], required: true },
        { name: 'transport_cost', label: 'Costo de Transporte (MXN)', type: 'number', required: false }
    ],
    vaccination: [
        { name: 'vaccine_type', label: 'Tipo de Vacuna', type: 'text', required: true },
        { name: 'batch_number', label: 'Número de Lote', type: 'text', required: false },
        { name: 'dose_ml', label: 'Dosis (ml)', type: 'number', required: true },
        { name: 'cost', label: 'Costo (MXN)', type: 'number', required: false },
        { name: 'next_due_date', label: 'Próxima Fecha', type: 'date', required: false }
    ],
    weighing: [
        { name: 'weight_kg', label: 'Peso (kg)', type: 'number', required: true },
        { name: 'body_condition_score', label: 'Condición Corporal (1-5)', type: 'number', min: 1, max: 5, required: false }
    ],
    treatment: [
        { name: 'diagnosis', label: 'Diagnóstico', type: 'text', required: true },
        { name: 'medicine', label: 'Medicamento', type: 'text', required: true },
        { name: 'dosage', label: 'Dosificación', type: 'text', required: true },
        { name: 'treatment_cost', label: 'Costo (MXN)', type: 'number', required: false }
    ],
    death: [
        { name: 'reason', label: 'Causa de Muerte', type: 'text', required: true },
        { name: 'age_months', label: 'Edad (meses)', type: 'number', required: false },
        { name: 'value_lost', label: 'Valor Perdido (MXN)', type: 'number', required: false }
    ]
};

// Render dynamic fields based on event type
function renderEventFields(eventType) {
    const fields = EVENT_FIELDS[eventType];
    if (!fields) return '';

    return fields.map(field => {
        if (field.type === 'select') {
            return `
                <div class="form-group">
                    <label class="form-label">${field.label} ${field.required ? '*' : ''}</label>
                    <select class="form-select" id="event-${field.name}" ${field.required ? 'required' : ''}>
                        <option value="">Seleccionar...</option>
                        ${field.options.map(opt => `<option value="${opt.value}">${opt.label}</option>`).join('')}
                    </select>
                </div>
            `;
        } else {
            return `
                <div class="form-group">
                    <label class="form-label">${field.label} ${field.required ? '*' : ''}</label>
                    <input 
                        type="${field.type}" 
                        class="form-input" 
                        id="event-${field.name}"
                        ${field.required ? 'required' : ''}
                        ${field.readonly ? 'readonly' : ''}
                        ${field.min ? `min="${field.min}"` : ''}
                        ${field.max ? `max="${field.max}"` : ''}
                        ${field.step ? `step="${field.step}"` : field.type === 'number' ? 'step="0.01"' : ''}
                    >
                </div>
            `;
        }
    }).join('');
}

// Auto-calculate total price for sales
function setupSaleCalculations() {
    const weightInput = document.getElementById('event-sale_weight_kg');
    const priceInput = document.getElementById('event-price_per_kg');
    const totalInput = document.getElementById('event-total_price');

    if (weightInput && priceInput && totalInput) {
        const calculate = () => {
            const weight = parseFloat(weightInput.value) || 0;
            const price = parseFloat(priceInput.value) || 0;
            totalInput.value = (weight * price).toFixed(2);
        };

        weightInput.addEventListener('input', calculate);
        priceInput.addEventListener('input', calculate);
    }
}

// Collect event data from form
function collectEventData(eventType) {
    const fields = EVENT_FIELDS[eventType];
    if (!fields) return {};

    const data = {};
    fields.forEach(field => {
        const input = document.getElementById(`event-${field.name}`);
        if (input) {
            const value = input.type === 'number' ? parseFloat(input.value) : input.value;
            if (value) data[field.name] = value;
        }
    });

    return data;
}

// Usage: Add to your event type change handler
// document.getElementById('event-type').addEventListener('change', function(e) {
//     const container = document.getElementById('dynamic-fields-container');
//     container.innerHTML = renderEventFields(e.target.value);
//     if (e.target.value === 'sale') setupSaleCalculations();
// });
