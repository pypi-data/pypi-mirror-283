from datetime import datetime, timedelta
from http import HTTPStatus
from uuid import uuid4
from flask.testing import FlaskClient
import jwt
from autosubmit_api import config
import pytest
from autosubmit_api.config.basicConfig import APIBasicConfig


class TestLogin:
    endpoint = "/v3/login"

    def test_not_allowed_client(
        self,
        fixture_client: FlaskClient,
        fixture_mock_basic_config: APIBasicConfig,
        monkeypatch: pytest.MonkeyPatch,
    ):
        monkeypatch.setattr(APIBasicConfig, "ALLOWED_CLIENTS", [])

        response = fixture_client.get(self.endpoint)
        resp_obj: dict = response.get_json()

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert resp_obj.get("authenticated") == False

    def test_redirect(
        self,
        fixture_client: FlaskClient,
        fixture_mock_basic_config: APIBasicConfig,
        monkeypatch: pytest.MonkeyPatch,
    ):
        random_referer = str(f"https://${str(uuid4())}/")
        monkeypatch.setattr(APIBasicConfig, "ALLOWED_CLIENTS", [random_referer])

        response = fixture_client.get(
            self.endpoint, headers={"Referer": random_referer}
        )

        assert response.status_code == HTTPStatus.FOUND
        assert config.CAS_LOGIN_URL in response.location
        assert random_referer in response.location


class TestVerifyToken:
    endpoint = "/v3/tokentest"

    def test_unauthorized_no_token(self, fixture_client: FlaskClient):
        response = fixture_client.get(self.endpoint)
        resp_obj: dict = response.get_json()

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert resp_obj.get("isValid") == False

    def test_unauthorized_random_token(self, fixture_client: FlaskClient):
        random_token = str(uuid4())
        response = fixture_client.get(
            self.endpoint, headers={"Authorization": random_token}
        )
        resp_obj: dict = response.get_json()

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert resp_obj.get("isValid") == False

    def test_authorized(self, fixture_client: FlaskClient):
        random_user = str(uuid4())
        payload = {
            "user_id": random_user,
            "exp": (
                datetime.utcnow() + timedelta(seconds=config.JWT_EXP_DELTA_SECONDS)
            ),
        }
        jwt_token = jwt.encode(payload, config.JWT_SECRET, config.JWT_ALGORITHM)

        response = fixture_client.get(
            self.endpoint, headers={"Authorization": jwt_token}
        )
        resp_obj: dict = response.get_json()

        assert response.status_code == HTTPStatus.OK
        assert resp_obj.get("isValid") == True


class TestExpInfo:
    endpoint = "/v3/expinfo/{expid}"

    def test_info(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["expid"] == expid
        assert resp_obj["total_jobs"] == 8

    def test_retro3_info(self, fixture_client: FlaskClient):
        expid = "a3tb"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["expid"] == expid
        assert resp_obj["total_jobs"] == 55
        assert resp_obj["completed_jobs"] == 28


class TestPerformance:
    endpoint = "/v3/performance/{expid}"

    def test_parallelization(self, fixture_client: FlaskClient):
        """
        Test parallelization without PROCESSORS_PER_NODE
        """
        expid = "a007"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["Parallelization"] == 8

        expid = "a3tb"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["Parallelization"] == 768

    def test_parallelization_platforms(self, fixture_client: FlaskClient):
        """
        Test parallelization that comes from default platform
        """
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["Parallelization"] == 16


class TestTree:
    endpoint = "/v3/tree/{expid}"

    def test_tree(self, fixture_client: FlaskClient):
        expid = "a003"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total"] == 8
        assert resp_obj["total"] == len(resp_obj["jobs"])
        for job in resp_obj["jobs"]:
            assert job["id"][:4] == expid

    def test_retro3(self, fixture_client: FlaskClient):
        expid = "a3tb"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total"] == 55
        assert resp_obj["total"] == len(resp_obj["jobs"])
        assert (
            len([job for job in resp_obj["jobs"] if job["status"] == "COMPLETED"]) == 24
        )
        for job in resp_obj["jobs"]:
            assert job["id"][:4] == expid

    def test_wrappers(self, fixture_client: FlaskClient):
        expid = "a6zj"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert len(resp_obj["jobs"]) == 10

        for job in resp_obj["jobs"]:
            if job["section"] == "SIM":
                assert isinstance(job["wrapper"], str) and len(job["wrapper"]) > 0
            else:
                assert job["wrapper"] == None

        assert (
            resp_obj["tree"][2]["title"] == "Wrappers" and resp_obj["tree"][2]["folder"]
        )


class TestRunsList:
    endpoint = "/v3/runs/{expid}"

    def test_runs_list(self, fixture_client: FlaskClient):
        expid = "a003"

        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert isinstance(resp_obj["runs"], list)


class TestRunDetail:
    endpoint = "/v3/rundetail/{expid}/{runId}"

    def test_runs_detail(self, fixture_client: FlaskClient):
        expid = "a003"

        response = fixture_client.get(self.endpoint.format(expid=expid, runId=2))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total"] == 8


class TestQuick:
    endpoint = "/v3/quick/{expid}"

    def test_quick(self, fixture_client: FlaskClient):
        expid = "a007"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total"] == len(resp_obj["tree_view"])
        assert resp_obj["total"] == len(resp_obj["view_data"])


class TestGraph:
    endpoint = "/v3/graph/{expid}/{graph_type}/{grouped}"

    def test_graph_standard_none(self, fixture_client: FlaskClient):
        expid = "a003"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid, graph_type="standard", grouped="none"),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total_jobs"] == len(resp_obj["nodes"])

    def test_graph_standard_datemember(self, fixture_client: FlaskClient):
        expid = "a003"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(
                expid=expid, graph_type="standard", grouped="date-member"
            ),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total_jobs"] == len(resp_obj["nodes"])

    def test_graph_standard_status(self, fixture_client: FlaskClient):
        expid = "a003"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid, graph_type="standard", grouped="status"),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total_jobs"] == len(resp_obj["nodes"])

    def test_graph_laplacian_none(self, fixture_client: FlaskClient):
        expid = "a003"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid, graph_type="laplacian", grouped="none"),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total_jobs"] == len(resp_obj["nodes"])

    def test_graph_standard_none_retro3(self, fixture_client: FlaskClient):
        expid = "a3tb"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid, graph_type="standard", grouped="none"),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total_jobs"] == len(resp_obj["nodes"])

    def test_graph_standard_datemember_retro3(self, fixture_client: FlaskClient):
        expid = "a3tb"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(
                expid=expid, graph_type="standard", grouped="date-member"
            ),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total_jobs"] == len(resp_obj["nodes"])

    def test_graph_standard_status_retro3(self, fixture_client: FlaskClient):
        expid = "a3tb"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid, graph_type="standard", grouped="status"),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()
        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total_jobs"] == len(resp_obj["nodes"])

    def test_wrappers(self, fixture_client: FlaskClient):
        expid = "a6zj"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid, graph_type="standard", grouped="none"),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()

        assert len(resp_obj["nodes"]) == 10

        for node in resp_obj["nodes"]:
            if node["section"] == "SIM":
                assert isinstance(node["wrapper"], str) and len(node["wrapper"]) > 0
            else:
                assert node["wrapper"] == None

        assert "packages" in list(resp_obj.keys())
        assert len(resp_obj["packages"].keys()) > 0


class TestExpCount:
    endpoint = "/v3/expcount/{expid}"

    def test_exp_count(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total"] == sum(
            [resp_obj["counters"][key] for key in resp_obj["counters"]]
        )
        assert resp_obj["expid"] == expid
        assert resp_obj["counters"]["READY"] == 1
        assert resp_obj["counters"]["WAITING"] == 7

    def test_retro3(self, fixture_client: FlaskClient):
        expid = "a3tb"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["total"] == sum(
            [resp_obj["counters"][key] for key in resp_obj["counters"]]
        )
        assert resp_obj["expid"] == expid
        assert resp_obj["counters"]["COMPLETED"] == 24
        assert resp_obj["counters"]["RUNNING"] == 1
        assert resp_obj["counters"]["QUEUING"] == 4
        assert resp_obj["counters"]["SUSPENDED"] == 2
        assert resp_obj["counters"]["WAITING"] == 24


class TestSummary:
    endpoint = "/v3/summary/{expid}"

    def test_summary(self, fixture_client: FlaskClient):
        expid = "a007"
        random_user = str(uuid4())
        response = fixture_client.get(
            self.endpoint.format(expid=expid),
            query_string={"loggedUser": random_user},
        )
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["n_sim"] > 0


class TestStatistics:
    endpoint = "/v3/stats/{expid}/{period}/{section}"

    def test_period_none(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(
            self.endpoint.format(expid=expid, period=0, section="Any")
        )
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["Statistics"]["Period"]["From"] == "None"


class TestCurrentConfig:
    endpoint = "/v3/cconfig/{expid}"

    def test_current_config(self, fixture_client: FlaskClient):
        expid = "a007"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert (
            resp_obj["configuration_filesystem"]["CONFIG"]["AUTOSUBMIT_VERSION"]
            == "4.0.95"
        )

    def test_retrocomp_v3_conf_files(self, fixture_client: FlaskClient):
        expid = "a3tb"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert (
            resp_obj["configuration_filesystem"]["conf"]["config"]["AUTOSUBMIT_VERSION"]
            == "3.13.0"
        )


class TestPklInfo:
    endpoint = "/v3/pklinfo/{expid}/{timestamp}"

    def test_pkl_info(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid, timestamp=0))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert len(resp_obj["pkl_content"]) == 8

        for job_obj in resp_obj["pkl_content"]:
            assert job_obj["name"][:4] == expid


class TestPklTreeInfo:
    endpoint = "/v3/pkltreeinfo/{expid}/{timestamp}"

    def test_pkl_tree_info(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid, timestamp=0))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert len(resp_obj["pkl_content"]) == 8

        for job_obj in resp_obj["pkl_content"]:
            assert job_obj["name"][:4] == expid


class TestExpRunLog:
    endpoint = "/v3/exprun/{expid}"

    def test_exp_run_log(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["found"] == True


class TestIfRunFromLog:
    endpoint = "/v3/logrun/{expid}"

    def test_run_status_from_log(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert isinstance(resp_obj["is_running"], bool)
        assert isinstance(resp_obj["log_path"], str)
        assert isinstance(resp_obj["timediff"], int)


class TestQuickIfRun:
    endpoint = "/v3/ifrun/{expid}"

    def test_quick_run_status(self, fixture_client: FlaskClient):
        expid = "a003"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert isinstance(resp_obj["running"], bool)


class TestJobLogLines:
    endpoint = "/v3/joblog/{logfile}"

    def test_get_logfile_content(self, fixture_client: FlaskClient):
        logfile = "a3tb_19930101_fc01_1_SIM.20211201184808.err"
        response = fixture_client.get(self.endpoint.format(logfile=logfile))
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert resp_obj["found"] == True
        assert isinstance(resp_obj["lastModified"], str)
        assert isinstance(resp_obj["logfile"], str)
        assert isinstance(resp_obj["timeStamp"], int)
        assert isinstance(resp_obj["logcontent"], list)
        assert len(resp_obj["logcontent"]) > 0 and len(resp_obj["logcontent"]) <= 150


class TestJobHistory:
    endpoint = "/v3/history/{expid}/{jobname}"

    def test_job_history(self, fixture_client: FlaskClient):
        expid = "a3tb"
        jobname = "a3tb_19930101_fc01_1_SIM"
        response = fixture_client.get(
            self.endpoint.format(expid=expid, jobname=jobname)
        )
        resp_obj: dict = response.get_json()

        assert resp_obj["error_message"] == ""
        assert resp_obj["error"] == False
        assert isinstance(resp_obj["path_to_logs"], str)
        assert isinstance(resp_obj["history"], list)
        assert len(resp_obj["history"]) > 0


class TestSearchExpid:
    endpoint = "/v3/search/{expid}"

    def test_search_by_expid(self, fixture_client: FlaskClient):
        expid = "a3tb"
        response = fixture_client.get(self.endpoint.format(expid=expid))
        resp_obj: dict = response.get_json()

        assert isinstance(resp_obj["experiment"], list)
        assert len(resp_obj["experiment"]) > 0


class TestRunningExps:
    endpoint = "/v3/running/"

    def test_search_by_expid(self, fixture_client: FlaskClient):
        expid = "a3tb"
        response = fixture_client.get(self.endpoint)
        resp_obj: dict = response.get_json()

        assert isinstance(resp_obj["experiment"], list)
