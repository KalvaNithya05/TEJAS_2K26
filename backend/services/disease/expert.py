# Expert knowledge base for plant diseases
# Mapping disease names to simple explanations, treatments, and prevention tips.

DISEASE_KNOWLEDGE_BASE = {
    "Apple_scab": {
        "explanation": "A common fungal disease causing dark, scabby spots on leaves and fruit, leading to premature leaf drop.",
        "treatment": "Apply fungicides like Captan or Myclobutanil during the growing season. Remove and destroy fallen leaves.",
        "prevention": ["Plant resistant varieties", "Prune to improve air circulation", "Rake and remove fallen leaves in autumn"]
    },
    "Apple_Black_rot": {
        "explanation": "A fungal infection that causes leaf spots, fruit rot, and cankers on branches.",
        "treatment": "Prune out infected branches and cankers. Apply fungicides like Captan or sulfur-based products.",
        "prevention": ["Remove mummified fruit from trees", "Keep trees well-pruned for airflow", "Dispose of infected wood away from the orchard"]
    },
    "Apple_Cedar_apple_rust": {
        "explanation": "A fungal disease that requires both apple trees and junipers/cedars to complete its life cycle, causing bright orange spots on leaves.",
        "treatment": "Apply fungicides like Myclobutanil when orange 'galls' appear on nearby cedars.",
        "prevention": ["Remove nearby junipers/cedars if possible", "Plant rust-resistant apple varieties", "Apply protective sprays in early spring"]
    },
    "Apple_healthy": {
        "explanation": "The apple tree leaves appear healthy and robust.",
        "treatment": "No treatment required.",
        "prevention": ["Regular monitoring", "Balanced fertilization", "Consistent watering at the base"]
    },
    "Blueberry_healthy": {
        "explanation": "The blueberry plant shows no signs of disease.",
        "treatment": "No treatment required.",
        "prevention": ["Maintain acidic soil pH (4.5-5.5)", "Mulch well to retain moisture", "Prune old wood annually"]
    },
    "Cherry_Powdery_mildew": {
        "explanation": "A fungal disease appearing as a white powdery coating on leaves, causing them to curl or distort.",
        "treatment": "Apply Neem oil or a mixture of baking soda and water (1 tsp per quart). Commercial fungicides with sulfur also work.",
        "prevention": ["Avoid overhead irrigation", "Space plants for good airflow", "Plant in full sun"]
    },
    "Cherry_healthy": {
        "explanation": "The cherry tree leaves look healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Inspect for pests regularly", "Prune in late winter", "Ensure well-draining soil"]
    },
    "Corn_Cercospora_leaf_spot_Gray_leaf_spot": {
        "explanation": "A fungal disease causing rectangular gray lesions on corn leaves, which can reduce yield significantly.",
        "treatment": "Apply fungicides if lesions appear on the EAR leaf. Rotate with non-host crops like soybeans.",
        "prevention": ["Tillage to bury infected residue", "Use resistant hybrids", "Ensure proper plant spacing"]
    },
    "Corn_Common_rust": {
        "explanation": "Fungal disease causing reddish-brown pustules on both sides of the leaves.",
        "treatment": "Rarely requires treatment unless severe. Foliar fungicides can be used if caught early.",
        "prevention": ["Plant resistant corn hybrids", "Early planting to avoid peak rust season"]
    },
    "Corn_Northern_Leaf_Blight": {
        "explanation": "Causes large, cigar-shaped grayish-green lesions on leaves.",
        "treatment": "Foliar fungicides are effective if applied at the first sign of symptoms.",
        "prevention": ["Crop rotation (2 years away from corn)", "Clean tillage", "Resistant hybrids"]
    },
    "Corn_healthy": {
        "explanation": "The corn plant is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Soil testing for nutrients", "Adequate nitrogen fertilization", "Weed control"]
    },
    "Grape_Black_rot": {
        "explanation": "A serious fungal disease that attacks leaves and turns grapes into hard, black 'mummies'.",
        "treatment": "Apply fungicides containing Mancozeb or Myclobutanil. Remove all 'mummified' fruit.",
        "prevention": ["Full sun exposure", "Excellent air circulation through pruning", "Sanitation of old vines"]
    },
    "Grape_Esca_(Black_Measles)": {
        "explanation": "A complex disease involving several fungi that affects the wood and leaves, causing tiger-stripe patterns.",
        "treatment": "No direct chemical cure. Prune out infected wood and seal wounds with pruning paint.",
        "prevention": ["Avoid pruning during wet weather", "Disinfect pruning tools", "Remove dead vines"]
    },
    "Grape_Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "explanation": "Fungal disease causing irregular brown spots on leaves, leading to drying and dropping.",
        "treatment": "Apply copper-based fungicides or Mancozeb.",
        "prevention": ["Remove infected leaves from the ground", "Avoid dense leaf canopies", "Water at the roots"]
    },
    "Grape_healthy": {
        "explanation": "The grape vine is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Keep vines off the ground", "Annual dormant pruning", "Consistent moisture"]
    },
    "Orange_Haunglongbing_(Citrus_greening)": {
        "explanation": "A devastating bacterial disease spread by insects (psyllids). Leaves turn yellow and fruit stays sour and green.",
        "treatment": "No current cure for the tree. Remove and destroy infected trees to prevent spread to others.",
        "prevention": ["Control Asian Citrus Psyllid insects", "Use certified disease-free nursery stock", "Regular inspections"]
    },
    "Peach_Bacterial_spot": {
        "explanation": "Bacterial infection causing small 'shot-holes' in leaves and spots on fruit.",
        "treatment": "Apply copper-based sprays during the dormant season and early spring.",
        "prevention": ["Avoid high-nitrogen fertilizers which encourage soft growth", "Plant resistant varieties", "Improve air drainage"]
    },
    "Peach_healthy": {
        "explanation": "The peach tree is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Thin fruit to prevent branch breakage", "Watch for peach tree borers", "Consistent mulching"]
    },
    "Pepper_bell_Bacterial_spot": {
        "explanation": "Small, water-soaked spots on leaves that turn brown and cause leaf drop.",
        "treatment": "Spray with copper-based fungicides. Avoid working in the garden when plants are wet.",
        "prevention": ["Seed treatment with bleach solution", "3-year crop rotation", "Control weeds"]
    },
    "Pepper_bell_healthy": {
        "explanation": "The bell pepper plant is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Even watering to prevent blossom end rot", "Stake plants for support", "Mulch for moisture"]
    },
    "Potato_Early_blight": {
        "explanation": "Fungal disease causing 'target-like' concentric rings on older leaves.",
        "treatment": "Apply fungicides like Chlorothalonil or Mancozeb. Ensure adequate soil fertility.",
        "prevention": ["Crop rotation", "Avoid overhead watering", "Remove potato refuse"]
    },
    "Potato_Late_blight": {
        "explanation": "A highly contagious disease (the cause of the Irish Potato Famine). Causes dark, water-soaked patches on leaves.",
        "treatment": "Immediate application of copper fungicides. Destroy infected plants immediately.",
        "prevention": ["Use certified disease-free seed potatoes", "Avoid planting near tomatoes", "Eliminate cull piles"]
    },
    "Potato_healthy": {
        "explanation": "The potato plant is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Hill potatoes to protect tubers", "Avoid excess nitrogen late in season"]
    },
    "Raspberry_healthy": {
        "explanation": "The raspberry plant is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Keep rows narrow for airflow", "Remove old canes after harvest", "Control weeds"]
    },
    "Soybean_healthy": {
        "explanation": "The soybean plant is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Balanced soil P and K", "Watch for bean leaf beetles", "No-till practices"]
    },
    "Squash_Powdery_mildew": {
        "explanation": "White, flour-like spots on leaves that can quickly cover the entire plant.",
        "treatment": "Spray with potassium bicarbonate or Neem oil. Remove heavily infected leaves.",
        "prevention": ["Provide plenty of space", "Grow in full sun", "Select resistant varieties"]
    },
    "Strawberry_Leaf_scorch": {
        "explanation": "Fungal disease causing purple-to-brown spots that merge, making leaves look 'scorched'.",
        "treatment": "Remove infected leaves. If severe, apply fungicides after harvest.",
        "prevention": ["Avoid overhead watering", "Don't over-fertilize with nitrogen in spring", "Renovate beds yearly"]
    },
    "Strawberry_healthy": {
        "explanation": "The strawberry plant is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Mulch with straw", "Control slugs and snails", "Replace plants every 3 years"]
    },
    "Tomato_Bacterial_spot": {
        "explanation": "Bacterial infection causing small, dark, raised spots on leaves and stems.",
        "treatment": "Use copper-based sprays. Remove infected debris immediately.",
        "prevention": ["Rotate crops", "Use drip irrigation", "Avoid handling wet plants"]
    },
    "Tomato_Early_blight": {
        "explanation": "Causes brown spots with concentric rings, usually starts on lower leaves.",
        "treatment": "Copper or sulfur fungicides. Prune lower leaves to prevent soil splash.",
        "prevention": ["Mulch around base", "Wide spacing for air", "Rotate with non-nightshade crops"]
    },
    "Tomato_Late_blight": {
        "explanation": "Rapidly spreading disease that can kill plants in days. Dark patches on leaves and stems.",
        "treatment": "Copper fungicides are the only option, but often ineffective if it spreads. Remove plants.",
        "prevention": ["Keep foliage dry", "Monitor weather (cool/wet favors blight)", "Do not compost infected plants"]
    },
    "Tomato_Leaf_Mold": {
        "explanation": "Fungal disease common in greenhouses. Olive-green mold appears on the underside of leaves.",
        "treatment": "Increase ventilation and reduce humidity. Fungicides containing chlorothalonil can help.",
        "prevention": ["Space plants well", "Avoid wetting leaves", "Prune for airflow"]
    },
    "Tomato_Septoria_leaf_spot": {
        "explanation": "Small circular spots with gray centers and dark borders. Causes heavy leaf drop.",
        "treatment": "Remove infected leaves. Apply copper or chlorothalonil fungicides.",
        "prevention": ["Mulch base of plants", "Clean up all garden debris in fall", "Avoid overhead watering"]
    },
    "Tomato_Spider_mites_Two-spotted_spider_mite": {
        "explanation": "Tiny pests that suck plant juices, causing yellow stippling on leaves and fine webbing.",
        "treatment": "Blast with water to dislodge mites. Use Neem oil or insecticidal soap.",
        "prevention": ["Maintain high humidity if possible", "Do not over-fertilize", "Encourage ladybugs"]
    },
    "Tomato_Target_Spot": {
        "explanation": "Fungal disease causing spots with a 'target' appearance of concentric rings.",
        "treatment": "Apply fungicides like Mancozeb or Chlorothalonil.",
        "prevention": ["Improve air circulation", "Avoid overhead irrigation", "Remove bottom-most leaves"]
    },
    "Tomato_Yellow_Leaf_Curl_Virus": {
        "explanation": "Viral disease spread by whiteflies. Leaves curl upwards and turn yellow; growth is stunted.",
        "treatment": "No cure for the virus. Remove infected plants immediately. Focus on whitefly control.",
        "prevention": ["Control whiteflies with sticky traps or Neem oil", "Use reflective mulches", "Plant resistant varieties"]
    },
    "Tomato_mosaic_virus": {
        "explanation": "Causes mottled green and yellow patterns on leaves and distorted growth.",
        "treatment": "No cure. Remove and destroy infected plants. Disinfect tools after use.",
        "prevention": ["Do not smoke near plants (virus is in tobacco)", "Buy certified virus-free seeds", "Wash hands after touching weeds"]
    },
    "Tomato_healthy": {
        "explanation": "The tomato plant is healthy.",
        "treatment": "No treatment required.",
        "prevention": ["Consistent watering", "Well-drained soil", "Regular pruning of suckers"]
    }
}

def get_disease_info(disease_name):
    """
    Returns explanation, treatment, and prevention tips for a given disease name.
    If disease name contains 'healthy', it handles it as a healthy case.
    """
    # Normalize name for lookup: 
    # 1. Replace double/triple underscores with single
    # 2. Remove parentheses if present (common in folder names)
    import re
    norm_name = re.sub(r'_{2,}', '_', disease_name)
    norm_name = norm_name.replace('(', '').replace(')', '')
    
    # Try exact match first on normalized name
    info = DISEASE_KNOWLEDGE_BASE.get(norm_name)
    
    if not info:
        # Try a partial match if normalization wasn't enough
        # Check if internal keys are in the input
        for key in DISEASE_KNOWLEDGE_BASE:
            if key in norm_name or key.replace('_', ' ') in norm_name.replace('_', ' '):
                return DISEASE_KNOWLEDGE_BASE[key]

        # Fallback for dynamic/unknown
        if 'healthy' in disease_name.lower():
            return {
                "explanation": "The plant appears to be healthy based on the visual assessment.",
                "treatment": "No treatment required.",
                "prevention": ["Regular monitoring for early detection", "Ensure proper soil nutrition", "Maintain appropriate watering schedule"]
            }
        else:
            return {
                "explanation": "A potential issue has been detected but specific details are limited.",
                "treatment": "Consult a local agricultural expert for a detailed diagnosis and treatment plan.",
                "prevention": ["Isolate affected plants if possible", "Improve overall garden sanitation", "Avoid transferring soil or water from infected areas"]
            }
            
    return info
