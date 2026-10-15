import os
import sys
import asyncio
import threading

import webview
from smartbindb import SmartBinDB


def base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


class BinApi:
    def __init__(self):
        self.db = SmartBinDB()
        self.loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def lookup(self, bin_number):
        try:
            bin_number = ''.join(filter(str.isdigit, str(bin_number)))[:6]
            if len(bin_number) < 6:
                return {"error": "Invalid BIN"}
            future = asyncio.run_coroutine_threadsafe(
                self.db.get_bin_info(bin_number), self.loop
            )
            info = future.result(timeout=10)
            if not info:
                return {"error": "Not found"}
            return {
                "scheme": info.get("scheme") or info.get("brand") or "N/A",
                "type": info.get("type") or info.get("card_type") or "N/A",
                "level": info.get("level") or info.get("category") or "N/A",
                "bank": info.get("bank") or info.get("issuer") or "N/A",
                "country": info.get("country") or info.get("country_name") or "N/A",
                "flag": info.get("flag") or "🌍",
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    api = BinApi()
    ui_file = os.path.join(base_path(), "ui.html")
    webview.create_window(
        title="BIN Checker Pro — Offline",
        url=ui_file,
        js_api=api,
        width=1200,
        height=800,
        min_size=(900, 600),
        resizable=True,
        text_select=True,
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
