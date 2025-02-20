import requests
import time

# Replace with your actual API Key and Endpoint ID
API_KEY = 'rpa_QMNIH2INI208G0KFX2BSTA76BCMSBQ99OLAVJHWV155x0r'  # Replace with your actual API key
ENDPOINT_ID = "5535hu45acjkvp"  # Replace with your actual endpoint ID

# API URLs
RUN_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
STATUS_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status"

# Headers
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Request Payload
payload = {
    "input": {"prompt": "Your prompt"}
}

def submit_job():
    """Submit a job to RunPod and return the job ID."""
    response = requests.post(RUN_URL, headers=HEADERS, json=payload)
    response_data = response.json()
    
    if "id" in response_data:
        job_id = response_data["id"]
        print(f"Job submitted successfully. Job ID: {job_id}")
        return job_id
    else:
        print("Failed to submit job:", response_data)
        return None

def get_job_result(job_id):
    """Poll RunPod until the job is finished and return the result."""
    while True:
        status_response = requests.get(f"{STATUS_URL}/{job_id}", headers=HEADERS)
        status_data = status_response.json()
        
        # Check job status
        job_status = status_data.get("status", "")
        print(f"Current job status: {job_status}")
        
        if job_status == "COMPLETED":
            print("Job completed successfully!")
            return status_data.get("output")  # Return final output
        elif job_status in ["FAILED", "CANCELLED"]:
            print(f"Job {job_status}.")
            return None
        
        # Wait before polling again
        time.sleep(3)  # Adjust the polling interval if needed

if __name__ == "__main__":
    job_id = submit_job()
    if job_id:
        result = get_job_result(job_id)
        print("Final Result:", result)
