
import React, { useState, useEffect } from 'react';
import { Animal, Species, Gender, Status } from '../types';

const Animals: React.FC = () => {
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [filter, setFilter] = useState<string>('all');
  const [search, setSearch] = useState('');

  useEffect(() => {
    // Mock data
    const mockAnimals: Animal[] = [
      {
        animal_id: '1',
        ranch_id: 'r1',
        arete_number: 'TX-452',
        species: Species.VACA,
        gender: Gender.F,
        birth_date: '2020-05-15',
        weight_kg: 520,
        status: Status.ACTIVE,
        lastReproductionDate: '2023-10-12',
        created_at: '2020-05-15'
      },
      {
        animal_id: '2',
        ranch_id: 'r1',
        arete_number: 'TX-789',
        species: Species.TORO,
        gender: Gender.M,
        birth_date: '2019-02-10',
        weight_kg: 840,
        status: Status.ACTIVE,
        created_at: '2019-02-10'
      },
      {
        animal_id: '3',
        ranch_id: 'r1',
        arete_number: 'BEC-102',
        species: Species.BECERRO,
        gender: Gender.F,
        birth_date: '2024-01-20',
        weight_kg: 95,
        status: Status.ACTIVE,
        created_at: '2024-01-20'
      },
    ];
    setAnimals(mockAnimals);
  }, []);

  const filtered = animals.filter(a => {
    const matchesSearch = a.arete_number.toLowerCase().includes(search.toLowerCase());
    const matchesType = filter === 'all' || a.species === filter;
    return matchesSearch && matchesType;
  });

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div>
          <h2 className="text-2xl font-bold text-[#134252]">Inventario de Animales</h2>
          <p className="text-gray-500">Mostrando {filtered.length} de {animals.length} registros</p>
        </div>
        
        <div className="flex w-full md:w-auto gap-2">
          <div className="relative flex-1 md:w-64">
            <i className="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
            <input 
              type="text" 
              placeholder="Buscar por arete..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-[#32b8c6] outline-none"
            />
          </div>
          <select 
            className="px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-[#32b8c6] outline-none"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="all">Todos</option>
            <option value={Species.VACA}>Vacas</option>
            <option value={Species.TORO}>Toros</option>
            <option value={Species.BECERRO}>Becerros</option>
            <option value={Species.VAQUILLA}>Vaquillas</option>
          </select>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b border-gray-100">
            <tr>
              <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Arete</th>
              <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Especie / Sexo</th>
              <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Peso</th>
              <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Estado</th>
              <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Últ. Evento</th>
              <th className="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest text-right">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {filtered.map((animal) => (
              <tr key={animal.animal_id} className="hover:bg-gray-50/50 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-[#fcfcf9] border border-gray-100 flex items-center justify-center text-[#136372]">
                      <i className="fa-solid fa-cow"></i>
                    </div>
                    <span className="font-bold text-[#134252]">{animal.arete_number}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex flex-col">
                    <span className="text-sm font-medium text-gray-700 capitalize">{animal.species}</span>
                    <span className="text-xs text-gray-400">{animal.gender === 'M' ? 'Macho' : 'Hembra'}</span>
                  </div>
                </td>
                <td className="px-6 py-4 font-semibold text-gray-700">{animal.weight_kg} kg</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 rounded-full bg-green-50 text-green-600 text-[10px] font-bold uppercase">
                    {animal.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {animal.lastReproductionDate ? new Date(animal.lastReproductionDate).toLocaleDateString() : '--'}
                </td>
                <td className="px-6 py-4 text-right">
                  <button className="p-2 text-gray-400 hover:text-[#32b8c6]">
                    <i className="fa-solid fa-ellipsis-vertical"></i>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Animals;
