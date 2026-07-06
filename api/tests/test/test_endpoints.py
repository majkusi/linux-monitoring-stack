


def test_disk(client):
    resp = client.get("/metrics/average/hourly/disk")
    assert resp.status_code == 200
    data = resp.json()
    assert data[0]["disk_pct"] == 40.0
    assert data[1]["disk_pct"] == 41.5

def test_cpu(client):
    resp = client.get("/metrics/average/hourly/cpu")
    assert resp.status_code == 200
    data = resp.json()
    assert data[0]["cpu_pct"] == 12.5
    assert data[1]["cpu_pct"] == 18.0

def test_ram(client):
    resp = client.get("/metrics/average/hourly/ram")
    assert resp.status_code == 200
    data = resp.json()
    assert data[0]["ram_pct"] == 62.5
    assert data[0]["ram_used"] == 5000.0
    assert data[1]["ram_pct"] == 64.0
    assert data[1]["ram_used"] == 5120.0

def test_http_response(client):
    resp = client.get("/metrics/status/test_results")
    assert resp.status_code == 200
    data = resp.json()
    assert data["http"] == 200
    assert data["mtls_no_cert"] == 0
    assert data["mtls_cert"] == 404
