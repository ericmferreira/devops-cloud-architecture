class NotificationService:

    def process(self, payload: dict) -> None:

        print(
            f"""
========================================
Notification

Request : {payload["request_id"]}
Status  : {payload["status"]}
Provider: {payload["provider"]}

Message : {payload["message"]}
========================================
""",
            flush=True,
        )