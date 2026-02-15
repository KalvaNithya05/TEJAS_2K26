from ml.recovery_model import RecoveryDecisionModel
from services.rule_engine import RuleEngine
from services.eco_advisory import EcoAdvisoryService
from services.govt_schemes import GovtSchemeService
from services.llm_advisor import LLMAdvisor

class RecoveryManager:
    def __init__(self):
        self.ml_model = RecoveryDecisionModel()
        self.rule_engine = RuleEngine()
        self.eco_service = EcoAdvisoryService()
        self.scheme_service = GovtSchemeService()
        self.llm_advisor = LLMAdvisor()

    def get_recovery_plan(self, features):
        """
        Orchestrates the recovery decision workflow.
        features: dict containing all input parameters
        """
        # 1. ML Prediction
        ml_result = self.ml_model.predict(features)
        initial_decision = ml_result['prediction']
        
        # 2. Rule Engine Override
        final_decision, reason = self.rule_engine.apply_rules(features, initial_decision)
        
        # 3. Eco Advisory
        eco_tips = self.eco_service.generate_advisory(features)
        
        # 4. Government Schemes
        # We need to pass more comprehensive data for schemes if available, 
        # for now using features which contains 'damage_percentage' etc.
        schemes = self.scheme_service.get_eligible_schemes(features)
        
        # Construct intermediate result
        recovery_plan = {
            "decision": final_decision,
            "confidence": ml_result['confidence'],
            "reason": reason,
            "ml_analysis": ml_result, # detailed ML output
            "eco_advisory": eco_tips,
            "schemes": schemes
        }
        
        # 5. LLM Explanation
        llm_explanation = self.llm_advisor.generate_explanation(recovery_plan)
        recovery_plan['llm_explanation'] = llm_explanation
        
        return recovery_plan
