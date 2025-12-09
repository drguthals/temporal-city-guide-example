import os
from temporalio.client import Client, TLSConfig

async def get_client() -> Client:
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
    
    # Read the content directly from the environment variable
    cert_raw = os.getenv("TEMPORAL_CLIENT_CERT")
    key_raw = os.getenv("TEMPORAL_CLIENT_KEY")
    
    tls_config = None
    
    if cert_raw and key_raw:
        # CRITICAL: Fix newlines if the cloud provider escaped them.
        # Many secret managers turn:
        #   "-----BEGIN CERTIFICATE-----\nMIIDT..."
        # into:
        #   "-----BEGIN CERTIFICATE-----\\nMIIDT..."
        # We replace the literal characters "\n" with actual newlines.
        cert_str = cert_raw.replace("\\n", "\n")
        key_str = key_raw.replace("\\n", "\n")

        # Convert the string to bytes, which the SDK expects
        tls_config = TLSConfig(
            client_cert=cert_str.encode("utf-8"),
            client_private_key=key_str.encode("utf-8"),
        )

    return await Client.connect(
        temporal_host,
        namespace=namespace,
        tls=tls_config
    )