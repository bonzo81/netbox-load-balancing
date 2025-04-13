from utilities.testing import ViewTestCases, create_tags

from netbox_load_balancing.tests.custom import ModelViewTestCase
from netbox_load_balancing.models import LBService


class LBServiceViewTestCase(
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
    model = LBService

    @classmethod
    def setUpTestData(cls):
        cls.services = (
            LBService(name="service-1", reference="1.1.1.1/32", disabled=True),
            LBService(name="service-2", reference="1.1.1.2/32", disabled=True),
            LBService(name="service-3", reference="1.1.1.3/32", disabled=True),
        )
        LBService.objects.bulk_create(cls.services)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "service-4",
            "reference": "1.1.1.4/32",
            "disabled": False,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,reference,disabled",
            "service-5,1.1.1.5/32,True",
            "service-6,1.1.1.6/32,True",
            "service-7,1.1.1.7/32,False",
        )

        cls.csv_update_data = (
            "id,name,reference,description,disabled",
            f"{cls.services[0].pk},service-8,1.1.1.8/32,test1,True",
            f"{cls.services[1].pk},service-9,1.1.1.9/32,test2,True",
            f"{cls.services[2].pk},service-10,1.1.1.10/32,test3,False",
        )

    maxDiff = None
