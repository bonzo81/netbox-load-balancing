from utilities.testing import ViewTestCases, create_tags

from ipam.models import IPAddress

from netbox_load_balancing.tests.custom import ModelViewTestCase
from netbox_load_balancing.models import Member


class MemberViewTestCase(
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
    model = Member

    @classmethod
    def setUpTestData(cls):
        cls.addresses = (
            IPAddress(
                address="1.1.1.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.2.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.3.1/24",
                status="active",
            ),
        )
        IPAddress.objects.bulk_create(cls.addresses)

        cls.members = (
            Member(
                name="member-1",
                reference="1.1.1.4/32",
                disabled=True,
                ip_address=cls.addresses[0],
            ),
            Member(
                name="member-2",
                reference="1.1.1.5/32",
                disabled=True,
                ip_address=cls.addresses[1],
            ),
            Member(
                name="member-3",
                reference="1.1.1.6/32",
                disabled=False,
                ip_address=cls.addresses[2],
            ),
        )
        Member.objects.bulk_create(cls.members)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "member-4",
            "reference": "1.1.1.4/32",
            "disabled": False,
            "ip_address": cls.addresses[0].pk,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,reference,disabled,ip_address",
            f"member-5,1.1.1.5/32,True,{cls.addresses[0].address}",
            f"member-6,1.1.1.6/32,True,{cls.addresses[1].address}",
            f"member-7,1.1.1.7/32,False,{cls.addresses[2].address}",
        )

        cls.csv_update_data = (
            "id,name,reference,description,disabled",
            f"{cls.members[0].pk},member-8,1.1.1.8/32,test1,True",
            f"{cls.members[1].pk},member-9,1.1.1.9/32,test2,True",
            f"{cls.members[2].pk},member-10,1.1.1.10/32,test3,False",
        )

    maxDiff = None
