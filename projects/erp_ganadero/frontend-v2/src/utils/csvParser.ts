/**
 * CSV Parser Utilities
 * 
 * Parse and validate CSV files
 */

import Papa from 'papaparse';

export interface CSVParseResult {
    data: any[];
    headers: string[];
    errors: string[];
}

/**
 * Parse CSV file
 */
export const parseCSV = (file: File): Promise<CSVParseResult> => {
    return new Promise((resolve, reject) => {
        Papa.parse(file, {
            header: true,
            skipEmptyLines: true,
            complete: (results) => {
                const headers = results.meta.fields || [];
                const errors = results.errors.map(err => err.message);

                resolve({
                    data: results.data,
                    headers,
                    errors
                });
            },
            error: (error) => {
                reject(error);
            }
        });
    });
};

/**
 * Validate CSV data against expected columns
 */
export const validateCSVColumns = (
    headers: string[],
    requiredColumns: string[]
): { valid: boolean; missing: string[] } => {
    const missing = requiredColumns.filter(col => !headers.includes(col));
    return {
        valid: missing.length === 0,
        missing
    };
};

/**
 * Auto-detect column mapping
 */
export const autoDetectMapping = (
    csvHeaders: string[],
    targetColumns: { key: string; label: string; aliases?: string[] }[]
): Record<string, string> => {
    const mapping: Record<string, string> = {};

    targetColumns.forEach(target => {
        // Try exact match first
        const exactMatch = csvHeaders.find(h =>
            h.toLowerCase() === target.label.toLowerCase()
        );

        if (exactMatch) {
            mapping[target.key] = exactMatch;
            return;
        }

        // Try aliases
        if (target.aliases) {
            const aliasMatch = csvHeaders.find(h =>
                target.aliases!.some(alias =>
                    h.toLowerCase().includes(alias.toLowerCase())
                )
            );

            if (aliasMatch) {
                mapping[target.key] = aliasMatch;
            }
        }
    });

    return mapping;
};

/**
 * Transform CSV data using column mapping
 */
export const transformCSVData = (
    data: any[],
    mapping: Record<string, string>
): any[] => {
    return data.map(row => {
        const transformed: any = {};
        Object.entries(mapping).forEach(([targetKey, csvColumn]) => {
            transformed[targetKey] = row[csvColumn];
        });
        return transformed;
    });
};
