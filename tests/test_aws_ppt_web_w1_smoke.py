import json
import unittest
from unittest.mock import MagicMock, call, patch

from scripts.python.smoke_aws_ppt_web_w1 import (
    _desktop_is_ready,
    _launch_chrome,
    _request,
    _verify_screenshot,
)


class AwsPptWebW1SmokeTests(unittest.TestCase):
    @patch("scripts.python.smoke_aws_ppt_web_w1.DIRECT_HTTP_SESSION.request")
    def test_head_probe_does_not_read_response_body(self, request):
        response = MagicMock()
        response.status_code = 200
        request.return_value = response

        payload = _request("http://example.test/screenshot", method="HEAD")

        self.assertEqual(payload, b"")
        self.assertEqual(request.call_args.args[:2], ("HEAD", "http://example.test/screenshot"))

    @patch("scripts.python.smoke_aws_ppt_web_w1._launch_command")
    def test_chrome_launch_uses_official_cdp_bridge(self, launch_command):
        _launch_chrome("203.0.113.10")

        self.assertEqual(
            launch_command.call_args_list,
            [
                call(
                    "203.0.113.10",
                    ["google-chrome", "--remote-debugging-port=1337"],
                ),
                call(
                    "203.0.113.10",
                    [
                        "socat",
                        "tcp-listen:9222,fork,reuseaddr",
                        "tcp:localhost:1337",
                    ],
                ),
            ],
        )

    @patch("scripts.python.smoke_aws_ppt_web_w1._request")
    def test_desktop_readiness_checks_gnome_and_x11(self, request):
        request.return_value = (
            b'{"status":"success","returncode":0,"output":"","error":""}'
        )

        self.assertTrue(_desktop_is_ready("203.0.113.10"))

        body = request.call_args.kwargs["body"]
        payload = json.loads(body.decode("utf-8"))
        self.assertIn("pgrep -x gnome-shell", payload["command"][2])
        self.assertIn("DISPLAY=:0 xdpyinfo", payload["command"][2])

    @patch("scripts.python.smoke_aws_ppt_web_w1._request")
    def test_screenshot_requires_png_magic(self, request):
        request.return_value = b"\x89PNG\r\n\x1a\ncontent"
        _verify_screenshot("203.0.113.10")

        request.return_value = b"<html>not an image</html>"
        with self.assertRaisesRegex(RuntimeError, "not a PNG"):
            _verify_screenshot("203.0.113.10")


if __name__ == "__main__":
    unittest.main()
