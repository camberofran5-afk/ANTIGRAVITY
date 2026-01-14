import React, { useState } from 'react';

interface Event {
    id: string;
    type: string;
    event_date: string;
    data: any;
    notes?: string;
}

interface EventTimelineProps {
    events: Event[];
}

const EventTimeline: React.FC<EventTimelineProps> = ({ events }) => {
    const [filterType, setFilterType] = useState<string>('all');
    const [expandedEvent, setExpandedEvent] = useState<string | null>(null);

    const eventTypes = [
        { value: 'all', label: 'Todos', icon: '📋' },
        { value: 'weighing', label: 'Pesaje', icon: '⚖️' },
        { value: 'vaccination', label: 'Vacunación', icon: '💉' },
        { value: 'treatment', label: 'Tratamiento', icon: '🏥' },
        { value: 'pregnancy_check', label: 'Chequeo Preñez', icon: '🤰' },
        { value: 'birth', label: 'Nacimiento', icon: '👶' },
        { value: 'sale', label: 'Venta', icon: '💰' }
    ];

    const getEventIcon = (type: string): string => {
        const found = eventTypes.find(t => t.value === type);
        return found?.icon || '📋';
    };

    const getEventLabel = (type: string): string => {
        const found = eventTypes.find(t => t.value === type);
        return found?.label || type;
    };

    const formatEventData = (event: Event): string => {
        switch (event.type) {
            case 'weighing':
                return `Peso: ${event.data.weight_kg} kg`;
            case 'vaccination':
                return `Vacuna: ${event.data.vaccine_type || 'N/A'}`;
            case 'treatment':
                return `Diagnóstico: ${event.data.diagnosis || 'N/A'}`;
            case 'pregnancy_check':
                return `Resultado: ${event.data.result === 'positive' ? 'Positivo' : event.data.result === 'negative' ? 'Negativo' : 'N/A'}`;
            case 'birth':
                return `Cría: ${event.data.calf_id || 'N/A'} - ${event.data.calf_weight_kg || 'N/A'} kg`;
            case 'sale':
                return `Precio: $${event.data.total_price || 'N/A'} - ${event.data.weight_kg || 'N/A'} kg`;
            default:
                return '';
        }
    };

    const filteredEvents = filterType === 'all'
        ? events
        : events.filter(e => e.type === filterType);

    return (
        <div style={{ width: '100%' }}>
            {/* Filter Buttons */}
            <div style={{
                display: 'flex',
                gap: '8px',
                marginBottom: '20px',
                flexWrap: 'wrap',
                padding: '12px',
                backgroundColor: '#f5f5f5',
                borderRadius: '8px'
            }}>
                {eventTypes.map(type => (
                    <button
                        key={type.value}
                        onClick={() => setFilterType(type.value)}
                        style={{
                            padding: '8px 16px',
                            border: 'none',
                            borderRadius: '20px',
                            backgroundColor: filterType === type.value ? '#4CAF50' : 'white',
                            color: filterType === type.value ? 'white' : '#555',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: filterType === type.value ? 600 : 400,
                            transition: 'all 0.2s',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px',
                            boxShadow: filterType === type.value ? '0 2px 4px rgba(0,0,0,0.2)' : '0 1px 2px rgba(0,0,0,0.1)'
                        }}
                        onMouseEnter={(e) => {
                            if (filterType !== type.value) {
                                e.currentTarget.style.backgroundColor = '#e8f5e9';
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (filterType !== type.value) {
                                e.currentTarget.style.backgroundColor = 'white';
                            }
                        }}
                    >
                        <span>{type.icon}</span>
                        <span>{type.label}</span>
                    </button>
                ))}
            </div>

            {/* Event Count */}
            <div style={{
                marginBottom: '16px',
                color: '#666',
                fontSize: '14px',
                fontWeight: 500
            }}>
                Mostrando {filteredEvents.length} de {events.length} eventos
            </div>

            {/* Timeline */}
            {filteredEvents.length === 0 ? (
                <div style={{
                    textAlign: 'center',
                    padding: '60px 20px',
                    color: '#999'
                }}>
                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>📭</div>
                    <p>No hay eventos de este tipo</p>
                </div>
            ) : (
                <div style={{ position: 'relative' }}>
                    {/* Timeline Line */}
                    <div style={{
                        position: 'absolute',
                        left: '20px',
                        top: '0',
                        bottom: '0',
                        width: '2px',
                        backgroundColor: '#e0e0e0'
                    }} />

                    {/* Events */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {filteredEvents.map((event, index) => (
                            <div
                                key={event.id}
                                style={{
                                    position: 'relative',
                                    paddingLeft: '56px',
                                    animation: `slideIn 0.3s ease-out ${index * 0.05}s both`
                                }}
                            >
                                {/* Timeline Dot */}
                                <div style={{
                                    position: 'absolute',
                                    left: '11px',
                                    top: '16px',
                                    width: '20px',
                                    height: '20px',
                                    borderRadius: '50%',
                                    backgroundColor: '#4CAF50',
                                    border: '3px solid white',
                                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '10px'
                                }}>
                                    {getEventIcon(event.type)}
                                </div>

                                {/* Event Card */}
                                <div
                                    style={{
                                        backgroundColor: 'white',
                                        borderRadius: '8px',
                                        padding: '16px',
                                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                                        border: '1px solid #e0e0e0',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                    onClick={() => setExpandedEvent(expandedEvent === event.id ? null : event.id)}
                                    onMouseEnter={(e) => {
                                        e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.15)';
                                        e.currentTarget.style.borderColor = '#4CAF50';
                                    }}
                                    onMouseLeave={(e) => {
                                        e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                                        e.currentTarget.style.borderColor = '#e0e0e0';
                                    }}
                                >
                                    {/* Header */}
                                    <div style={{
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'flex-start',
                                        marginBottom: '8px'
                                    }}>
                                        <div>
                                            <div style={{
                                                fontWeight: 600,
                                                color: '#2c3e50',
                                                fontSize: '16px',
                                                marginBottom: '4px'
                                            }}>
                                                {getEventLabel(event.type)}
                                            </div>
                                            <div style={{
                                                color: '#555',
                                                fontSize: '14px'
                                            }}>
                                                {formatEventData(event)}
                                            </div>
                                        </div>
                                        <div style={{
                                            color: '#999',
                                            fontSize: '13px',
                                            textAlign: 'right'
                                        }}>
                                            {new Date(event.event_date).toLocaleDateString('es-MX', {
                                                day: 'numeric',
                                                month: 'short',
                                                year: 'numeric'
                                            })}
                                        </div>
                                    </div>

                                    {/* Expanded Details */}
                                    {expandedEvent === event.id && (
                                        <div style={{
                                            marginTop: '12px',
                                            paddingTop: '12px',
                                            borderTop: '1px solid #e0e0e0',
                                            animation: 'fadeIn 0.2s ease-out'
                                        }}>
                                            {event.notes && (
                                                <div style={{
                                                    backgroundColor: '#f5f5f5',
                                                    padding: '12px',
                                                    borderRadius: '6px',
                                                    marginBottom: '8px'
                                                }}>
                                                    <strong style={{ fontSize: '13px', color: '#666' }}>Notas:</strong>
                                                    <p style={{ margin: '4px 0 0 0', fontSize: '14px', color: '#555' }}>
                                                        {event.notes}
                                                    </p>
                                                </div>
                                            )}
                                            <div style={{ fontSize: '12px', color: '#999' }}>
                                                ID: {event.id}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <style>{`
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateX(-20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }
                
                @keyframes fadeIn {
                    from {
                        opacity: 0;
                    }
                    to {
                        opacity: 1;
                    }
                }
            `}</style>
        </div>
    );
};

export default EventTimeline;
