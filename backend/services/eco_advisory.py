class EcoAdvisoryService:
    @staticmethod
    def generate_advisory(inputs):
        """
        Generates eco-friendly advice based on soil and damage conditions.
        """
        advisory = []
        
        soil_n = inputs.get('N', 0)
        soil_p = inputs.get('P', 0)
        damage_type = inputs.get('damage_type', '')
        moisture = inputs.get('moisture', 0)
        
        # Nitrogen Management
        if soil_n < 50:
            advisory.append({
                "issue": "Low Nitrogen",
                "solution": "Use compost or vermicompost.",
                "type": "Organic Fertilizer"
            })
            advisory.append({
                "issue": "Nitrogen Deficiency",
                "solution": "Plant leguminous crops (beans, peas) for natural N-fixation.",
                "type": "Crop Rotation"
            })
            
        # Pest Management
        if damage_type == "Pest Attack":
             advisory.append({
                "issue": "Pest Attack",
                "solution": "Spray Neem Oil solution (5ml/liter water).",
                "type": "Natural Pesticide"
            })
             advisory.append({
                "issue": "Pest Control",
                "solution": "Introduce beneficial insects like Ladybugs.",
                "type": "Biological Control"
            })
            
        # Water Management
        if moisture > 80:
             advisory.append({
                "issue": "High Moisture/Waterlogging",
                "solution": "Improve drainage by digging channels.",
                "type": "Water Management"
            })
            
        return advisory
