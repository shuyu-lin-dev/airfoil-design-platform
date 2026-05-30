import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


# Fixture that builds a standalone app with just the geometry router.
# Avoiding main.py registration keeps T003 self-contained within allowed_paths.
@pytest.fixture
def client():
    from airfoil_platform.api.geometry import router

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestAirfoil2D:
    VALID_CST = [0.15, 0.20, 0.15, 0.10, 0.05, 0.02, 0.08, 0.10, 0.08, 0.05, 0.02, 0.01]

    def test_returns_200_points_with_meta(self, client):
        resp = client.post("/geometry/airfoil-2d", json={"cst_params": self.VALID_CST})
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["points"]) == 200
        assert body["is_stub"] is True
        assert body["model_version"] == "stub-v0"

    def test_first_100_upper_last_100_lower(self, client):
        resp = client.post("/geometry/airfoil-2d", json={"cst_params": self.VALID_CST})
        body = resp.json()
        points = body["points"]
        assert len(points) == 200
        # Upper surface (first 100) and lower surface (last 100) should have
        # differing y values near mid-chord for a non-symmetric airfoil.
        upper_mid_y = points[50]["y"]
        lower_mid_y = points[150]["y"]
        assert upper_mid_y != lower_mid_y

    def test_every_point_has_x_and_y(self, client):
        resp = client.post("/geometry/airfoil-2d", json={"cst_params": self.VALID_CST})
        body = resp.json()
        for pt in body["points"]:
            assert isinstance(pt["x"], (int, float))
            assert isinstance(pt["y"], (int, float))

    def test_points_are_ordered_along_chord(self, client):
        resp = client.post("/geometry/airfoil-2d", json={"cst_params": self.VALID_CST})
        body = resp.json()
        upper = body["points"][:100]
        lower = body["points"][100:]
        # Upper surface: x increasing from LE to TE
        for i in range(len(upper) - 1):
            assert upper[i]["x"] <= upper[i + 1]["x"]
        # Lower surface: x increasing from LE to TE
        for i in range(len(lower) - 1):
            assert lower[i]["x"] <= lower[i + 1]["x"]

    def test_leading_edge_coincides(self, client):
        resp = client.post("/geometry/airfoil-2d", json={"cst_params": self.VALID_CST})
        body = resp.json()
        upper = body["points"][:100]
        lower = body["points"][100:]
        # Leading edge (x≈0): both surfaces should be near y=0
        assert abs(upper[0]["x"]) < 0.01
        assert abs(lower[0]["x"]) < 0.01
        assert abs(upper[0]["y"]) < 1e-6
        assert abs(lower[0]["y"]) < 1e-6

    def test_trailing_edge_coincides(self, client):
        resp = client.post("/geometry/airfoil-2d", json={"cst_params": self.VALID_CST})
        body = resp.json()
        upper = body["points"][:100]
        lower = body["points"][100:]
        # Trailing edge (x≈1): both surfaces should be near y=0
        assert abs(upper[99]["x"] - 1.0) < 0.01
        assert abs(lower[99]["x"] - 1.0) < 0.01
        assert abs(upper[99]["y"]) < 1e-6
        assert abs(lower[99]["y"]) < 1e-6


class TestAirfoil2DValidation:
    @pytest.mark.parametrize("bad_cst", [
        [0.1] * 11,
        [0.1] * 13,
        [],
        [0.1] * 20,
    ])
    def test_wrong_cst_count_returns_422(self, bad_cst):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from airfoil_platform.api.geometry import router

        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        resp = client.post("/geometry/airfoil-2d", json={"cst_params": bad_cst})
        assert resp.status_code == 422

    def test_missing_cst_params_returns_422(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from airfoil_platform.api.geometry import router

        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        resp = client.post("/geometry/airfoil-2d", json={})
        assert resp.status_code == 422
