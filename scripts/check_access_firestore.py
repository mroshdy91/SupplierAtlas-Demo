"""Bounded real-store verification, using a temporary isolated collection.

Uses gcloud's current login in memory. Never prints or saves its access token.
Deletes only the documents created in the unique verification collection.
"""
import argparse
import secrets
import subprocess
from concurrent.futures import ThreadPoolExecutor

from google.oauth2.credentials import Credentials

from supplier_atlas.access import AccessError, AccessService, FirestoreAccessStore, Limits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gcloud", required=True)
    parser.add_argument("--project", default="supplieratlas-demo-20261015")
    args = parser.parse_args()
    credential = subprocess.run([args.gcloud, "auth", "print-access-token"], capture_output=True,
                                text=True, check=True).stdout.strip()
    collection = "supplieratlas_check_" + secrets.token_hex(8)
    store = FirestoreAccessStore(args.project, Credentials(credential), collection)
    service = AccessService(store, secrets.token_hex(32), limits=Limits(account_daily=2))
    try:
        token = service.register("integration@example.invalid")["token"]

        def attempt(_):
            try:
                service.authorize(token, tool=True)
                return True
            except AccessError as error:
                assert error.status == 429
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sum(pool.map(attempt, range(4))) == 2
        restarted = AccessService(FirestoreAccessStore(args.project, Credentials(credential), collection),
                                  service.key.decode(), limits=Limits(account_daily=2))
        assert restarted.authorize(token)["daily_tool_remaining"] == 0
        assert restarted.authorize(token, revoke=True)["revoked"]
        try:
            service.authorize(token)
        except AccessError as error:
            assert error.status == 401
        else:
            raise AssertionError("Revoked token authorized")
        print("Firestore: registration, atomic concurrency, restart persistence and revocation passed.")
    finally:
        documents = list(store.collection.limit(10).stream())
        assert len(documents) <= 4
        for document in documents:
            document.reference.delete()
        store.client.close()


if __name__ == "__main__":
    main()
