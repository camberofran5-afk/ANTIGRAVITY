import React, { useState } from 'react';
import { Worker } from '../types';
import Button from './Button';
import Modal from './Modal';
import Input from './Input';
import Select from './Select';

const Workers: React.FC = () => {
    const [workers, _setWorkers] = useState<Worker[]>([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const [formData, setFormData] = useState({
        name: '',
        role: '' as 'vaquero' | 'veterinario' | 'manager' | '',
        salary_monthly: 0,
        hire_date: new Date().toISOString().split('T')[0]
    });

    const resetForm = () => {
        setFormData({
            name: '',
            role: '',
            salary_monthly: 0,
            hire_date: new Date().toISOString().split('T')[0]
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/v1/workers', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ranch_id: 'ranch-1', ...formData })
            });
            if (response.ok) {
                alert('Trabajador agregado exitosamente');
                setIsModalOpen(false);
                resetForm();
            }
        } catch (err) {
            alert('Error al agregar trabajador');
        }
    };

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.75rem', margin: 0 }}>👷 Trabajadores</h2>
                <Button variant="primary" onClick={() => { resetForm(); setIsModalOpen(true); }}>
                    ➕ Agregar Trabajador
                </Button>
            </div>

            {workers.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)' }}>
                        No hay trabajadores registrados. Agrega el primer trabajador.
                    </p>
                </div>
            ) : (
                <div style={{ display: 'grid', gap: '1rem' }}>
                    {workers.map((worker) => (
                        <div key={worker.id} className="card">
                            <h3>{worker.name}</h3>
                        </div>
                    ))}
                </div>
            )}

            <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); resetForm(); }} title="Nuevo Trabajador">
                <form onSubmit={handleSubmit}>
                    <Input
                        label="Nombre"
                        value={formData.name}
                        onChange={(val) => setFormData({ ...formData, name: val as string })}
                        required
                    />
                    <Select
                        label="Rol"
                        value={formData.role}
                        onChange={(val) => setFormData({ ...formData, role: val as any })}
                        options={[
                            { value: 'vaquero', label: 'Vaquero' },
                            { value: 'veterinario', label: 'Veterinario' },
                            { value: 'manager', label: 'Gerente' }
                        ]}
                        required
                    />
                    <Input
                        type="number"
                        label="Salario Mensual (MXN)"
                        value={formData.salary_monthly}
                        onChange={(val) => setFormData({ ...formData, salary_monthly: val as number })}
                        min={0}
                        step={0.01}
                        required
                    />
                    <Input
                        type="date"
                        label="Fecha de Contratación"
                        value={formData.hire_date}
                        onChange={(val) => setFormData({ ...formData, hire_date: val as string })}
                        required
                    />
                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.5rem' }}>
                        <Button variant="secondary" onClick={() => { setIsModalOpen(false); resetForm(); }} type="button" fullWidth>
                            Cancelar
                        </Button>
                        <Button variant="primary" type="submit" fullWidth>
                            Guardar
                        </Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default Workers;
