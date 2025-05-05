import strawberry_django

from netbox.graphql.filter_mixins import PrimaryModelFilterMixin
from tenancy.graphql.filter_mixins import TenancyFilterMixin

from netbox_load_balancing.models import (
    LBService,
    Listener,
    HealthMonitor,
    Pool,
    Member,
    VirtualIPPool,
    VirtualIP,
)


@strawberry_django.filter(LBService, lookups=True)
class NetBoxLoadBalancingLBServiceFilter(TenancyFilterMixin, PrimaryModelFilterMixin):
    pass


@strawberry_django.filter(Listener, lookups=True)
class NetBoxLoadBalancingListenerFilter(PrimaryModelFilterMixin):
    pass


@strawberry_django.filter(HealthMonitor, lookups=True)
class NetBoxLoadBalancingHealthMonitorFilter(PrimaryModelFilterMixin):
    pass


@strawberry_django.filter(Pool, lookups=True)
class NetBoxLoadBalancingPoolFilter(PrimaryModelFilterMixin):
    pass


@strawberry_django.filter(Member, lookups=True)
class NetBoxLoadBalancingMemberFilter(PrimaryModelFilterMixin):
    pass


@strawberry_django.filter(VirtualIPPool, lookups=True)
class NetBoxLoadBalancingVirtualIPPoolFilter(TenancyFilterMixin, PrimaryModelFilterMixin):
    pass


@strawberry_django.filter(VirtualIP, lookups=True)
class NetBoxLoadBalancingVirtualIPFilter(PrimaryModelFilterMixin):
    pass
