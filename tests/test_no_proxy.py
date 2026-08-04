import unittest

from desktop_env.network import add_no_proxy_host


class NoProxyTests(unittest.TestCase):
    def test_adds_vm_host_and_preserves_existing_entries(self):
        environ = {
            "NO_PROXY": "localhost,127.0.0.1",
            "no_proxy": "metadata.internal",
        }

        merged = add_no_proxy_host("203.0.113.10", environ)

        self.assertEqual(
            merged,
            "localhost,127.0.0.1,metadata.internal,203.0.113.10",
        )
        self.assertEqual(environ["NO_PROXY"], merged)
        self.assertEqual(environ["no_proxy"], merged)

    def test_deduplicates_and_normalizes_bracketed_hosts(self):
        environ = {"NO_PROXY": "2001:db8::1"}

        merged = add_no_proxy_host("[2001:db8::1]", environ)

        self.assertEqual(merged, "2001:db8::1")

    def test_rejects_empty_host(self):
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            add_no_proxy_host("  ", {})


if __name__ == "__main__":
    unittest.main()
