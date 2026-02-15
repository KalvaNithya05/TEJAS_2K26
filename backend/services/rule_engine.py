class RuleEngine:
    """
    Applies deterministic rules to override or validate ML predictions.
    """
    
    @staticmethod
    def apply_rules(inputs, ml_prediction):
        """
        inputs: dict containing 'damage_percentage', 'days_remaining', 'soil_n', 'damage_type', etc.
        ml_prediction: string (class label from ML model)
        
        Returns: strict override class or original prediction
        """
        damage_pct = inputs.get('damage_percentage', 0)
        days_rem = inputs.get('days_remaining', 0)
        soil_n = inputs.get('N', 0)
        damage_type = inputs.get('damage_type', '')
        
        # Rule 1: High Damage + Low Time -> Financial Relief (regardless of ML)
        if damage_pct > 75 and days_rem < 40:
            return "FINANCIAL_RELIEF_RECOMMENDED", "Override: Damage > 75% and insufficient time for recovery."

        # Rule 2: Soil Restoration mandatory if nutrients are critically low
        if soil_n < 30 and damage_type == "Nutrient Deficiency":
             return "SOIL_RESTORATION_REQUIRED", "Override: Critical Nitrogen deficiency detected."
             
        # Rule 3: If damage is minor and plenty of time -> Continue recovery
        if damage_pct < 30 and days_rem > 60:
             return "CONTINUE_WITH_RECOVERY_PLAN", "Override: Minor damage, sufficient time to recover."

        return ml_prediction, "ML Prediction accepted."
