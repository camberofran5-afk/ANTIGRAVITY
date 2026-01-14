import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Animal } from '../types';
import Button from './Button';
import Modal from './Modal';
import Input from './Input';
import Select from './Select';

interface AnimalFormData {
    arete: string;
    name: string;
    species: 'vaca' | 'toro' | 'becerro' | '';
    gender: 'M' | 'F' | '';
    birth_date: string;
    weight_kg?: number;
    mother_id?: string;
    status: 'active' | 'sold' | 'dead';
}

const Animals: React.FC = () => {
    const [animals, setAnimals] = useState<Animal[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingAnimal, setEditingAnimal] = useState<Animal | null>(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterSpecies, setFilterSpecies] = useState<string>('');
    const [filterStatus, setFilterStatus] = useState<string>('');

    const RANCH_ID = 'ranch-1'; // TODO: Get from auth context

    const [formData, setFormData] = useState<AnimalFormData>({
        arete: '',
        name: '',
        species: '',
        gender: '',
        birth_date: new Date().toISOString().split('T')[0],
        weight_kg: undefined,
        mother_id: undefined,
        status: 'active'
    });

    useEffect(() => {
        loadAnimals();
    }, []);

    const loadAnimals = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await api.getAnimals(RANCH_ID);

            // Map backend response to frontend format
            const mappedAnimals = Array.isArray(data) ? data.map((animal: any) => ({
                ...animal,
                arete: animal.arete || animal.arete_number || '',
                name: animal.name || '',
                species: animal.species || 'vaca',
                gender: animal.gender || 'M',
                status: animal.status || 'active'
            })) : [];

            setAnimals(mappedAnimals);
        } catch (err) {
            console.error('Error loading animals:', err);
            setError('No se pudieron cargar los animales. Verifica que el backend esté corriendo.');
            setAnimals([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!formData.arete || !formData.species || !formData.gender) {
            alert('Por favor completa los campos requeridos');
            return;
        }

        try {
            const animalData = {
                ranch_id: RANCH_ID,
                ...formData,
                species: formData.species as 'vaca' | 'toro' | 'becerro',
                gender: formData.gender as 'M' | 'F'
            };

            if (editingAnimal) {
                await api.updateAnimal(editingAnimal.id, animalData);
                alert('Animal actualizado exitosamente');
            } else {
                await api.createAnimal(animalData);
                alert('Animal agregado exitosamente');
            }

            setIsModalOpen(false);
            resetForm();
            loadAnimals();
        } catch (err) {
            console.error('Error saving animal:', err);
            alert('Error al guardar animal');
        }
    };

    const handleEdit = (animal: Animal) => {
        setEditingAnimal(animal);
        setFormData({
            arete: animal.arete,
            name: animal.name || '',
            species: animal.species,
            gender: animal.gender,
            birth_date: animal.birth_date,
            weight_kg: animal.weight_kg,
            mother_id: animal.mother_id,
            status: animal.status
        });
        setIsModalOpen(true);
    };

    const handleDelete = async (animal: Animal) => {
        if (!confirm(`¿Estás seguro de eliminar a ${animal.arete}?`)) {
            return;
        }

        try {
            await api.deleteAnimal(animal.id);
            alert('Animal eliminado exitosamente');
            loadAnimals();
        } catch (err) {
            console.error('Error deleting animal:', err);
            alert('Error al eliminar animal');
        }
    };

    const resetForm = () => {
        setEditingAnimal(null);
        setFormData({
            arete: '',
            name: '',
            species: '',
            gender: '',
            birth_date: new Date().toISOString().split('T')[0],
            weight_kg: undefined,
            mother_id: undefined,
            status: 'active'
        });
    };

    const getSpeciesLabel = (species: string) => {
        const labels: Record<string, string> = {
            vaca: 'Vaca',
            toro: 'Toro',
            becerro: 'Becerro'
        };
        return labels[species] || species;
    };

    const getStatusLabel = (status: string) => {
        const labels: Record<string, string> = {
            active: 'Activo',
            sold: 'Vendido',
            dead: 'Muerto'
        };
        return labels[status] || status;
    };

    const getStatusColor = (status: string) => {
        const colors: Record<string, string> = {
            active: 'var(--success)',
            sold: 'var(--warning)',
            dead: 'var(--danger)'
        };
        return colors[status] || 'var(--text-secondary)';
    };

    // Filter animals
    const filteredAnimals = animals.filter(animal => {
        const matchesSearch = animal.arete.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (animal.name && animal.name.toLowerCase().includes(searchTerm.toLowerCase()));
        const matchesSpecies = !filterSpecies || animal.species === filterSpecies;
        const matchesStatus = !filterStatus || animal.status === filterStatus;
        return matchesSearch && matchesSpecies && matchesStatus;
    });

    if (loading) {
        return (
            <div className="container">
                <div className="loading">Cargando animales...</div>
            </div>
        );
    }

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.75rem', margin: 0 }}>🐄 Ganado</h2>
                <Button variant="primary" onClick={() => { resetForm(); setIsModalOpen(true); }}>
                    ➕ Agregar Animal
                </Button>
            </div>

            {error && (
                <div className="card" style={{
                    background: '#FFF3E0',
                    border: '2px solid var(--warning)',
                    padding: '1rem',
                    marginBottom: '1rem'
                }}>
                    <p style={{ margin: 0 }}>⚠️ {error}</p>
                </div>
            )}

            {/* Search and Filters */}
            <div className="card" style={{ marginBottom: '1.5rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '1rem' }}>
                    <Input
                        label="Buscar"
                        value={searchTerm}
                        onChange={(val) => setSearchTerm(val as string)}
                        placeholder="Buscar por arete o nombre..."
                    />
                    <Select
                        label="Especie"
                        value={filterSpecies}
                        onChange={setFilterSpecies}
                        options={[
                            { value: '', label: 'Todas' },
                            { value: 'vaca', label: 'Vaca' },
                            { value: 'toro', label: 'Toro' },
                            { value: 'becerro', label: 'Becerro' }
                        ]}
                    />
                    <Select
                        label="Estado"
                        value={filterStatus}
                        onChange={setFilterStatus}
                        options={[
                            { value: '', label: 'Todos' },
                            { value: 'active', label: 'Activo' },
                            { value: 'sold', label: 'Vendido' },
                            { value: 'dead', label: 'Muerto' }
                        ]}
                    />
                </div>
            </div>

            {/* Animals List */}
            {filteredAnimals.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)' }}>
                        {animals.length === 0 ? 'No hay animales registrados. Agrega el primer animal.' : 'No se encontraron animales con los filtros seleccionados.'}
                    </p>
                </div>
            ) : (
                <div style={{ display: 'grid', gap: '1rem' }}>
                    {filteredAnimals.map((animal) => (
                        <div
                            key={animal.id}
                            className="card"
                            style={{
                                padding: '1.5rem',
                                transition: 'var(--transition-normal)',
                                cursor: 'pointer'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.boxShadow = 'none';
                            }}
                        >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                <div style={{ flex: 1 }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                                        <h3 style={{ fontSize: '1.5rem', margin: 0, color: 'var(--primary)' }}>
                                            {animal.arete}
                                        </h3>
                                        <span style={{
                                            padding: '0.25rem 0.75rem',
                                            borderRadius: 'var(--radius-xl)',
                                            fontSize: '0.75rem',
                                            fontWeight: 600,
                                            background: getStatusColor(animal.status),
                                            color: 'white'
                                        }}>
                                            {getStatusLabel(animal.status)}
                                        </span>
                                    </div>
                                    {animal.name && (
                                        <div style={{ fontSize: '1.125rem', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                                            {animal.name}
                                        </div>
                                    )}
                                    <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                        <span>🐄 {getSpeciesLabel(animal.species)}</span>
                                        <span>{animal.gender === 'M' ? '♂️ Macho' : '♀️ Hembra'}</span>
                                        {animal.weight_kg && <span>⚖️ {animal.weight_kg} kg</span>}
                                        <span>📅 {new Date(animal.birth_date).toLocaleDateString('es-MX')}</span>
                                    </div>
                                </div>
                                <div style={{ display: 'flex', gap: '0.5rem' }}>
                                    <Button variant="secondary" onClick={() => handleEdit(animal)}>
                                        ✏️ Editar
                                    </Button>
                                    <Button variant="danger" onClick={() => handleDelete(animal)}>
                                        🗑️ Eliminar
                                    </Button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Add/Edit Modal */}
            <Modal
                isOpen={isModalOpen}
                onClose={() => { setIsModalOpen(false); resetForm(); }}
                title={editingAnimal ? 'Editar Animal' : 'Nuevo Animal'}
            >
                <form onSubmit={handleSubmit}>
                    <Input
                        label="Arete"
                        value={formData.arete}
                        onChange={(val) => setFormData({ ...formData, arete: val as string })}
                        placeholder="TX-001"
                        required
                    />

                    <Input
                        label="Nombre (opcional)"
                        value={formData.name}
                        onChange={(val) => setFormData({ ...formData, name: val as string })}
                        placeholder="Nombre del animal"
                    />

                    <Select
                        label="Especie"
                        value={formData.species}
                        onChange={(val) => setFormData({ ...formData, species: val as any })}
                        options={[
                            { value: 'vaca', label: 'Vaca' },
                            { value: 'toro', label: 'Toro' },
                            { value: 'becerro', label: 'Becerro' }
                        ]}
                        required
                    />

                    <Select
                        label="Género"
                        value={formData.gender}
                        onChange={(val) => setFormData({ ...formData, gender: val as any })}
                        options={[
                            { value: 'M', label: 'Macho' },
                            { value: 'F', label: 'Hembra' }
                        ]}
                        required
                    />

                    <Input
                        type="date"
                        label="Fecha de Nacimiento"
                        value={formData.birth_date}
                        onChange={(val) => setFormData({ ...formData, birth_date: val as string })}
                        required
                    />

                    <Input
                        type="number"
                        label="Peso (kg)"
                        value={formData.weight_kg || ''}
                        onChange={(val) => setFormData({ ...formData, weight_kg: val as number })}
                        min={0}
                        step={0.1}
                    />

                    <Select
                        label="Estado"
                        value={formData.status}
                        onChange={(val) => setFormData({ ...formData, status: val as any })}
                        options={[
                            { value: 'active', label: 'Activo' },
                            { value: 'sold', label: 'Vendido' },
                            { value: 'dead', label: 'Muerto' }
                        ]}
                        required
                    />

                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.5rem' }}>
                        <Button variant="secondary" onClick={() => { setIsModalOpen(false); resetForm(); }} type="button" fullWidth>
                            Cancelar
                        </Button>
                        <Button variant="primary" type="submit" fullWidth>
                            {editingAnimal ? 'Actualizar' : 'Guardar'}
                        </Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default Animals;
