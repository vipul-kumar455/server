 
 
 # main.py
from flask import Flask, jsonify, send_file
from utils import read_store_status_from_csv, read_business_hours_from_csv, read_timezones_from_csv, compute_uptime_downtime
import os
import pandas as pd


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'data', 'store_status.csv')

@app.route('/trigger_report', methods=['POST'])
def trigger_report():
     
    read_store_status_from_csv(file_path)
    read_business_hours_from_csv('data/menu_hours.csv')
    read_timezones_from_csv('data/timezones.csv')

     
    
    store_id = 1
    start_time_local = pd.to_timedelta('09:00:00')
    end_time_local = pd.to_timedelta('12:00:00')
    uptime_minutes, downtime_hours = compute_uptime_downtime(store_id, start_time_local, end_time_local)

    
    report_data = {
        'store_id': store_id,
        'uptime_last_hour': uptime_minutes,
        'downtime_last_hour': downtime_hours,
        
    }
    df_report = pd.DataFrame([report_data])
    report_filename = f"report_{store_id}.csv"
    report_filepath = os.path.join(BASE_DIR, 'reports', report_filename)
    df_report.to_csv(report_filepath, index=False)

    return jsonify({'report_id': report_filename})

@app.route('/get_report/<report_id>', methods=['GET'])
def get_report(report_id):
    
    filepath = os.path.join(BASE_DIR, 'reports', report_id)
    if not os.path.exists(filepath):
        return jsonify({'status': 'Running'})

    
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
   

