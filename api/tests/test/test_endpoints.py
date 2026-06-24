


def test_disk(client):
    resp = client.get("/metrics/average/hourly/disl")
    assert resp.status_code == 200
    data = resp.json()
    assert data[0]["disk_pct"] == 40.0
    assert data[1]["disk_pct"] == 41.5