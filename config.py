# config.py
import os
from temporalio.client import Client, TLSConfig

async def get_client() -> Client:
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
    
    # Try reading file paths first
    client_cert_path = os.getenv("TEMPORAL_CLIENT_CERT_PATH")
    client_key_path = os.getenv("TEMPORAL_CLIENT_KEY_PATH")
    
    tls_config = None
    
    if client_cert_path and client_key_path:
        # Read from files (Best for Docker/Local)
        with open(client_cert_path, "rb") as f:
            cert_data = f.read()
        with open(client_key_path, "rb") as f:
            key_data = f.read()
            
        tls_config = TLSConfig(
            client_cert=cert_data,
            client_private_key=key_data,
        )
    else:
        # Fallback to reading raw strings (Good for GitHub Actions)
        cert_raw = os.getenv("TEMPORAL_CLIENT_CERT")
        key_raw = os.getenv("TEMPORAL_CLIENT_KEY")
        
        if cert_raw and key_raw:
            cert_str = cert_raw.replace("\\n", "\n")
            key_str = key_raw.replace("\\n", "\n")
            tls_config = TLSConfig(
                client_cert=cert_str.encode("utf-8"),
                client_private_key=key_str.encode("utf-8"),
            )

    return await Client.connect(
        temporal_host,
        namespace=namespace,
        tls=tls_config
    )