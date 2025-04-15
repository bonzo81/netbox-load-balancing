from django.contrib.contenttypes.models import ContentType
from utilities.testing import ViewTestCases, create_tags

from netbox_load_balancing.tests.custom import ModelViewTestCase
from ipam.models import Prefix, IPAddress, IPRange

from netbox_load_balancing.models import (
    VirtualIP,
    VirtualIPPool,
    VirtualIPPoolAssignment,
)


class VirtualIPViewTestCase(
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
    model = VirtualIP

    @classmethod
    def setUpTestData(cls):
        cls.prefixes = (
            Prefix(prefix="10.1.1.0/24", status="active"),
            Prefix(prefix="10.1.2.0/24", status="active"),
        )
        Prefix.objects.bulk_create(cls.prefixes)

        cls.ip_ranges = (
            IPRange(start_address="10.1.3.1/24", end_address="10.1.3.254/24", size=253),
        )
        IPRange.objects.bulk_create(cls.ip_ranges)

        cls.addresses = (
            IPAddress(address="10.1.1.1/24", status="active"),
            IPAddress(address="10.1.1.2/24", status="active"),
            IPAddress(address="10.1.3.1/24", status="active"),
            IPAddress(address="10.1.3.2/24", status="active"),
        )
        IPAddress.objects.bulk_create(cls.addresses)

        cls.pools = (
            VirtualIPPool(name="virtual-pool-4", disabled=False),
            VirtualIPPool(name="virtual-pool-5", disabled=False),
            VirtualIPPool(name="virtual-pool-6", disabled=False),
        )
        VirtualIPPool.objects.bulk_create(cls.pools)

        cls.assignments = (
            VirtualIPPoolAssignment(
                virtual_pool=cls.pools[0],
                assigned_object=cls.prefixes[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "ipam", "prefix"
                ),
                assigned_object_id=cls.prefixes[0].pk,
                weight=5,
                disabled=False,
            ),
            VirtualIPPoolAssignment(
                virtual_pool=cls.pools[0],
                assigned_object=cls.prefixes[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "ipam", "prefix"
                ),
                assigned_object_id=cls.prefixes[1].pk,
                weight=1,
                disabled=True,
            ),
            VirtualIPPoolAssignment(
                virtual_pool=cls.pools[1],
                assigned_object=cls.prefixes[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "ipam", "prefix"
                ),
                assigned_object_id=cls.prefixes[0].pk,
                weight=1,
                disabled=False,
            ),
            VirtualIPPoolAssignment(
                virtual_pool=cls.pools[2],
                assigned_object=cls.ip_ranges[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "ipam", "iprange"
                ),
                assigned_object_id=cls.ip_ranges[0].pk,
                weight=1,
                disabled=False,
            ),
        )
        VirtualIPPoolAssignment.objects.bulk_create(cls.assignments)

        cls.vips = (
            VirtualIP(
                name="virtual-ip-1",
                virtual_pool=cls.pools[0],
                address=cls.addresses[0],
                dns_name="test4.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-2",
                virtual_pool=cls.pools[0],
                address=cls.addresses[1],
                dns_name="test4.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-3",
                virtual_pool=cls.pools[1],
                address=cls.addresses[2],
                dns_name="test5.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-4",
                virtual_pool=cls.pools[2],
                address=cls.addresses[3],
                dns_name="test6.example.com",
                disabled=False,
                route_health_injection=False,
            ),
        )
        VirtualIP.objects.bulk_create(cls.vips)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "virtual-ip-5",
            "virtual_pool": cls.pools[0].pk,
            "dns_name": "test5.example.com",
            "disabled": False,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,dns_name,virtual_pool,disabled",
            f"virtual-ip-6,test6.example.com,{cls.pools[0].name},True",
            f"virtual-ip-7,test7.example.com,{cls.pools[1].name},True",
            f"virtual-ip-8,test8.example.com,{cls.pools[2].name},False",
        )

        cls.csv_update_data = (
            "id,name,dns_name,description,disabled",
            f"{cls.vips[0].pk},virtual-ip-9,test9.example.com,test1,True",
            f"{cls.vips[1].pk},virtual-ip-10,test10.example.com,test2,True",
            f"{cls.vips[2].pk},virtual-ip-11,test11.example.com,test3,False",
        )

    maxDiff = None
