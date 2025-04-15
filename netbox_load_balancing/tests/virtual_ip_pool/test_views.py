from utilities.testing import ViewTestCases, create_tags

from netbox_load_balancing.tests.custom import ModelViewTestCase
from netbox_load_balancing.models import VirtualIPPool


class VirtualIPPoolViewTestCase(
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
    model = VirtualIPPool

    @classmethod
    def setUpTestData(cls):
        cls.pools = (
            VirtualIPPool(name="virtual-pool-1", disabled=True),
            VirtualIPPool(name="virtual-pool-2", disabled=True),
            VirtualIPPool(name="virtual-pool-3", disabled=True),
        )
        VirtualIPPool.objects.bulk_create(cls.pools)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "virtual-pool-4",
            "disabled": False,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,disabled",
            "virtual-pool-5,True",
            "virtual-pool-6,True",
            "virtual-pool-7,False",
        )

        cls.csv_update_data = (
            "id,name,description,disabled",
            f"{cls.pools[0].pk},service-8,test1,True",
            f"{cls.pools[1].pk},service-9,test2,True",
            f"{cls.pools[2].pk},service-10,test3,False",
        )

    maxDiff = None
