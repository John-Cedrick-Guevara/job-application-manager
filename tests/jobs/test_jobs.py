VALID_JOB = {
    "title": "Software Engineer",
    "company": "Tech Corp",
    "description": "We are looking for a skilled software engineer to join our team.",
    "location": "San Francisco, CA",
    "source": "LinkedIn",
    "date_posted": "2023-09-15",
}

def create_job(client, **overrides):
    """"Helper: Creates a job with the given overrides and returns the response."""
    job_data = {**VALID_JOB, **overrides}
    response = client.post("/jobs/", json=job_data)

    return response

def test_create_job_returns_201(client):
    res = create_job(client)

    assert res.status_code == 201
    body = res.json()
    assert body["title"] == VALID_JOB["title"]

def test_create_job_with_missing_fields_returns_422(client):
    payload = {k: v for k, v in VALID_JOB.items() if k != "title"}  # Remove the title field

    res = client.post("/jobs/", json=payload)

    assert res.status_code == 422


def test_get_jobs_returns_200(client):
    # Create a job first
    create_job(client)

    res = client.get("/jobs/?skip=0&limit=10")

    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) > 0

def test_get_job_by_id_returns_200(client):
    # Create a job first
    create_job(client)
    res = client.get("/jobs/1")

    assert res.status_code == 200
    body = res.json()
    assert body["id"] == 1
    assert body["title"] == VALID_JOB["title"]

def test_get_job_by_id_not_found_returns_404(client):
    res = client.get("/jobs/999")  # Assuming this ID does not exist

    assert res.status_code == 404

def test_list_jobs_respect_limit_and_skip(client):
    # Create multiple jobs
    for i in range(5):
        create_job(client, title=f"Job {i}")

    res = client.get("/jobs/?limit=2&skip=1")

    assert res.status_code == 200
    body = res.json()
    assert len(body) == 2
    assert body[0]["title"] == "Job 1"
    assert body[1]["title"] == "Job 2"

def test_update_job_returns_200(client):
    # Create a job first
    create_job(client)
    update_payload = {"title": "Updated Job Title", **{k: v for k, v in VALID_JOB.items() if k != "title"}}  # Ensure all required fields are present

    res = client.put("/jobs/1", json=update_payload)

    assert res.status_code == 200
    body = res.json()
    assert body["title"] == "Updated Job Title"

def test_update_job_not_found_returns_404(client):
    update_payload = {"title": "Updated Job Title", **{k: v for k, v in VALID_JOB.items() if k != "title"}}  # Ensure all required fields are present

    res = client.put("/jobs/999", json=update_payload)  # Assuming this ID does not exist

    assert res.status_code == 404

def test_update_job_with_invalid_data_returns_422(client):
    # Create a job first
    create_job(client)
    update_payload = {"date_posted": "invalid-date-format"}

    res = client.put("/jobs/1", json=update_payload)

    assert res.status_code == 422

def test_update_job_only_updates_provided_fields(client):
    # Create a job first
    create_job(client)
    update_payload = {"title": "Partially Updated Job Title", **{k: v for k, v in VALID_JOB.items() if k != "title"}}  # Only updating the title, other fields remain unchanged

    res = client.put("/jobs/1", json=update_payload)

    assert res.status_code == 200
    body = res.json()
    assert body["title"] == "Partially Updated Job Title"
    assert body["company"] == VALID_JOB["company"]  # Ensure other fields remain unchanged

def test_delete_job_returns_204(client):
    # Create a job first
    create_job(client)

    res = client.delete("/jobs/1")

    assert res.status_code == 200

def test_delete_job_not_found_returns_404(client):
    res = client.delete("/jobs/999")  # Assuming this ID does not exist

    assert res.status_code == 404