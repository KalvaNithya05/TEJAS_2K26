
TRANSLATIONS = {
    'hi': {
        'rice': 'चावल',
        'maize': 'मक्का',
        'cotton': 'कपास',
        'chickpea': 'चना',
        'kidneybeans': 'राजमा',
        'pigeonpeas': 'अरहर',
        'mothbeans': 'मोठ बीन',
        'mungbean': 'मूंग',
        'blackgram': 'उड़द',
        'lentil': 'मसूर',
        'pomegranate': 'अनार',
        'banana': 'केला',
        'mango': 'आम',
        'grapes': 'अंगूर',
        'watermelon': 'तरबूज',
        'muskmelon': 'खरबूजा',
        'apple': 'सेब',
        'orange': 'संतरा',
        'papaya': 'पपीता',
        'coconut': 'नारियल',
        'jute': 'जूट',
        'coffee': 'कॉफी',
        'chili': 'मिर्च',
        'pulses': 'दालें',
        'predicted_crop': 'अनुमानित फसल',
        'confidence_score': 'विश्वास स्कोर',
        'fertilizer': 'उर्वरक',
        'yield': 'उपज',
        'recommendation': 'सिफारिश'
    },
    'te': {
        'rice': 'वరి',
        'maize': 'మొక్కజొన్న',
        'cotton': 'పత్తి',
        'chickpea': 'శనగలు',
        'kidneybeans': 'రాజ్మా',
        'pigeonpeas': 'కంది',
        'mothbeans': 'అలసందలు', # Approx
        'mungbean': 'పెసలు',
        'blackgram': 'మినుములు',
        'lentil': 'ఎర్ర కంది',
        'pomegranate': 'దానిమ్మ',
        'banana': 'అరటి',
        'mango': 'మామిడి',
        'grapes': 'ద్రాక్ష',
        'watermelon': 'పుచ్చకాయ',
        'muskmelon': 'కర్బూజా',
        'apple': 'యాపిల్',
        'orange': 'నారింజ',
        'papaya': 'బొప్పాయి',
        'coconut': 'కొబ్బరి',
        'jute': 'జనుము',
        'coffee': 'కాఫీ',
        'chili': 'మిరప',
        'pulses': 'పప్పుధాన్యాలు',
        'predicted_crop': 'అంచనా వేసిన పంట',
        'confidence_score': 'నమ్మక స్కోరు',
        'fertilizer': 'ఎరువులు',
        'yield': 'దిగుబడి',
        'recommendation': 'సిఫార్సు'
    },
    'ta': {
        'rice': 'அரிசி',
        'maize': 'சோளம்',
        'cotton': 'பருத்தி',
        # Add more as needed
    },
    'ml': {
        'rice': 'അരി',
        'maize': 'ചോളം',
        # Add more as needed
    }
}

def translate_text(text, lang='en'):
    if lang == 'en':
        return text
    
    text_lower = str(text).lower()
    if lang in TRANSLATIONS and text_lower in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][text_lower]
    
    return text

def translate_response(response_dict, lang='en'):
    """
    Recursively translate keys and values in a dictionary.
    Focus on specific keys like 'crop', 'fertilizer', 'yield'.
    """
    if lang == 'en':
        return response_dict
        
    return response_dict # Placeholder for complex dict translation if needed
    # For now, we will use translate_text explicitly in predictors
