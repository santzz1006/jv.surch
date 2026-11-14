"""One-shot companion to the current collection; exits after its final translation."""
import json
import time
import urllib.request
import translate_catalog

while True:
    translate_catalog.run()
    try:
        with urllib.request.urlopen('http://127.0.0.1:8081/api/catalog',timeout=10) as response:
            active=json.load(response)['collection']['running']
    except OSError:
        active=False
    if not active:
        # A last pass includes pages completed during the translation batch.
        translate_catalog.run()
        break
    time.sleep(5)
