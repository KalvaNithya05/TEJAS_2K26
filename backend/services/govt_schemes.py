import json
import os

class GovtSchemeService:
    def __init__(self, data_path='backend/data/govt_schemes.json'):
        self.data_path = data_path
        self.schemes = self._load_schemes()

    def _load_schemes(self):
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading schemes: {e}")
            return []

    def get_eligible_schemes(self, inputs):
        """
        Filter schemes based on inputs.
        inputs: dict containing details like 'damage_percentage', 'damage_type', 'soil_health'
        """
        eligible_schemes = []
        damage_pct = inputs.get('damage_percentage', 0)
        damage_type = inputs.get('damage_type', '')
        
        for scheme in self.schemes:
            criteria = scheme.get('eligibility', {})
            
            # Check Damage Criteria
            if 'min_damage_percentage' in criteria:
                if damage_pct >= criteria['min_damage_percentage']:
                     if 'types_of_damage' in criteria and damage_type in criteria['types_of_damage']:
                         eligible_schemes.append(scheme)
                         continue
            
            # Check Soil Health Criteria (simplistic check)
            if 'soil_health_condition' in criteria:
                # We assume inputs might have a flag or derived status, 
                # for now, match broadly if 'Low Nitrogen' etc is detected
                # This logic can be refined
                if inputs.get('N', 100) < 50: # Example logic
                     eligible_schemes.append(scheme)
                     continue

        # Remove duplicates based on scheme name
        seen_schemes = set()
        unique_schemes = []
        for scheme in eligible_schemes:
            name = scheme.get('scheme_name')
            if name not in seen_schemes:
                seen_schemes.add(name)
                unique_schemes.append(scheme)
                
        return unique_schemes
