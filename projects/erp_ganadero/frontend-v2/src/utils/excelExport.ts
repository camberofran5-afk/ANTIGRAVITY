/**
 * Excel Export Utilities
 * 
 * Export data to Excel (.xlsx) format
 */

import * as XLSX from 'xlsx';

/**
 * Export data to Excel file
 */
export const exportToExcel = (
    data: any[],
    filename: string,
    sheetName: string = 'Sheet1'
) => {
    // Create worksheet
    const worksheet = XLSX.utils.json_to_sheet(data);

    // Create workbook
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);

    // Generate Excel file
    XLSX.writeFile(workbook, `${filename}.xlsx`);
};

/**
 * Export cattle data to Excel
 */
export const exportCattleToExcel = (cattle: any[]) => {
    const data = cattle.map(animal => ({
        'Arete': animal.arete_number,
        'Especie': animal.species,
        'Género': animal.gender,
        'Fecha Nacimiento': animal.birth_date,
        'Peso (kg)': animal.weight_kg,
        'Estado': animal.status,
        'Notas': animal.notes || ''
    }));

    exportToExcel(data, 'ganado', 'Ganado');
};

/**
 * Export costs to Excel
 */
export const exportCostsToExcel = (costs: any[]) => {
    const data = costs.map(cost => ({
        'Fecha': cost.cost_date,
        'Categoría': cost.category,
        'Monto (MXN)': cost.amount_mxn,
        'Descripción': cost.description || '',
        'Ganado ID': cost.cattle_id || ''
    }));

    exportToExcel(data, 'costos', 'Costos');
};

/**
 * Export inventory to Excel
 */
export const exportInventoryToExcel = (items: any[]) => {
    const data = items.map(item => ({
        'Categoría': item.category,
        'Nombre': item.name,
        'Cantidad': item.quantity,
        'Unidad': item.unit,
        'Costo Unitario': item.unit_cost || '',
        'Stock Mínimo': item.min_stock || '',
        'Proveedor': item.supplier || ''
    }));

    exportToExcel(data, 'inventario', 'Inventario');
};

/**
 * Export clients to Excel
 */
export const exportClientsToExcel = (clients: any[]) => {
    const data = clients.map(client => ({
        'Nombre': client.name,
        'Tipo': client.type || '',
        'Contacto': client.contact_name || '',
        'Teléfono': client.phone || '',
        'Email': client.email || '',
        'Dirección': client.address || ''
    }));

    exportToExcel(data, 'clientes', 'Clientes');
};

/**
 * Export workers to Excel
 */
export const exportWorkersToExcel = (workers: any[]) => {
    const data = workers.map(worker => ({
        'Nombre': worker.full_name,
        'Puesto': worker.position || '',
        'Teléfono': worker.phone || '',
        'Email': worker.email || '',
        'Salario (MXN)': worker.salary_mxn || '',
        'Fecha Contratación': worker.hire_date || '',
        'Activo': worker.is_active ? 'Sí' : 'No'
    }));

    exportToExcel(data, 'trabajadores', 'Trabajadores');
};
