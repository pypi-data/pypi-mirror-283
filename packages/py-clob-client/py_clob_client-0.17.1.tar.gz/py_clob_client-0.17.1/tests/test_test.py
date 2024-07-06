from unittest import TestCase

from py_clob_client.clob_types import (
    ApiCreds,
)
from py_clob_client.client import ClobClient
from py_clob_client.constants import AMOY

from dotenv import load_dotenv

import os

load_dotenv()


class TestTest(TestCase):
    def test(self):
        host = "https://clob-staging.polymarket.com"
        key = "61925f6e49905e7551884129c1d46b3661d6b566173feee556737743162bec7d"
        creds = ApiCreds(
            api_key="1229b503-3124-94d7-0b28-46e64418510f",
            api_secret="1vslCNSHeKXnPIsitiDirDrQ8sPPI4hyXYqIXkBwfPs=",
            api_passphrase="8f25643b36d0c8be522646356010f3b1c61c1b47eada77ad8b4b58e9be7c87c0",
        )
        chain_id = AMOY
        client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

        print(client.cancel_market_orders(asset_id="100"))
        # print(client.cancel("0x0"))
        print("Done!")
