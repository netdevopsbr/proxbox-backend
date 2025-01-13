from backend.routes.netbox.generic import NetboxBase

from backend.routes.netbox.dcim.sites import Site
from backend.routes.netbox.dcim.device_types import DeviceType
from backend.routes.netbox.dcim.device_roles import DeviceRole

from backend.routes.netbox.virtualization.cluster import Cluster

class Device(NetboxBase):
    
    default_name: str = "Proxbox Basic Device"
    default_slug: str = "proxbox-basic-device"
    default_description: str = "Proxbox Basic Device"
    
    app: str = "dcim"
    endpoint: str = "devices"
    object_name: str = "Device"
    
    async def get_base_dict(self):
        site = await Site(nb = self.nb, websocket = self.websocket).get()
        role = await DeviceRole(nb = self.nb, websocket = self.websocket).get()
        device_type = await DeviceType(nb = self.nb, websocket = self.websocket).get()
        cluster = await Cluster(nb = self.nb, websocket = self.websocket).get()
        
        return {
            "name": self.default_name,
            "slug": self.default_slug,
            "description": self.default_description,
            "site": site.id,
            "role": role.id,
            "device_type": device_type.id,
            "status": "active",
            "cluster": cluster.id
        }
