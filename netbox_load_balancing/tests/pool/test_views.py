from utilities.testing import ViewTestCases, create_tags

from netbox_load_balancing.tests.custom import ModelViewTestCase
from netbox_load_balancing.models import LBService, Pool, Listener
from netbox_load_balancing.choices import (
    PoolAlgorythmChoices,
    PoolSessionPersistenceChoices,
    PoolBackupSessionPersistenceChoices,
)


class PoolViewTestCase(
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
    model = Pool

    @classmethod
    def setUpTestData(cls):
        cls.services = (
            LBService(name="service-1", reference="1.1.1.4/32", disabled=True),
            LBService(name="service-2", reference="1.1.1.5/32", disabled=True),
            LBService(name="service-3", reference="1.1.1.6/32", disabled=True),
        )
        LBService.objects.bulk_create(cls.services)

        cls.listeners = (
            Listener(name="listener-1", service=cls.services[0], port=10),
            Listener(name="listener-2", service=cls.services[1], port=10),
            Listener(name="listener-3", service=cls.services[2], port=10),
        )
        Listener.objects.bulk_create(cls.listeners)

        cls.pools = (
            Pool(
                name="pool-1",
                member_port=1,
                disabled=True,
                backup_persistence=PoolBackupSessionPersistenceChoices.SOURCE_IP,
            ),
            Pool(
                name="pool-2",
                member_port=1,
                disabled=True,
                algorythm=PoolAlgorythmChoices.ROUND_ROBIN,
            ),
            Pool(
                name="pool-3",
                member_port=1,
                disabled=False,
                session_persistence=PoolSessionPersistenceChoices.SSL_BRIDGE,
            ),
        )
        Pool.objects.bulk_create(cls.pools)
        for p in cls.pools:
            p.listeners.set(cls.listeners)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "pool-4",
            "listeners": [cls.listeners[0].pk, cls.listeners[1].pk],
            "member_port": 1,
            "disabled": False,
            "backup_persistence": PoolBackupSessionPersistenceChoices.SOURCE_IP,
            "session_persistence": PoolSessionPersistenceChoices.SSL_BRIDGE,
            "algorythm": PoolAlgorythmChoices.ROUND_ROBIN,
            "backup_timeout": 10,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,member_port,disabled",
            "pool-5,1,true",
            "pool-6,2,true",
            "pool-7,3,false",
        )

        cls.csv_update_data = (
            "id,name,member_port,description,disabled",
            f"{cls.pools[0].pk},pool-8,4,test1,true",
            f"{cls.pools[1].pk},pool-9,5,test2,true",
            f"{cls.pools[2].pk},pool-10,6,test3,false",
        )

    maxDiff = None
