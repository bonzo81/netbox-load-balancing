from utilities.testing import ViewTestCases, create_tags

from netbox_load_balancing.tests.custom import ModelViewTestCase
from netbox_load_balancing.models import HealthMonitor
from netbox_load_balancing.choices import (
    HealthMonitorTypeChoices,
)


class HealthMonitorViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = HealthMonitor

    @classmethod
    def setUpTestData(cls):
        cls.monitors = (
            HealthMonitor(
                name="monitor-4",
                type=HealthMonitorTypeChoices.PING,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=True,
            ),
            HealthMonitor(
                name="monitor-5",
                type=HealthMonitorTypeChoices.HTTP,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=True,
            ),
            HealthMonitor(
                name="monitor-6",
                type=HealthMonitorTypeChoices.HTTP,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=False,
            ),
        )
        HealthMonitor.objects.bulk_create(cls.monitors)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "monitor-4",
            "type": HealthMonitorTypeChoices.PING,
            "monitor_port": 10,
            "http_response_codes": "200,201",
            "disabled": False,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,type,disabled",
            f"monitor-5,{HealthMonitorTypeChoices.PING},True",
            f"monitor-6,{HealthMonitorTypeChoices.PING},True",
            f"monitor-7,{HealthMonitorTypeChoices.PING},False",
        )

        cls.csv_update_data = (
            "id,name,type,description,disabled",
            f"{cls.monitors[0].pk},monitor-8,{HealthMonitorTypeChoices.PING},test1,True",
            f"{cls.monitors[1].pk},monitor-9,{HealthMonitorTypeChoices.PING},test2,True",
            f"{cls.monitors[2].pk},monitor-10,{HealthMonitorTypeChoices.PING},test3,False",
        )

    maxDiff = None
