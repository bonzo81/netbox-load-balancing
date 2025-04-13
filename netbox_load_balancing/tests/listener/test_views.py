from utilities.testing import ViewTestCases, create_tags

from netbox_load_balancing.tests.custom import ModelViewTestCase
from netbox_load_balancing.models import Listener, LBService
from netbox_load_balancing.choices import ListenerProtocolChoices


class ListenerViewTestCase(
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
    model = Listener

    @classmethod
    def setUpTestData(cls):
        cls.services = (
            LBService(name="service-1", reference="1.1.1.1/32", disabled=True),
            LBService(name="service-2", reference="1.1.1.2/32", disabled=True),
            LBService(name="service-3", reference="1.1.1.3/32", disabled=True),
        )
        LBService.objects.bulk_create(cls.services)
        cls.listeners = (
            Listener(name="listener-1", service=cls.services[0], port=10),
            Listener(name="listener-2", service=cls.services[1], port=10),
            Listener(
                name="listener-3",
                service=cls.services[2],
                port=10,
                protocol=ListenerProtocolChoices.HTTP,
            ),
        )
        Listener.objects.bulk_create(cls.listeners)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "listener-4",
            "service": cls.services[0].pk,
            "port": 10,
            "protocol": ListenerProtocolChoices.HTTP,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,port,service",
            f"listener-5,10,{cls.services[0].name}",
            f"listener-6,10,{cls.services[0].name}",
            f"listener-7,10,{cls.services[0].name}",
        )

        cls.csv_update_data = (
            "id,name,port,description",
            f"{cls.listeners[0].pk},listener-8,20,test1",
            f"{cls.listeners[1].pk},listener-9,20,test2",
            f"{cls.listeners[2].pk},listener-10,20,test3",
        )

    maxDiff = None
