import React, { useState } from 'react';
import { EventType, EventData } from '../types';
import Input from './Input';
import Select from './Select';
import Button from './Button';

interface EventFormProps {
    cattleId: string;
    onSubmit: (data: { type: EventType; event_date: string; data: EventData; notes?: string }) => void;
    onCancel: () => void;
}

const EventForm: React.FC<EventFormProps> = ({ cattleId: _cattleId, onSubmit, onCancel }) => {
    const [eventType, setEventType] = useState<EventType | ''>('');
    const [eventDate, setEventDate] = useState(new Date().toISOString().split('T')[0]);
    const [notes, setNotes] = useState('');

    // Birth fields
    const [calfWeight, setCalfWeight] = useState<number>(0);
    const [calfGender, setCalfGender] = useState<'M' | 'F' | ''>('');
    const [calfArete, setCalfArete] = useState('');
    const [birthType, setBirthType] = useState<'natural' | 'assisted' | 'cesarean' | ''>('');
    const [complications, setComplications] = useState('');

    // Sale fields
    const [buyerId, setBuyerId] = useState('');
    const [saleWeight, setSaleWeight] = useState<number>(0);
    const [pricePerKg, setPricePerKg] = useState<number>(0);
    const [totalPrice, setTotalPrice] = useState<number>(0);
    const [paymentTerms, setPaymentTerms] = useState<'cash' | 'credit' | 'installments' | ''>('');

    // Vaccination fields
    const [vaccineType, setVaccineType] = useState('');
    const [batchNumber, setBatchNumber] = useState('');
    const [doseMl, setDoseMl] = useState<number>(0);
    const [vaccineCost, setVaccineCost] = useState<number>(0);
    const [nextDueDate, setNextDueDate] = useState('');

    // Treatment fields
    const [diagnosis, setDiagnosis] = useState('');
    const [medicine, setMedicine] = useState('');
    const [dosage, setDosage] = useState('');
    const [treatmentCost, setTreatmentCost] = useState<number>(0);

    // Weighing fields
    const [weight, setWeight] = useState<number>(0);
    const [bodyCondition, setBodyCondition] = useState<number>(0);

    // Death fields
    const [deathReason, setDeathReason] = useState('');
    const [ageMonths, setAgeMonths] = useState<number>(0);
    const [valueLost, setValueLost] = useState<number>(0);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!eventType) {
            alert('Por favor selecciona un tipo de evento');
            return;
        }

        const eventData: EventData = {};

        // Build event data based on type
        switch (eventType) {
            case 'birth':
                eventData.calf_weight_kg = calfWeight;
                eventData.calf_gender = calfGender as 'M' | 'F';
                eventData.calf_arete = calfArete;
                eventData.birth_type = birthType as 'natural' | 'assisted' | 'cesarean';
                eventData.complications = complications;
                break;
            case 'sale':
                eventData.buyer_id = buyerId;
                eventData.sale_weight_kg = saleWeight;
                eventData.price_per_kg = pricePerKg;
                eventData.total_price = totalPrice;
                eventData.payment_terms = paymentTerms as 'cash' | 'credit' | 'installments';
                break;
            case 'vaccination':
                eventData.vaccine_type = vaccineType;
                eventData.batch_number = batchNumber;
                eventData.dose_ml = doseMl;
                eventData.cost = vaccineCost;
                eventData.next_due_date = nextDueDate;
                break;
            case 'treatment':
                eventData.diagnosis = diagnosis;
                eventData.medicine = medicine;
                eventData.dosage = dosage;
                eventData.treatment_cost = treatmentCost;
                break;
            case 'weighing':
                eventData.weight_kg = weight;
                eventData.body_condition_score = bodyCondition;
                break;
            case 'death':
                eventData.reason = deathReason;
                eventData.age_months = ageMonths;
                eventData.value_lost = valueLost;
                break;
        }

        onSubmit({
            type: eventType,
            event_date: eventDate,
            data: eventData,
            notes: notes || undefined
        });
    };

    const eventTypeOptions = [
        { value: 'birth', label: 'Nacimiento' },
        { value: 'sale', label: 'Venta' },
        { value: 'vaccination', label: 'Vacunación' },
        { value: 'treatment', label: 'Tratamiento' },
        { value: 'weighing', label: 'Pesaje' },
        { value: 'death', label: 'Muerte' }
    ];

    return (
        <form onSubmit={handleSubmit}>
            <Select
                label="Tipo de Evento"
                value={eventType}
                onChange={(val) => setEventType(val as EventType)}
                options={eventTypeOptions}
                required
            />

            <Input
                type="date"
                label="Fecha del Evento"
                value={eventDate}
                onChange={(val) => setEventDate(val as string)}
                required
            />

            {/* Birth Fields */}
            {eventType === 'birth' && (
                <>
                    <Input
                        type="number"
                        label="Peso del Becerro (kg)"
                        value={calfWeight}
                        onChange={(val) => setCalfWeight(val as number)}
                        min={0}
                        step={0.1}
                        required
                    />
                    <Select
                        label="Sexo del Becerro"
                        value={calfGender}
                        onChange={(val) => setCalfGender(val as 'M' | 'F')}
                        options={[
                            { value: 'M', label: 'Macho' },
                            { value: 'F', label: 'Hembra' }
                        ]}
                        required
                    />
                    <Input
                        label="Número de Arete del Becerro"
                        value={calfArete}
                        onChange={(val) => setCalfArete(val as string)}
                    />
                    <Select
                        label="Tipo de Parto"
                        value={birthType}
                        onChange={(val) => setBirthType(val as any)}
                        options={[
                            { value: 'natural', label: 'Natural' },
                            { value: 'assisted', label: 'Asistido' },
                            { value: 'cesarean', label: 'Cesárea' }
                        ]}
                    />
                    <Input
                        label="Complicaciones"
                        value={complications}
                        onChange={(val) => setComplications(val as string)}
                        placeholder="Describe cualquier complicación..."
                    />
                </>
            )}

            {/* Sale Fields */}
            {eventType === 'sale' && (
                <>
                    <Input
                        label="ID del Comprador"
                        value={buyerId}
                        onChange={(val) => setBuyerId(val as string)}
                        required
                    />
                    <Input
                        type="number"
                        label="Peso de Venta (kg)"
                        value={saleWeight}
                        onChange={(val) => {
                            setSaleWeight(val as number);
                            if (pricePerKg > 0) setTotalPrice((val as number) * pricePerKg);
                        }}
                        min={0}
                        step={0.1}
                        required
                    />
                    <Input
                        type="number"
                        label="Precio por Kg (MXN)"
                        value={pricePerKg}
                        onChange={(val) => {
                            setPricePerKg(val as number);
                            if (saleWeight > 0) setTotalPrice(saleWeight * (val as number));
                        }}
                        min={0}
                        step={0.01}
                        required
                    />
                    <Input
                        type="number"
                        label="Precio Total (MXN)"
                        value={totalPrice}
                        onChange={(val) => setTotalPrice(val as number)}
                        min={0}
                        step={0.01}
                        disabled
                    />
                    <Select
                        label="Términos de Pago"
                        value={paymentTerms}
                        onChange={(val) => setPaymentTerms(val as any)}
                        options={[
                            { value: 'cash', label: 'Contado' },
                            { value: 'credit', label: 'Crédito' },
                            { value: 'installments', label: 'Parcialidades' }
                        ]}
                        required
                    />
                </>
            )}

            {/* Vaccination Fields */}
            {eventType === 'vaccination' && (
                <>
                    <Input
                        label="Tipo de Vacuna"
                        value={vaccineType}
                        onChange={(val) => setVaccineType(val as string)}
                        required
                    />
                    <Input
                        label="Número de Lote"
                        value={batchNumber}
                        onChange={(val) => setBatchNumber(val as string)}
                    />
                    <Input
                        type="number"
                        label="Dosis (ml)"
                        value={doseMl}
                        onChange={(val) => setDoseMl(val as number)}
                        min={0}
                        step={0.1}
                    />
                    <Input
                        type="number"
                        label="Costo (MXN)"
                        value={vaccineCost}
                        onChange={(val) => setVaccineCost(val as number)}
                        min={0}
                        step={0.01}
                    />
                    <Input
                        type="date"
                        label="Próxima Fecha de Vacunación"
                        value={nextDueDate}
                        onChange={(val) => setNextDueDate(val as string)}
                    />
                </>
            )}

            {/* Treatment Fields */}
            {eventType === 'treatment' && (
                <>
                    <Input
                        label="Diagnóstico"
                        value={diagnosis}
                        onChange={(val) => setDiagnosis(val as string)}
                        required
                    />
                    <Input
                        label="Medicina"
                        value={medicine}
                        onChange={(val) => setMedicine(val as string)}
                        required
                    />
                    <Input
                        label="Dosificación"
                        value={dosage}
                        onChange={(val) => setDosage(val as string)}
                        placeholder="Ej: 10ml cada 12 horas"
                    />
                    <Input
                        type="number"
                        label="Costo del Tratamiento (MXN)"
                        value={treatmentCost}
                        onChange={(val) => setTreatmentCost(val as number)}
                        min={0}
                        step={0.01}
                    />
                </>
            )}

            {/* Weighing Fields */}
            {eventType === 'weighing' && (
                <>
                    <Input
                        type="number"
                        label="Peso (kg)"
                        value={weight}
                        onChange={(val) => setWeight(val as number)}
                        min={0}
                        step={0.1}
                        required
                    />
                    <Input
                        type="number"
                        label="Condición Corporal (1-5)"
                        value={bodyCondition}
                        onChange={(val) => setBodyCondition(val as number)}
                        min={1}
                        max={5}
                        step={0.5}
                    />
                </>
            )}

            {/* Death Fields */}
            {eventType === 'death' && (
                <>
                    <Input
                        label="Razón de Muerte"
                        value={deathReason}
                        onChange={(val) => setDeathReason(val as string)}
                        required
                    />
                    <Input
                        type="number"
                        label="Edad (meses)"
                        value={ageMonths}
                        onChange={(val) => setAgeMonths(val as number)}
                        min={0}
                    />
                    <Input
                        type="number"
                        label="Valor Perdido (MXN)"
                        value={valueLost}
                        onChange={(val) => setValueLost(val as number)}
                        min={0}
                        step={0.01}
                    />
                </>
            )}

            {/* Notes (all types) */}
            <div style={{ marginBottom: '1rem' }}>
                <label style={{
                    display: 'block',
                    marginBottom: '0.5rem',
                    fontWeight: 500,
                    fontSize: '0.875rem'
                }}>
                    Notas
                </label>
                <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Notas adicionales..."
                    style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: '2px solid var(--border)',
                        borderRadius: 'var(--radius-md)',
                        fontSize: '1rem',
                        fontFamily: 'inherit',
                        minHeight: '100px',
                        resize: 'vertical'
                    }}
                />
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.5rem' }}>
                <Button variant="secondary" onClick={onCancel} type="button" fullWidth>
                    Cancelar
                </Button>
                <Button variant="primary" type="submit" fullWidth>
                    Guardar Evento
                </Button>
            </div>
        </form>
    );
};

export default EventForm;
