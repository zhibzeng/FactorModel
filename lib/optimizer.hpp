int setStopCondition(double epsg, 
        double epsf, 
        double epsx, 
        int maxits);

int portfolioOptimizerWithoutTradingCostPenalty(int size,
        double* covMatrix,
        double* expectedReturn,
        double* currentWeight,
        double* lowerBound,
        double* upperBound,
        int lcNumber,
        double* linearCond,
        int* linearCondType,
        double* targetWeight,
        double* cost);

int portfolioOptimizerWithoutTradingCostPenalty2(int size,
        double* covMatrix,
        double* expectedReturn,
        double* currentWeight,
        double* lowerBound,
        double* upperBound,
        int lcNumber,
        double* linearCond,
        int* linearCondType,
        double* targetWeight,
        double* cost);

int portfolioOptimizerWithTradingCostPenalty(int size,
        double* covMatrix,
        double* expectedReturn,
        double* tradingCost,
        double* currentWeight,
        double* lowerBound,
        double* upperBound,
        int lcNumber,
        double* linearCond,
        int* linearCondType,
        double* targetWeight,
        double* cost);

int portfolioOptimizerWithTradingCostBudget(int size,
	double* covMatrix,
	double* expectedReturn,
	double* tradingCost,
	double* currentWeight,
	double tradingCostBuget,
	double* lowerBound,
	double* upperBound,
	int lcNumber,
	double* linearCond,
	int* linearCondType,
	double* targetWeight,
	double* cost);

int portfolioOptimizerWithTradingCostBudget2(int size,
	double* covMatrix,
	double* expectedReturn,
	double* tradingCost,
	double* currentWeight,
	double bandWidth,
	double* lowerBound,
	double* upperBound,
	int lcNumber,
	double* linearCond,
	int* linearCondType,
	double* targetWeight,
	double* cost);