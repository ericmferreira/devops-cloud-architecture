

class ProvisionService:

    def process(self, payload: dict) -> None:

        print(f"Starting provisioning request #{payload['id']}", flush=True)
        print(f"Provider: {payload['provider']}", flush=True)
        print(f"Resource: {payload['resource_type']}", flush=True)
        print(f"Location: {payload['location']}", flush=True)
        print("Provisioning completed successfully.", flush=True)

        print("Provisioning completed successfully.")