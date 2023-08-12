# utils.py
import pandas as pd
from models import StoreStatus, BusinessHours, Timezone
from db import Session
from datetime import timedelta
import os

def read_store_status_from_csv(filepath):
    df = pd.read_csv(filepath)
    with Session() as session:
        for _, row in df.iterrows():
            store_status = StoreStatus(store_id=row['store_id'], timestamp_utc=row['timestamp_utc'], status=row['status'])
            session.add(store_status)

def read_business_hours_from_csv(filepath):
    df = pd.read_csv(filepath)
    with Session() as session:
        for _, row in df.iterrows():
            day_of_week = row.get('dayOfWeek', 'default_value')
            business_hours = BusinessHours(store_id=row['store_id'], day_of_week=day_of_week, start_time_local=row['start_time_local'], end_time_local=row['end_time_local'])

        
             
            session.add(business_hours)

def read_timezones_from_csv(filepath):
    df = pd.read_csv(filepath)
    with Session() as session:
        for _, row in df.iterrows():
            timezone_str = row['timezone_str'] if not pd.isnull(row['timezone_str']) else "America/Chicago"
            timezone = Timezone(store_id=row['store_id'], timezone_str=timezone_str)
            session.add(timezone)

def compute_uptime_downtime(store_id, start_time_local, end_time_local):
    with Session() as session:
        
        business_hours = session.query(BusinessHours).filter(BusinessHours.store_id == store_id).all()

       
        total_uptime = timedelta()
        total_downtime = timedelta()

        
        business_hours = sorted(business_hours, key=lambda x: x.day_of_week)

       
        for business_day in business_hours:
           
            interval_start = max(start_time_local, business_day.start_time_local)
            interval_end = min(end_time_local, business_day.end_time_local)

            
            if interval_start >= interval_end:
                continue

           
            status_observations = session.query(StoreStatus).filter(
                StoreStatus.store_id == store_id,
                StoreStatus.timestamp_utc >= interval_start,
                StoreStatus.timestamp_utc < interval_end,
               
                StoreStatus.status == 'active'   
            ).order_by(StoreStatus.timestamp_utc).all()

            
            interval_uptime = timedelta()
            interval_downtime = timedelta()
            prev_timestamp = interval_start

            for observation in status_observations:
                interval_uptime += observation.timestamp_utc - prev_timestamp
                prev_timestamp = observation.timestamp_utc

            interval_downtime = interval_end - prev_timestamp

             
            if status_observations and status_observations[-1].status == 'active':
                interval_downtime = timedelta()

            total_uptime += interval_uptime
            total_downtime += interval_downtime

         
        uptime_minutes = total_uptime.total_seconds() // 60
        downtime_hours = total_downtime.total_seconds() // 3600

        return uptime_minutes, downtime_hours

