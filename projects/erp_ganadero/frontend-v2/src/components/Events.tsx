import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Event } from '../types';
import Button from './Button';
import Modal from './Modal';
import EventForm from './EventForm';

const Events: React.FC = () => {
    const [events, setEvents] = useState<Event[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedCattleId] = useState('cattle-1'); // TODO: Get from context

    useEffect(() => {
        loadEvents();
    }, []);

    const loadEvents = async () => {
        try {
            setLoading(true);
            setError(null);
            // For now, load events for first cattle
            const data = await api.getEvents(selectedCattleId);
            setEvents(Array.isArray(data) ? data : []);
        } catch (error) {
            console.error('Error loading events:', error);
            setError('No se pudieron cargar los eventos. El animal puede no existir o el backend no está disponible.');
            setEvents([]); // Set empty array on error
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (eventData: any) => {
        try {
            await api.createEvent({
                cattle_id: selectedCattleId,
                ...eventData
            });
            setIsModalOpen(false);
            loadEvents();
            alert('Evento guardado exitosamente');
        } catch (error) {
            console.error('Error saving event:', error);
            alert('Error al guardar evento');
        }
    };

    const getEventTypeLabel = (type: string) => {
        const labels: Record<string, string> = {
            birth: 'Nacimiento',
            sale: 'Venta',
            vaccination: 'Vacunación',
            treatment: 'Tratamiento',
            weighing: 'Pesaje',
            death: 'Muerte'
        };
        return labels[type] || type;
    };

    const getEventIcon = (type: string) => {
        const icons: Record<string, string> = {
            birth: '🍼',
            sale: '💰',
            vaccination: '💉',
            treatment: '🏥',
            weighing: '⚖️',
            death: '💀'
        };
        return icons[type] || '📋';
    };

    if (loading) {
        return (
            <div className="container">
                <div className="loading">Cargando eventos...</div>
            </div>
        );
    }

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.75rem', margin: 0 }}>📅 Eventos</h2>
                <Button variant="primary" onClick={() => setIsModalOpen(true)}>
                    ➕ Agregar Evento
                </Button>
            </div>

            {error && (
                <div className="card" style={{
                    background: '#FFF3E0',
                    border: '2px solid var(--warning)',
                    padding: '1rem',
                    marginBottom: '1rem'
                }}>
                    <p style={{ margin: 0, color: 'var(--text-primary)' }}>
                        ⚠️ {error}
                    </p>
                    <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                        Puedes agregar eventos de todas formas. Se guardarán cuando el backend esté disponible.
                    </p>
                </div>
            )}

            {events.length === 0 && !error ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)' }}>
                        No hay eventos registrados. Agrega el primer evento.
                    </p>
                </div>
            ) : (
                <div className="card">
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {events.map((event) => (
                            <div
                                key={event.id}
                                style={{
                                    padding: '1rem',
                                    border: '2px solid var(--border)',
                                    borderRadius: 'var(--radius-md)',
                                    borderLeft: '4px solid var(--primary)',
                                    transition: 'var(--transition-normal)',
                                    cursor: 'pointer'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.borderColor = 'var(--primary)';
                                    e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.borderColor = 'var(--border)';
                                    e.currentTarget.style.boxShadow = 'none';
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                            <span style={{ fontSize: '1.5rem' }}>{getEventIcon(event.type)}</span>
                                            <span style={{ fontWeight: 600, fontSize: '1.125rem', color: 'var(--primary)' }}>
                                                {getEventTypeLabel(event.type)}
                                            </span>
                                        </div>
                                        <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                            {new Date(event.event_date).toLocaleDateString('es-MX', {
                                                year: 'numeric',
                                                month: 'long',
                                                day: 'numeric'
                                            })}
                                        </div>
                                        {event.notes && (
                                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', fontStyle: 'italic' }}>
                                                {event.notes}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title="Nuevo Evento"
            >
                <EventForm
                    cattleId={selectedCattleId}
                    onSubmit={handleSubmit}
                    onCancel={() => setIsModalOpen(false)}
                />
            </Modal>
        </div>
    );
};

export default Events;
