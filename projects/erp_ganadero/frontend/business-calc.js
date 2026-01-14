// Business Calculations Module
// All financial formulas for ERP Ganadero V2

const BusinessCalc = {
    // Cost per Kg Produced
    costPerKg(totalCosts, weightGain) {
        if (weightGain <= 0) return 0;
        return totalCosts / weightGain;
    },

    // Profit per Animal
    profit(revenue, totalCosts) {
        return revenue - totalCosts;
    },

    // Margin %
    marginPercent(profit, revenue) {
        if (revenue <= 0) return 0;
        return (profit / revenue) * 100;
    },

    // Unproductive Cow Cost (MVP Feature)
    unproductiveCost(count) {
        const weeklyMaintenance = 15.42; // USD
        return {
            weekly: count * weeklyMaintenance,
            monthly: count * weeklyMaintenance * 4.33,
            annual: count * weeklyMaintenance * 52
        };
    },

    // Economic Opportunity (MVP Feature)
    economicOpportunity(currentRate, targetRate, herdSize) {
        const gap = targetRate - currentRate;
        const missingCalves = (gap / 100) * herdSize;
        const revenuePerCalf = 550; // USD
        return missingCalves * revenuePerCalf;
    },

    // Break-Even Price
    breakEvenPrice(totalCosts, finalWeight) {
        if (finalWeight <= 0) return 0;
        return totalCosts / finalWeight;
    },

    // ROI per Animal
    roiPercent(salePrice, totalCosts) {
        if (totalCosts <= 0) return 0;
        return ((salePrice - totalCosts) / totalCosts) * 100;
    },

    // Total Price from Weight and Price/Kg
    totalPrice(weight, pricePerKg) {
        return weight * pricePerKg;
    },

    // Unit Cost from Total and Quantity
    unitCost(total, quantity) {
        if (quantity <= 0) return 0;
        return total / quantity;
    },

    // Format currency
    formatMXN(amount) {
        return new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: 'MXN'
        }).format(amount);
    },

    formatUSD(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    // Calculate total costs for an animal
    calculateAnimalCosts(events, fixedCostsPerMonth = 500) {
        const birthDate = new Date(events.find(e => e.type === 'birth')?.event_date);
        const now = new Date();
        const ageMonths = (now - birthDate) / (1000 * 60 * 60 * 24 * 30);

        const fixedCosts = ageMonths * fixedCostsPerMonth;
        const eventCosts = events
            .filter(e => e.data.cost || e.data.treatment_cost)
            .reduce((sum, e) => sum + (e.data.cost || e.data.treatment_cost || 0), 0);

        return fixedCosts + eventCosts;
    },

    // Calculate weight gain
    weightGain(currentWeight, birthWeight) {
        return currentWeight - birthWeight;
    },

    // Calculate average daily gain (ADG)
    averageDailyGain(weightGain, ageInDays) {
        if (ageInDays <= 0) return 0;
        return weightGain / ageInDays;
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BusinessCalc;
}
