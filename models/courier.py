"""
KayaKonnect - Courier Model
Branch: courier-module
"""

import random
import string
from datetime import datetime


class Courier:
    """
    Represents a KayaKonnect courier (Kaya).
    Handles job viewing, accepting, completing, and earnings.
    """

    def __init__(self, courier_id: str, name: str, email: str):
        self.courier_id = courier_id
        self.name = name
        self.email = email
        self.earnings = 0.0
        self.incentive_progress = 75  # percentage toward incentive target
        self.accepted_jobs: list[dict] = []
        self.completed_jobs: list[dict] = []

        # Seed some demo available jobs
        self._available_jobs: list[dict] = [
            {
                "id": "JOB-REQUEST-1",
                "pickup": "T & C Market, Stand 4",
                "destination": "Car Park A",
                "fare": 6000,
                "status": "available",
            },
            {
                "id": "JOB-REQUEST-2",
                "pickup": "Memo Bros Store",
                "destination": "Car Park D",
                "fare": 12000,
                "status": "available",
            },
            {
                "id": "JOB-REQUEST-3",
                "pickup": "J & J Traders",
                "destination": "Car Park C",
                "fare": 8500,
                "status": "available",
            },
        ]

    # ------------------------------------------------------------------ #
    #  Core Methods                                                        #
    # ------------------------------------------------------------------ #

    def view_available_jobs(self) -> list[dict]:
        """Return list of currently available (un-accepted) jobs."""
        return [j for j in self._available_jobs if j["status"] == "available"]

    def accept_job(self, job_id: str) -> dict | None:
        """
        Accept a job by ID.
        Returns the job dict on success, None if not found / already taken.
        """
        for job in self._available_jobs:
            if job["id"] == job_id and job["status"] == "available":
                job["status"] = "accepted"
                job["accepted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.accepted_jobs.append(job)
                return job
        return None

    def complete_job(self, job_id: str) -> dict | None:
        """
        Mark an accepted job as completed and credit earnings.
        Returns the job dict on success, None if not found.
        """
        for job in self.accepted_jobs:
            if job["id"] == job_id and job["status"] == "accepted":
                job["status"] = "completed"
                job["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.earnings += job["fare"]
                self.completed_jobs.append(job)
                self.accepted_jobs.remove(job)
                # Bump incentive progress a little
                self.incentive_progress = min(100, self.incentive_progress + 5)
                return job
        return None

    def view_earnings(self) -> dict:
        """Return an earnings summary dict."""
        return {
            "total_earnings": self.earnings,
            "jobs_completed": len(self.completed_jobs),
            "incentive_progress": self.incentive_progress,
            "currency_symbol": "₦",
        }

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def generate_id(prefix: str = "KYC") -> str:
        """Generate a random courier ID."""
        suffix = "".join(random.choices(string.digits, k=6))
        return f"{prefix}{suffix}"

    def __repr__(self) -> str:
        return f"<Courier id={self.courier_id} name={self.name}>"
