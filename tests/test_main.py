async def test_root_healthcheck_endpoint_returns_body_with_ok_in_status(client):
    response = await client.get('/')
    data = response.json()

    assert data['status'] == 'OK'
