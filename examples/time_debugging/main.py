from datetime import datetime


class SubscriptionManager:
    def __init__(self, user_name):
        self.user_name = user_name
        self.registered_at = datetime.now()

    def get_expiration_date(self):
        return self.registered_at.replace(year=self.registered_at.year + 1)

    def check_status(self):
        print(f"Checking subscription for: {self.user_name}")
        print(f"Registered on: {self.registered_at.strftime('%Y-%m-%d')}")

        try:
            expire_date = self.get_expiration_date()
            days_left = (expire_date - datetime.now()).days

            if days_left < 0:
                print("Valid until: EXPIRED")
                return False
            else:
                print(
                    f"Valid until: {expire_date.strftime('%Y-%m-%d')} ({days_left} days left)"
                )
                return True
        except Exception as e:
            print(f"[CRITICAL ERROR] System crashed during validation: {e}")


def main():
    manager = SubscriptionManager("AdminUser")

    status = manager.check_status()

    if status is True:
        print(">> Access Granted.")
    elif status is False:
        print(">> Access Denied.")
    else:
        print(">> Unknown Status.")


if __name__ == "__main__":
    main()
