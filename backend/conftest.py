import pytest
import sys
sys.path.append("/app")
import common.connection

@pytest.fixture(scope="session")
def cleanDatabase(request):
    conn = common.connection.Connection('test')
    conn.execute(f"TRUNCATE TABLE q_table")
    conn.execute(f"TRUNCATE TABLE steps")
