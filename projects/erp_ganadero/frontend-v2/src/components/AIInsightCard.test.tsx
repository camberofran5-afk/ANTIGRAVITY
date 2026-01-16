import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import AIInsightCard from './AIInsightCard';
import { TrendingUp, TrendingDown } from 'lucide-react';

// Mock specific icons to avoid issues
vi.mock('lucide-react', () => ({
    TrendingUp: () => <span data-testid="trending-up">Icon</span>,
    TrendingDown: () => <span data-testid="trending-down">Icon</span>,
    AlertTriangle: () => <span>Icon</span>,
    CheckCircle: () => <span>Icon</span>,
    Info: () => <span>Icon</span>,
    Activity: () => <span>Icon</span>,
    DollarSign: () => <span>Icon</span>,
    Users: () => <span>Icon</span>,
}));

describe('AIInsightCard', () => {
    const mockInsight = {
        insight: "El ganado está ganando peso correctamente",
        recommendation: "Mantener dieta actual",
        confidence: 85,
        alert: null,
        provider: "Gemini Pro",
        generated_at: new Date().toISOString()
    };

    it('renders title and insight content correctly', () => {
        render(
            <AIInsightCard
                title="Ganancia Diaria"
                icon="⚖️"
                insight={mockInsight}
            />
        );

        expect(screen.getByText('Ganancia Diaria')).toBeInTheDocument();
        expect(screen.getByText('El ganado está ganando peso correctamente')).toBeInTheDocument();
        expect(screen.getByText('Mantener dieta actual')).toBeInTheDocument();
    });

    it('shows high confidence badge', () => {
        render(
            <AIInsightCard
                title="Test"
                icon="🔍"
                insight={{ ...mockInsight, confidence: 95 }}
            />
        );
        expect(screen.getByText('Alta (95%)')).toBeInTheDocument();
    });

    it('shows alert when present', () => {
        render(
            <AIInsightCard
                title="Test"
                icon="⚠️"
                insight={{ ...mockInsight, alert: "Detectada posible enfermedad" }}
            />
        );
        expect(screen.getByText('Detectada posible enfermedad')).toBeInTheDocument();
    });
});
