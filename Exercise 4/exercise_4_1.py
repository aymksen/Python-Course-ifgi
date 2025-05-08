from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# wrap the expression in single quotes so QGIS will substitute [% "Name" %]
district = '[% "Name" %]'

# make it URL-safe
safe_name = district.replace(' ', '_')
url = QUrl(f"https://en.wikipedia.org/wiki/{safe_name}")

view = QWebView()
view.load(url)
view.show()
