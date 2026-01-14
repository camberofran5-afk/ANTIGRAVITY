// Financial Calculations

export const calculations = {
    // Cost per Kg Produced
    costPerKg(totalCosts: number, weightGain: number): number {
        if (weightGain <= 0) return 0;
        return totalCosts / weightGain;
    },

    // Profit per Animal
    profit(revenue: number, totalCosts: number): number {
        return revenue - totalCosts;
    },

    // Margin %
    marginPercent(profit: number, revenue: number): number {
        if (revenue <= 0) return 0;
        return (profit / revenue) * 100;
    },

    // Unproductive Cow Cost (MVP Feature)
    unproductiveCost(count: number) {
        const weeklyMaintenance = 15.42; // USD
        return {
            weekly: count * weeklyMaintenance,
            monthly: count * weeklyMaintenance * 4.33,
            annual: count * weeklyMaintenance * 52
        };
    },

    // Economic Opportunity (MVP Feature)
    economicOpportunity(currentRate: number, targetRate: number, herdSize: number): number {
        const gap = targetRate - currentRate;
        const missingCalves = (gap / 100) * herdSize;
        const revenuePerCalf = 550; // USD
        return missingCalves * revenuePerCalf;
    },

    // Break-Even Price
    breakEvenPrice(totalCosts: number, finalWeight: number): number {
        if (finalWeight <= 0) return 0;
        return totalCosts / finalWeight;
    },

    // ROI per Animal
    roiPercent(salePrice: number, totalCosts: number): number {
        if (totalCosts <= 0) return 0;
        return ((salePrice - totalCosts) / totalCosts) * 100;
    },

    // Total Price from Weight and Price/Kg
    totalPrice(weight: number, pricePerKg: number): number {
        return weight * pricePerKg;
    },

    // Unit Cost from Total and Quantity
    unitCost(total: number, quantity: number): number {
        if (quantity <= 0) return 0;
        return total / quantity;
    }
};
