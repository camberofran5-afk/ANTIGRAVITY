import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import type { Animal, Event, InventoryItem, Client, Cost } from '../types';

// Extend jsPDF type to include autoTable
declare module 'jspdf' {
    interface jsPDF {
        autoTable: typeof autoTable;
    }
}

interface DateRange {
    start: string;
    end: string;
}

// Helper function to format currency
const formatCurrency = (amount: number): string => {
    return `$${amount.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
};

// Helper function to format date
const formatDate = (date: string): string => {
    return new Date(date).toLocaleDateString('es-MX', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

// Add header and footer to PDF
const addHeaderFooter = (doc: jsPDF, title: string, pageNumber: number = 1) => {
    // Header
    doc.setFontSize(20);
    doc.setTextColor(33, 150, 243); // Blue
    doc.text('ERP Ganadero', 14, 20);

    doc.setFontSize(14);
    doc.setTextColor(0, 0, 0);
    doc.text(title, 14, 30);

    doc.setFontSize(10);
    doc.setTextColor(128, 128, 128);
    doc.text(`Generado: ${formatDate(new Date().toISOString())}`, 14, 37);

    // Footer
    const pageHeight = doc.internal.pageSize.height;
    doc.setFontSize(8);
    doc.setTextColor(128, 128, 128);
    doc.text(`Página ${pageNumber}`, 14, pageHeight - 10);
};

// Generate Inventory Report
export const generateInventoryReport = (
    items: InventoryItem[]
): void => {
    const doc = new jsPDF();

    addHeaderFooter(doc, 'Reporte de Inventario', 1);

    // Summary section
    const totalValue = items.reduce((sum, item) => sum + item.total_value, 0);
    const lowStockItems = items.filter(item =>
        item.min_stock && item.quantity <= item.min_stock
    ).length;
    const expiringItems = items.filter(item => {
        if (!item.expiry_date) return false;
        const daysUntil = Math.floor(
            (new Date(item.expiry_date).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)
        );
        return daysUntil <= 30 && daysUntil >= 0;
    }).length;

    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.text('Resumen', 14, 50);

    doc.setFontSize(10);
    doc.text(`Total de artículos: ${items.length}`, 14, 58);
    doc.text(`Valor total: ${formatCurrency(totalValue)}`, 14, 64);
    doc.text(`Artículos con stock bajo: ${lowStockItems}`, 14, 70);
    doc.text(`Artículos por vencer (30 días): ${expiringItems}`, 14, 76);

    // Items table
    const tableData = items.map(item => [
        item.name,
        item.category,
        `${item.quantity} ${item.unit}`,
        formatCurrency(item.unit_cost),
        formatCurrency(item.total_value),
        item.expiry_date ? formatDate(item.expiry_date) : 'N/A',
        item.min_stock && item.quantity <= item.min_stock ? '⚠️ Bajo' : 'OK'
    ]);

    autoTable(doc, {
        startY: 85,
        head: [['Artículo', 'Categoría', 'Cantidad', 'Costo Unit.', 'Valor Total', 'Vencimiento', 'Estado']],
        body: tableData,
        theme: 'striped',
        headStyles: { fillColor: [33, 150, 243] },
        styles: { fontSize: 9 },
        columnStyles: {
            3: { halign: 'right' },
            4: { halign: 'right' }
        }
    });

    doc.save(`inventario_${new Date().toISOString().split('T')[0]}.pdf`);
};

// Generate Sales Report
export const generateSalesReport = (
    sales: Event[],
    animals: Animal[],
    clients: Client[],
    dateRange: DateRange
): void => {
    const doc = new jsPDF();

    addHeaderFooter(doc, 'Reporte de Ventas', 1);

    // Filter sales within date range
    const filteredSales = sales.filter(sale => {
        const saleDate = new Date(sale.event_date);
        return saleDate >= new Date(dateRange.start) && saleDate <= new Date(dateRange.end);
    });

    // Calculate totals
    const totalRevenue = filteredSales.reduce((sum, sale) =>
        sum + (sale.data.total_price || 0), 0
    );
    const totalWeight = filteredSales.reduce((sum, sale) =>
        sum + (sale.data.sale_weight_kg || 0), 0
    );
    const avgPricePerKg = totalWeight > 0 ? totalRevenue / totalWeight : 0;

    // Summary section
    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.text('Resumen del Período', 14, 50);

    doc.setFontSize(10);
    doc.text(`Período: ${formatDate(dateRange.start)} - ${formatDate(dateRange.end)}`, 14, 58);
    doc.text(`Total de ventas: ${filteredSales.length}`, 14, 64);
    doc.text(`Ingresos totales: ${formatCurrency(totalRevenue)}`, 14, 70);
    doc.text(`Peso total vendido: ${totalWeight.toFixed(2)} kg`, 14, 76);
    doc.text(`Precio promedio/kg: ${formatCurrency(avgPricePerKg)}`, 14, 82);

    // Sales table
    const tableData = filteredSales.map(sale => {
        const animal = animals.find(a => a.id === sale.cattle_id);
        const client = clients.find(c => c.id === sale.data.buyer_id);

        return [
            formatDate(sale.event_date),
            animal?.arete || animal?.arete_number || 'N/A',
            client?.name || 'N/A',
            `${sale.data.sale_weight_kg || 0} kg`,
            formatCurrency(sale.data.price_per_kg || 0),
            formatCurrency(sale.data.total_price || 0),
            sale.data.payment_status === 'paid' ? '✓ Pagado' : '⏳ Pendiente'
        ];
    });

    autoTable(doc, {
        startY: 92,
        head: [['Fecha', 'Arete', 'Cliente', 'Peso', '$/kg', 'Total', 'Estado']],
        body: tableData,
        theme: 'striped',
        headStyles: { fillColor: [76, 175, 80] },
        styles: { fontSize: 9 },
        columnStyles: {
            4: { halign: 'right' },
            5: { halign: 'right' }
        }
    });

    doc.save(`ventas_${dateRange.start}_${dateRange.end}.pdf`);
};

// Generate Financial Summary Report
export const generateFinancialReport = (
    costs: Cost[],
    sales: Event[],
    dateRange: DateRange
): void => {
    const doc = new jsPDF();

    addHeaderFooter(doc, 'Resumen Financiero', 1);

    // Filter data within date range
    const filteredCosts = costs.filter(cost => {
        const costDate = new Date(cost.cost_date);
        return costDate >= new Date(dateRange.start) && costDate <= new Date(dateRange.end);
    });

    const filteredSales = sales.filter(sale => {
        const saleDate = new Date(sale.event_date);
        return saleDate >= new Date(dateRange.start) && saleDate <= new Date(dateRange.end);
    });

    // Calculate totals
    const totalCosts = filteredCosts.reduce((sum, cost) => sum + cost.amount_mxn, 0);
    const totalRevenue = filteredSales.reduce((sum, sale) => sum + (sale.data.total_price || 0), 0);
    const profit = totalRevenue - totalCosts;
    const margin = totalRevenue > 0 ? (profit / totalRevenue) * 100 : 0;

    // Summary section
    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.text('Resumen Financiero', 14, 50);

    doc.setFontSize(10);
    doc.text(`Período: ${formatDate(dateRange.start)} - ${formatDate(dateRange.end)}`, 14, 58);

    // Revenue box
    doc.setDrawColor(76, 175, 80);
    doc.setLineWidth(0.5);
    doc.rect(14, 65, 85, 20);
    doc.setFontSize(9);
    doc.setTextColor(128, 128, 128);
    doc.text('Ingresos Totales', 18, 70);
    doc.setFontSize(14);
    doc.setTextColor(76, 175, 80);
    doc.text(formatCurrency(totalRevenue), 18, 80);

    // Costs box
    doc.setDrawColor(255, 152, 0);
    doc.rect(105, 65, 85, 20);
    doc.setFontSize(9);
    doc.setTextColor(128, 128, 128);
    doc.text('Costos Totales', 109, 70);
    doc.setFontSize(14);
    doc.setTextColor(255, 152, 0);
    doc.text(formatCurrency(totalCosts), 109, 80);

    // Profit box
    const profitColor: [number, number, number] = profit >= 0 ? [76, 175, 80] : [244, 67, 54];
    doc.setDrawColor(profitColor[0], profitColor[1], profitColor[2]);
    doc.rect(14, 90, 85, 20);
    doc.setFontSize(9);
    doc.setTextColor(128, 128, 128);
    doc.text('Ganancia/Pérdida', 18, 95);
    doc.setFontSize(14);
    doc.setTextColor(profitColor[0], profitColor[1], profitColor[2]);
    doc.text(formatCurrency(profit), 18, 105);

    // Margin box
    doc.setDrawColor(33, 150, 243);
    doc.rect(105, 90, 85, 20);
    doc.setFontSize(9);
    doc.setTextColor(128, 128, 128);
    doc.text('Margen %', 109, 95);
    doc.setFontSize(14);
    doc.setTextColor(33, 150, 243);
    doc.text(`${margin.toFixed(2)}%`, 109, 105);

    // Cost breakdown by category
    const costsByCategory = filteredCosts.reduce((acc, cost) => {
        acc[cost.category] = (acc[cost.category] || 0) + cost.amount_mxn;
        return acc;
    }, {} as Record<string, number>);

    const categoryLabels: Record<string, string> = {
        feed: '🌾 Alimento',
        veterinary: '💊 Veterinario',
        labor: '👷 Mano de Obra',
        infrastructure: '🏗️ Infraestructura',
        other: '📦 Otros'
    };

    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.text('Desglose de Costos', 14, 125);

    const categoryData = Object.entries(costsByCategory).map(([category, amount]) => [
        categoryLabels[category] || category,
        formatCurrency(amount),
        `${((amount / totalCosts) * 100).toFixed(1)}%`
    ]);

    autoTable(doc, {
        startY: 130,
        head: [['Categoría', 'Monto', '% del Total']],
        body: categoryData,
        theme: 'striped',
        headStyles: { fillColor: [33, 150, 243] },
        styles: { fontSize: 10 },
        columnStyles: {
            1: { halign: 'right' },
            2: { halign: 'right' }
        }
    });

    doc.save(`financiero_${dateRange.start}_${dateRange.end}.pdf`);
};

// Generate KPI Dashboard Report
export const generateKPIReport = (
    animals: Animal[],
    events: Event[],
    dateRange: DateRange
): void => {
    const doc = new jsPDF();

    addHeaderFooter(doc, 'Dashboard de KPIs', 1);

    // Calculate KPIs
    const activeAnimals = animals.filter(a => a.status === 'active').length;
    const totalAnimals = animals.length;

    const births = events.filter(e =>
        e.type === 'birth' &&
        new Date(e.event_date) >= new Date(dateRange.start) &&
        new Date(e.event_date) <= new Date(dateRange.end)
    );

    const deaths = events.filter(e =>
        e.type === 'death' &&
        new Date(e.event_date) >= new Date(dateRange.start) &&
        new Date(e.event_date) <= new Date(dateRange.end)
    );

    const sales = events.filter(e =>
        e.type === 'sale' &&
        new Date(e.event_date) >= new Date(dateRange.start) &&
        new Date(e.event_date) <= new Date(dateRange.end)
    );

    const mortalityRate = totalAnimals > 0 ? (deaths.length / totalAnimals) * 100 : 0;

    const avgWeight = animals
        .filter(a => a.weight_kg)
        .reduce((sum, a) => sum + (a.weight_kg || 0), 0) /
        animals.filter(a => a.weight_kg).length || 0;

    // KPIs section
    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.text(`KPIs del Período: ${formatDate(dateRange.start)} - ${formatDate(dateRange.end)}`, 14, 50);

    // KPI boxes
    const kpis = [
        { label: 'Animales Activos', value: `${activeAnimals}`, color: [33, 150, 243], y: 60 },
        { label: 'Total de Animales', value: `${totalAnimals}`, color: [156, 39, 176], y: 60 },
        { label: 'Nacimientos', value: `${births.length}`, color: [76, 175, 80], y: 85 },
        { label: 'Muertes', value: `${deaths.length}`, color: [244, 67, 54], y: 85 },
        { label: 'Ventas', value: `${sales.length}`, color: [255, 152, 0], y: 110 },
        { label: 'Tasa Mortalidad', value: `${mortalityRate.toFixed(2)}%`, color: [244, 67, 54], y: 110 },
    ];

    kpis.forEach((kpi, index) => {
        const x = index % 2 === 0 ? 14 : 105;
        const color = kpi.color as [number, number, number];
        doc.setDrawColor(color[0], color[1], color[2]);
        doc.setLineWidth(0.5);
        doc.rect(x, kpi.y, 85, 20);
        doc.setFontSize(9);
        doc.setTextColor(128, 128, 128);
        doc.text(kpi.label, x + 4, kpi.y + 5);
        doc.setFontSize(14);
        doc.setTextColor(color[0], color[1], color[2]);
        doc.text(kpi.value, x + 4, kpi.y + 15);
    });

    // Additional metrics table
    const metricsData = [
        ['Peso Promedio', `${avgWeight.toFixed(2)} kg`],
        ['Animales Vendidos', `${sales.length}`],
        ['Tasa de Natalidad', `${totalAnimals > 0 ? ((births.length / totalAnimals) * 100).toFixed(2) : 0}%`],
        ['Eventos Registrados', `${events.length}`]
    ];

    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.text('Métricas Adicionales', 14, 145);

    autoTable(doc, {
        startY: 150,
        head: [['Métrica', 'Valor']],
        body: metricsData,
        theme: 'striped',
        headStyles: { fillColor: [33, 150, 243] },
        styles: { fontSize: 10 },
        columnStyles: {
            1: { halign: 'right', fontStyle: 'bold' }
        }
    });

    doc.save(`kpis_${dateRange.start}_${dateRange.end}.pdf`);
};
