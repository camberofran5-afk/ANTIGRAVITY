/**
 * Excel Import Utilities
 * 
 * Import data from Excel (.xlsx) files
 */

import * as XLSX from 'xlsx';

export interface ExcelImportResult {
    data: any[];
    headers: string[];
    sheetName: string;
}

/**
 * Read Excel file and extract data
 */
export const importFromExcel = (file: File): Promise<ExcelImportResult[]> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (e) => {
            try {
                const data = e.target?.result;
                const workbook = XLSX.read(data, { type: 'binary' });

                const results: ExcelImportResult[] = [];

                // Process each sheet
                workbook.SheetNames.forEach(sheetName => {
                    const worksheet = workbook.Sheets[sheetName];
                    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

                    if (jsonData.length > 0) {
                        const headers = jsonData[0] as string[];
                        const rows = jsonData.slice(1).map(row => {
                            const obj: any = {};
                            headers.forEach((header, index) => {
                                obj[header] = (row as any[])[index];
                            });
                            return obj;
                        });

                        results.push({
                            data: rows,
                            headers,
                            sheetName
                        });
                    }
                });

                resolve(results);
            } catch (error) {
                reject(error);
            }
        };

        reader.onerror = () => {
            reject(new Error('Failed to read Excel file'));
        };

        reader.readAsBinaryString(file);
    });
};

/**
 * Validate Excel data structure
 */
export const validateExcelData = (
    data: any[],
    requiredColumns: string[]
): { valid: boolean; missing: string[]; errors: string[] } => {
    const errors: string[] = [];
    const headers = data.length > 0 ? Object.keys(data[0]) : [];
    const missing = requiredColumns.filter(col => !headers.includes(col));

    // Check for empty data
    if (data.length === 0) {
        errors.push('El archivo no contiene datos');
    }

    // Check for missing required columns
    if (missing.length > 0) {
        errors.push(`Columnas faltantes: ${missing.join(', ')}`);
    }

    return {
        valid: errors.length === 0,
        missing,
        errors
    };
};
