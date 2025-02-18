from fastapi import APIRouter

from backend.schemas.proxmox import *
from backend.session.proxmox import ProxmoxSessionsDep
from backend.enum.proxmox import *

router = APIRouter()

#
# /proxmox/* API Endpoints
#

@router.get("/sessions")
async def proxmox_sessions(
    pxs: ProxmoxSessionsDep
):
    """
    ### Asynchronously retrieves Proxmox session details and returns them as a JSON response.
    
    **Args:**
    - **pxs (`ProxmoxSessionsDep`):** A dependency injection of Proxmox sessions.
    
    **Returns:**
    - **list:** A list of dictionaries containing Proxmox session details, each with the following keys:
        - **domain (str):** The domain of the Proxmox session.
        - **http_port (int):** The HTTP port of the Proxmox session.
        - **user (str):** The user associated with the Proxmox session.
        - **name (str):** The name of the Proxmox session.
        - **mode (str):** The mode of the Proxmox session.
    """
    
    json_response = []
    
    for px in pxs:
        json_response.append(
            {
                "domain": px.domain,
                "http_port": px.http_port,
                "user": px.user,
                "name": px.name,
                "mode": px.mode,
            }
        )
    
    return json_response



@router.get("/version", )
async def proxmox_version(
    pxs: ProxmoxSessionsDep
):
    """
    ### Retrieve the version information from multiple Proxmox sessions.
    
    *Args:**
        **pxs (`ProxmoxSessionsDep`):** A dependency injection of Proxmox sessions.
    
    **Returns:**
        **list:** A list of dictionaries containing the name and version of each Proxmox session.
    """
    json_response = []
    
    for px in pxs:
        json_response.append(
            {
                px.name: px.session.version.get()
            }
        )
            
    return json_response


@router.get("/{top_level}")
async def top_level_endpoint(
    pxs: ProxmoxSessionsDep,
    top_level: ProxmoxUpperPaths,
):
    """
    ### Asynchronously retrieves data from multiple Proxmox sessions for a given top-level path.
    
    **Args:**    
    - **pxs (`ProxmoxSessionsDep`):** A dependency injection of Proxmox sessions.
    - **top_level (`ProxmoxUpperPaths`):** The top-level path to query in each Proxmox session.
    
    **Returns:**
    - **list:** A list of dictionaries containing the session name as the key and the response data as the value.
    """
    
    json_response = []
    
    for px in pxs:
        json_response.append(
            {  
                px.name: px.session(top_level).get()
            }
        )
    
    return json_response


@router.get("/")
async def proxmox(
    pxs: ProxmoxSessionsDep
):
    """
    #### Fetches and compiles data from multiple Proxmox sessions.
    
    **Args:**
    - **pxs (ProxmoxSessionsDep):** A dependency injection of Proxmox sessions.
    
    **Returns:**
    - **dict:** A dictionary containing:
        - **message (`str`):** A static message "Proxmox API".
        - **proxmox_api_viewer (`str`):** URL to the Proxmox API viewer.
        - **github (`dict`):** URLs to relevant GitHub repositories.
        - **clusters (`list`):** A list of dictionaries, each representing a Proxmox session with keys:
            - **ccess (`list`):** Minimized result of the "access" endpoint.
            - **cluster (`list`):** Minimized result of the "cluster" endpoint.
            - **nodes (`list`):** Result of the "nodes" endpoint.
            - **pools (`list`):** Result of the "pools" endpoint.
            - **storage (`list`):** Result of the "storage" endpoint.
            - **version (`dict`):** Result of the "version" endpoint.
    """
    
    json_response = []

    def minimize_result(endpoint_name):
        """
        Minimize the result obtained from a Proxmox endpoint.
        This function retrieves data from a specified Proxmox endpoint and extracts
        specific fields based on the endpoint name. The extracted fields are then
        returned as a list.
        
        **Args:**
        - **endpoint_name (`str`):** The name of the Proxmox endpoint to query. 
        Supported values are "access" and "cluster".
        
        **Returns:**
        - **list:** A list of extracted fields from the Proxmox endpoint. For the 
            - "access" endpoint, it returns a list of "subdir" values. For the 
            - "cluster" endpoint, it returns a list of "name" values.
        """
        
        endpoint_list = []
        result = px.session(endpoint_name).get()
        
        match endpoint_name:
            case "access":
                for obj in result:
                    endpoint_list.append(obj.get("subdir"))
            
            case "cluster":
                for obj in result:
                    endpoint_list.append(obj.get("name"))
                
        return endpoint_list
    
    for px in pxs:  
        json_response.append(
            {
                f"{px.name}": {
                    "access": minimize_result("access"),
                    "cluster": minimize_result("cluster"),
                    "nodes": px.session.nodes.get(),
                    "pools": px.session.pools.get(),
                    "storage": px.session.storage.get(),
                    "version": px.session.version.get(),
                }
            } 
        )

    return {
        "message": "Proxmox API",
        "proxmox_api_viewer": "https://pve.proxmox.com/pve-docs/api-viewer/",
        "github": {
            "netbox": "https://github.com/netbox-community/netbox",
            "pynetbox": "https://github.com/netbox-community/pynetbox",
            "proxmoxer": "https://github.com/proxmoxer/proxmoxer",
            "proxbox": "https://github.com/netdevopsbr/netbox-proxbox"
        },
        "clusters": json_response
    }