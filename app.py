import os
import sys
import json
import threading

import webview


# ============================================
# BUILT-IN VERIFIED DATABASE
# ============================================
BUILTIN_DB = {
    "440393": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Sutton Bank", "country": "United States", "flag": "🇺🇸"},
    "447227": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Bank of America", "country": "United States", "flag": "🇺🇸"},
    "400895": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Wells Fargo", "country": "United States", "flag": "🇺🇸"},
    "497040": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Capital One", "country": "United States", "flag": "🇺🇸"},
    "483612": {"scheme": "VISA", "type": "CREDIT", "level": "PLATINUM", "bank": "Wells Fargo", "country": "United States", "flag": "🇺🇸"},
    "403163": {"scheme": "VISA", "type": "CREDIT", "level": "SIGNATURE", "bank": "Chase Bank", "country": "United States", "flag": "🇺🇸"},
    "423223": {"scheme": "VISA", "type": "CREDIT", "level": "PLATINUM", "bank": "Chase Bank", "country": "United States", "flag": "🇺🇸"},
    "498503": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Bank of America", "country": "United States", "flag": "🇺🇸"},
    "414720": {"scheme": "VISA", "type": "CREDIT", "level": "SIGNATURE", "bank": "Chase Bank", "country": "United States", "flag": "🇺🇸"},
    "426398": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Bank of America", "country": "United States", "flag": "🇺🇸"},
    "491183": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Wells Fargo", "country": "United States", "flag": "🇺🇸"},
    "425416": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "PNC Bank", "country": "United States", "flag": "🇺🇸"},
    "453253": {"scheme": "VISA", "type": "CREDIT", "level": "GOLD", "bank": "Citibank", "country": "United States", "flag": "🇺🇸"},
    "473704": {"scheme": "VISA", "type": "CREDIT", "level": "PLATINUM", "bank": "US Bank", "country": "United States", "flag": "🇺🇸"},
    "515597": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "STANDARD", "bank": "Bank of America", "country": "United States", "flag": "🇺🇸"},
    "515678": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "STANDARD", "bank": "Chase Bank", "country": "United States", "flag": "🇺🇸"},
    "531983": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "WORLD", "bank": "Citibank", "country": "United States", "flag": "🇺🇸"},
    "524173": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "GOLD", "bank": "Citibank", "country": "United States", "flag": "🇺🇸"},
    "541275": {"scheme": "MASTERCARD", "type": "DEBIT", "level": "STANDARD", "bank": "Capital One", "country": "United States", "flag": "🇺🇸"},
    "550989": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "STANDARD", "bank": "Bank of America", "country": "United States", "flag": "🇺🇸"},
    "541449": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "STANDARD", "bank": "Citibank", "country": "United States", "flag": "🇺🇸"},
    "515599": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "STANDARD", "bank": "Wells Fargo", "country": "United States", "flag": "🇺🇸"},
    "517148": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "STANDARD", "bank": "Chase Bank", "country": "United States", "flag": "🇺🇸"},
    "536347": {"scheme": "MASTERCARD", "type": "DEBIT", "level": "STANDARD", "bank": "Bank of America", "country": "United States", "flag": "🇺🇸"},
    "515593": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "WORLD", "bank": "Capital One", "country": "United States", "flag": "🇺🇸"},
    "515676": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "WORLD", "bank": "Capital One", "country": "United States", "flag": "🇺🇸"},
    "517805": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "STANDARD", "bank": "Citibank", "country": "United States", "flag": "🇺🇸"},
    "527519": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "STANDARD", "bank": "Bank of America", "country": "United States", "flag": "🇺🇸"},
    "558158": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "WORLD", "bank": "HSBC Bank", "country": "United Kingdom", "flag": "🇬🇧"},
    "552141": {"scheme": "MASTERCARD", "type": "CREDIT", "level": "PLATINUM", "bank": "Barclays Bank", "country": "United Kingdom", "flag": "🇬🇧"},
    "476134": {"scheme": "VISA", "type": "CREDIT", "level": "PLATINUM", "bank": "HSBC Bank", "country": "United Kingdom", "flag": "🇬🇧"},
    "457173": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Danske Bank", "country": "Denmark", "flag": "🇩🇰"},
    "371449": {"scheme": "AMEX", "type": "CREDIT", "level": "GOLD", "bank": "American Express", "country": "United States", "flag": "🇺🇸"},
    "378282": {"scheme": "AMEX", "type": "CREDIT", "level": "PLATINUM", "bank": "American Express", "country": "United States", "flag": "🇺🇸"},
    "601100": {"scheme": "DISCOVER", "type": "CREDIT", "level": "STANDARD", "bank": "Discover Bank", "country": "United States", "flag": "🇺🇸"},
    "601109": {"scheme": "DISCOVER", "type": "CREDIT", "level": "PLATINUM", "bank": "Discover Bank", "country": "United States", "flag": "🇺🇸"},
    "353011": {"scheme": "JCB", "type": "CREDIT", "level": "STANDARD", "bank": "JCB Bank", "country": "Japan", "flag": "🇯🇵"},
    "402420": {"scheme": "VISA", "type": "CREDIT", "level": "PLATINUM", "bank": "Scotiabank", "country": "Canada", "flag": "🇨🇦"},
    "450803": {"scheme": "VISA", "type": "DEBIT", "level": "CLASSIC", "bank": "Commonwealth Bank", "country": "Australia", "flag": "🇦🇺"},
}


# ============================================
# DETECT NETWORK from BIN pattern (fallback)
# ============================================
def detect_network(bin_number):
    try:
        first = int(bin_number[0])
        first2 = int(bin_number[:2])
        first4 = int(bin_number[:4])

        if first == 4:
            return "VISA"
        if 51 <= first2 <= 55:
            return "MASTERCARD"
        if 2221 <= first4 <= 2720:
            return "MASTERCARD"
        if first2 in (34, 37):
            return "AMEX"
        if first4 == 6011 or first2 == 65:
            return "DISCOVER"
        if first2 == 35:
            return "JCB"
        if first2 in (36, 38, 39):
            return "DINERS"
    except Exception:
        pass
    return "UNKNOWN"


# ============================================
# SMARTBINDB WRAPPER (safe)
# ============================================
class SmartDB:
    def __init__(self):
        self.db = None
        self.available = False
        self.error = None
        self._init()

    def _init(self):
        try:
            from smartbindb import SmartBinDB
            self.db = SmartBinDB()
            self.available = True
        except Exception as e:
            self.error = str(e)
            self.available = False

    def lookup(self, bin_number):
        """Sync wrapper around async SmartBinDB"""
        if not self.available:
            return None
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(self.db.get_bin_info(bin_number))
            finally:
                loop.close()
            return result
        except Exception as e:
            self.error = str(e)
            return None


# ============================================
# API exposed to JavaScript
# ============================================
class BinApi:
    def __init__(self):
        self.smart = SmartDB()

    def get_status(self):
        """Return DB status for debugging"""
        return {
            "smartbindb_available": self.smart.available,
            "smartbindb_error": self.smart.error,
            "builtin_count": len(BUILTIN_DB),
        }

    def lookup(self, bin_number):
        try:
            # Normalize
            digits = ''.join(filter(str.isdigit, str(bin_number)))
            if len(digits) < 6:
                return {"error": "Invalid BIN (need at least 6 digits)"}

            bin6 = digits[:6]

            # 1) Try SmartBinDB first
            if self.smart.available:
                info = self.smart.lookup(bin6)
                if info:
                    return {
                        "scheme": (info.get("scheme") or info.get("brand") or "UNKNOWN").upper(),
                        "type": (info.get("type") or info.get("card_type") or "UNKNOWN").upper(),
                        "level": info.get("level") or info.get("category") or "STANDARD",
                        "bank": info.get("bank") or info.get("issuer") or "Unknown Bank",
                        "country": info.get("country") or info.get("country_name") or "Unknown",
                        "flag": info.get("flag") or "🌍",
                    }

            # 2) Built-in verified DB
            if bin6 in BUILTIN_DB:
                return BUILTIN_DB[bin6]

            # 3) Partial match on 6-digit prefix
            for k, v in BUILTIN_DB.items():
                if k.startswith(bin6):
                    return v

            # 4) At least detect network from pattern
            network = detect_network(bin6)
            if network != "UNKNOWN":
                return {
                    "scheme": network,
                    "type": "UNKNOWN",
                    "level": "STANDARD",
                    "bank": "Not in offline DB",
                    "country": "Unknown",
                    "flag": "🌍",
                }

            return {"error": "BIN not found in offline database"}

        except Exception as e:
            return {"error": f"Error: {str(e)}"}


# ============================================
# Path helper
# ============================================
def base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


# ============================================
# Main
# ============================================
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
