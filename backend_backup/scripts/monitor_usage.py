#!/usr/bin/env python3
"""
Monitoring script to track Qdrant Cloud and Neon Serverless Postgres usage
to ensure staying within free-tier limits.
"""

import psycopg2
import requests
import time
from datetime import datetime
from qdrant_client import QdrantClient
from src.config.settings import settings
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class UsageMonitor:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.neon_connection = psycopg2.connect(settings.neon_db_url)
        
        # Free tier limits
        self.qdrant_limits = {
            "max_collection_size": 50000,
            "max_upsert_per_month": 100000
        }
        
        self.neon_limits = {
            "max_compute_time": 14400,  # 4 hours in seconds
            "max_data_transfer": 10  # 10 GB
        }
    
    def get_qdrant_usage(self):
        """
        Get current Qdrant usage metrics.
        Note: Qdrant doesn't provide direct API to check usage against tier limits.
        This is a simulation based on collection sizes and point counts.
        """
        try:
            collections = self.qdrant_client.get_collections()
            
            total_points = 0
            for collection in collections.collections:
                # Get point count for this collection
                count = self.qdrant_client.count(
                    collection_name=collection.name
                ).count
                total_points += count
            
            usage = {
                "collection_size": total_points,
                "max_collection_size": self.qdrant_limits["max_collection_size"],
                "upsert_count": total_points,  # Simplification: assume all points are upserts
                "max_upsert_per_month": self.qdrant_limits["max_upsert_per_month"],
                "percentage_used": min(100, (total_points / self.qdrant_limits["max_collection_size"]) * 100)
            }
            
            return usage
        except Exception as e:
            print(f"Error getting Qdrant usage: {e}")
            return None
    
    def get_neon_usage(self):
        """
        Get current Neon usage metrics.
        Note: Neon doesn't provide direct API to check usage against tier limits.
        This is a simulation based on database size and activity.
        """
        try:
            # Since Neon doesn't provide usage via API in a straightforward way,
            # we'll use a simulation based on what we can measure
            with self.neon_connection.cursor() as cursor:
                # Get an estimate of the database size
                cursor.execute("SELECT pg_database_size(current_database());")
                size_bytes = cursor.fetchone()[0]
                size_gb = size_bytes / (1024**3)  # Convert to GB
            
            # Simulated compute time and data transfer
            # In a real implementation, you'd track these via your application's metrics
            usage = {
                "compute_time_used": 7200,  # Simulated value in seconds
                "max_compute_time": self.neon_limits["max_compute_time"],
                "data_transfer_used": size_gb,  # Using DB size as proxy for data transfer
                "max_data_transfer": self.neon_limits["max_data_transfer"],
                "percentage_used": min(100, (size_gb / self.neon_limits["max_data_transfer"]) * 100)
            }
            
            return usage
        except Exception as e:
            print(f"Error getting Neon usage: {e}")
            return None
    
    def check_limits_and_alert(self):
        """
        Check usage against limits and send alerts if approaching limits.
        """
        qdrant_usage = self.get_qdrant_usage()
        neon_usage = self.get_neon_usage()
        
        alerts = []
        
        if qdrant_usage:
            if qdrant_usage["percentage_used"] >= 90:
                alerts.append(f"CRITICAL: Qdrant usage at {qdrant_usage['percentage_used']:.1f}% of limit")
            elif qdrant_usage["percentage_used"] >= 75:
                alerts.append(f"WARNING: Qdrant usage at {qdrant_usage['percentage_used']:.1f}% of limit")
            elif qdrant_usage["percentage_used"] >= 50:
                alerts.append(f"NOTICE: Qdrant usage at {qdrant_usage['percentage_used']:.1f}% of limit")
        
        if neon_usage:
            if neon_usage["percentage_used"] >= 90:
                alerts.append(f"CRITICAL: Neon usage at {neon_usage['percentage_used']:.1f}% of limit")
            elif neon_usage["percentage_used"] >= 75:
                alerts.append(f"WARNING: Neon usage at {neon_usage['percentage_used']:.1f}% of limit")
            elif neon_usage["percentage_used"] >= 50:
                alerts.append(f"NOTICE: Neon usage at {neon_usage['percentage_used']:.1f}% of limit")
        
        if alerts:
            self.send_alert(alerts, qdrant_usage, neon_usage)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "qdrant_usage": qdrant_usage,
            "neon_usage": neon_usage,
            "alerts": alerts
        }
    
    def send_alert(self, alerts, qdrant_usage, neon_usage):
        """
        Send alert notifications when approaching limits.
        This is a placeholder - in a real system you might use email, Slack, etc.
        """
        print("ALERTS TRIGGERED:")
        for alert in alerts:
            print(f"  - {alert}")
        
        # In a production system, you might want to:
        # - Send an email notification
        # - Post to a Slack channel
        # - Log to a monitoring system
        # - Trigger an automated scaling action
        print("\nUsage details:")
        if qdrant_usage:
            print(f"  Qdrant: {qdrant_usage['percentage_used']:.1f}% of limit")
        if neon_usage:
            print(f"  Neon: {neon_usage['percentage_used']:.1f}% of limit")
    
    def run_monitoring_cycle(self):
        """
        Run a single monitoring cycle and return the results.
        """
        print(f"[{datetime.now().isoformat()}] Running usage monitoring cycle...")
        
        results = self.check_limits_and_alert()
        
        # Save results to a log file for historical tracking
        with open("usage_monitoring_log.json", "a") as f:
            f.write(json.dumps(results) + "\n")
        
        return results
    
    def run_continuous_monitoring(self, interval_minutes=60):
        """
        Run continuous monitoring at specified intervals.
        """
        print(f"Starting continuous monitoring (checking every {interval_minutes} minutes)...")
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user.")
                break
            except Exception as e:
                print(f"Error during monitoring cycle: {e}")
                time.sleep(60)  # Wait a minute before retrying


if __name__ == "__main__":
    monitor = UsageMonitor()
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        # Run continuous monitoring
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60  # Default to 60 minutes
        monitor.run_continuous_monitoring(interval)
    else:
        # Run single monitoring cycle
        results = monitor.run_monitoring_cycle()
        print("\nMonitoring cycle completed.")
        print("Results:", json.dumps(results, indent=2))