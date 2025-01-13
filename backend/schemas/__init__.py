from pydantic import BaseModel
from backend.schemas.netbox import NetboxSessionSchema
from backend.schemas.proxmox import ProxmoxSessionSchema

class PluginConfig(BaseModel):
    proxmox: list[ProxmoxSessionSchema]
    netbox: NetboxSessionSchema