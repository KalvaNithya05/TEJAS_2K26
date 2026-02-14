import time
from datetime import datetime, timezone

from services.thingspeak_service import (
    fetch_latest_thingspeak_data,
    store_in_supabase,
    get_last_supabase_timestamp
)


def run_thingspeak_ingestion():
    print("📡 ThingSpeak ingestion started")

    while True:
        try:
            # 1️⃣ Fetch latest data from ThingSpeak
            feed = fetch_latest_thingspeak_data()

            if not feed:
                print("⚠️ No data from ThingSpeak")
                time.sleep(60)
                continue

            # 2️⃣ Parse ThingSpeak timestamp (UTC)
            ts_created_at = feed.get("created_at")
            if ts_created_at:
                ts_dt = datetime.fromisoformat(
                    ts_created_at.replace("Z", "+00:00")
                )

                # 3️⃣ Get last timestamp from Supabase
                last_db_ts = get_last_supabase_timestamp()

                if last_db_ts:
                    db_dt = datetime.fromisoformat(
                        last_db_ts.replace("Z", "+00:00")
                    )

                    # 4️⃣ Prevent duplicate inserts
                    if ts_dt <= db_dt:
                        print(f"⏸️ No new data (Last TS: {ts_dt}, Last DB: {db_dt})")
                        time.sleep(60)
                        continue

            # 5️⃣ Insert new data
            store_in_supabase(feed)
            print("✅ New data inserted into Supabase")

        except Exception as e:
            print(f"❌ Ingestion error: {e}")

        # 6️⃣ Poll every 60 seconds
        time.sleep(60)
