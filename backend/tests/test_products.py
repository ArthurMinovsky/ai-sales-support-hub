def test_product_crud_and_persistence(client, auth, example_product):
    create = client.post("/api/products", headers=auth, json=example_product)
    assert create.status_code == 201
    product_id = create.json()["id"]
    products = client.get("/api/products", headers=auth)
    assert products.status_code == 200
    assert any(p["id"] == product_id for p in products.json())
    assert client.get(f"/api/products/{product_id}", headers=auth).json()["name"] == example_product["name"]
    change = client.put(f"/api/products/{product_id}", headers=auth, json={**example_product, "name": "Updated device"})
    assert change.status_code == 200
    assert change.json()["name"] == "Updated device"
    assert client.get("/api/products", headers=auth, params={"search": "Updated device"}).json()[0]["id"] == product_id
    assert client.delete(f"/api/products/{product_id}", headers=auth).status_code == 204
    assert client.get(f"/api/products/{product_id}", headers=auth).status_code == 404


def test_validation_and_missing_id(client, auth, example_product):
    assert client.post("/api/products", headers=auth, json={**example_product, "description": "short"}).status_code == 422
    assert client.post("/api/products", headers=auth, json={**example_product, "image_url": "http://127.0.0.1/"}).status_code == 422
    assert client.post("/api/products", headers=auth, json={**example_product, "name": "  "}).status_code == 422
    assert client.put("/api/products/987654", headers=auth, json=example_product).status_code == 404
    assert client.delete("/api/products/987654", headers=auth).status_code == 404
