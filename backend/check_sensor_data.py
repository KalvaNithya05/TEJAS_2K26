import requests
import json

BASE_URL = "http://localhost:5000/api"

def check_sensor_data():
    with open("test_results_sensor.txt", "w", encoding='utf-8') as f:
        f.write("Checking Sensor Data Endpoints...\n")
        
        # 1. Check Latest
        try:
            resp = requests.get(f"{BASE_URL}/sensor/latest")
            f.write(f"\n[GET] /sensor/latest: {resp.status_code}\n")
            if resp.status_code == 200:
                f.write(json.dumps(resp.json(), indent=2) + "\n")
            else:
                f.write(f"  Error: {resp.text}\n")
        except Exception as e:
            f.write(f"  Exception: {e}\n")

        # 3. Check Aggregate vs Manual Calc
        try:
            print("\n--- Verifying Averages ---")
            # Get History first
            hist_resp = requests.get(f"{BASE_URL}/sensor/history")
            if hist_resp.status_code == 200:
                history = hist_resp.json()
                print(f"History Count: {len(history)}")
                
                # Calculate manual average for Temperature as sample
                temps = [r['temperature'] for r in history if r['temperature'] is not None]
                if temps:
                    manual_avg = sum(temps) / len(temps)
                    print(f"Manual Avg Temp (from {len(temps)} records): {manual_avg:.2f}")
                    print(f"First 5 Temps: {temps[:5]}")
                else:
                    print("No temperature data in history.")
            
            # Get Aggregate
            agg_resp = requests.get(f"{BASE_URL}/sensor/aggregate?device_id=MM-POLE-001") # Explicit ID
            if agg_resp.status_code == 200:
                agg = agg_resp.json()
                print(f"Backend Avg Temp: {agg.get('temperature')}")
                
            # Get Aggregate for TS_STATION_01 just in case
            agg_ts_resp = requests.get(f"{BASE_URL}/sensor/aggregate?device_id=TS_STATION_01")
            if agg_ts_resp.status_code == 200:
                 print(f"Backend Avg Temp (TS_STATION_01): {agg_ts_resp.json().get('temperature')}")

        except Exception as e:
            f.write(f"  Exception: {e}\n")
            print(e)


if __name__ == "__main__":
    check_sensor_data()
