"""
Test script for the complete fertilizer recommendation pipeline.
Tests the cascaded ML architecture end-to-end.
"""

import requests
import json

def test_fertilizer_pipeline():
    """
    Test the complete cascaded ML pipeline:
    1. Crop prediction
    2. Data storage
    3. Fertilizer recommendation with reasoning
    """
    print("="*60)
    print("FERTILIZER RECOMMENDATION PIPELINE TEST")
    print("="*60)
    
    # Test data - typical sensor readings
    test_data = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20,
        "humidity": 82,
        "ph": 6.5,
        "rainfall": 202,
        "moisture": 45,
        "soil_type": "Loamy",
        "location": "Hyderabad",
        "device_id": "pi_test_01"
    }
    
    print("\nTest Input:")
    print(json.dumps(test_data, indent=2))
    
    # Make API request
    print("\nSending request to /api/predict/recommend...")
    
    try:
        response = requests.post(
            "http://localhost:5000/api/predict/recommend",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n" + "="*60)
            print("RESPONSE RECEIVED")
            print("="*60)
            
            # Display crop predictions
            print("\n📊 CROP PREDICTIONS:")
            print("-" * 60)
            for i, crop in enumerate(result.get('crops', []), 1):
                print(f"{i}. {crop['crop'].upper()}")
                print(f"   Confidence: {crop['confidence']*100:.1f}%")
            
            # Display fertilizer recommendation
            fert = result.get('fertilizer_recommendation', {})
            print("\n🌱 FERTILIZER RECOMMENDATION:")
            print("-" * 60)
            print(f"Fertilizer: {fert.get('fertilizer', 'N/A')}")
            print(f"Confidence: {fert.get('confidence', 0)*100:.1f}%")
            
            print("\n💡 REASONING:")
            for reason in fert.get('reasoning', []):
                print(f"  • {reason}")
            
            # Data storage confirmation
            print("\n💾 DATA STORAGE:")
            print(f"  Stored in database: {result.get('data_stored', False)}")
            
            print("\n" + "="*60)
            print("✓ TEST COMPLETED SUCCESSFULLY")
            print("="*60)
            
            # Check for 100% confidence
            if fert.get('confidence', 0) == 1.0:
                print("\n⚠ WARNING: Fertilizer confidence is 100% - possible overfitting")
            else:
                print(f"\n✓ Fertilizer confidence is realistic: {fert.get('confidence', 0)*100:.1f}%")
            
            return True
            
        else:
            print(f"\n✗ Request failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to server")
        print("Make sure the backend server is running:")
        print("  cd backend && python app.py")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_fertilizer_pipeline()
