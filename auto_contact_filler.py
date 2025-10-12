import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

# --- Config ---
EXCEL_FILE = 'corporate_list.xlsx'
IMPLICIT_WAIT = 10 # seconds

FIELD_MAP = {
    # Excel Column Name: [ (By method, selector value), ... ]
    '企業名': [
        (By.CSS_SELECTOR, "input[name*='company'], input[id*='company']"),
        (By.CSS_SELECTOR, "input[name*='kaisha'], input[placeholder*='会社名']"),
    ],
    '担当者名': [
        (By.CSS_SELECTOR, "input[name*='name'], input[id*='name']"),
        (By.CSS_SELECTOR, "input[placeholder*='氏名'], input[name*='shimei']"),
    ],
    'メールアドレス': [
        (By.CSS_SELECTOR, "input[type='email'], input[name*='mail'], input[id*='mail']"),
        (By.CSS_SELECTOR, "input[placeholder*='メール']"),
    ],
    '送信メッセージ': [
        (By.TAG_NAME, "textarea"),
        (By.CSS_SELECTOR, "textarea[name*='message'], textarea[id*='body']"),
    ]
}

REQUIRED_COLS = ['URL', '企業名', '担当者名', 'メールアドレス', '送信メッセージ']

# --- Helper Functions ---

def find_and_send_keys(driver, column_name, value):
    """Attempt to find element by defined selectors and send keys."""
    for by, selector in FIELD_MAP.get(column_name, []):
        try:
            element = driver.find_element(by, selector)
            element.clear()
            element.send_keys(value)
            return True
        except NoSuchElementException:
            continue
        except Exception:
            return False # Stop trying on unexpected element errors

    print(f"  [WARN] Field '{column_name}' not identified.")
    return False

def setup_driver():
    """Initializes and returns the WebDriver without manual path configuration."""
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Uncomment for silent mode
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver

# --- Main Logic ---

def main():
    # 1. Load Data
    try:
        df = pd.read_excel(EXCEL_FILE)
        if not all(col in df.columns for col in REQUIRED_COLS):
            raise ValueError(f"Missing required columns in Excel: {', '.join(REQUIRED_COLS)}")
        if '入力結果' not in df.columns:
            df['入力結果'] = ""

    except FileNotFoundError:
        print(f"[ERROR] Excel file '{EXCEL_FILE}' not found.")
        return
    except Exception as e:
        print(f"[ERROR] Data loading failed: {e}")
        return

    # 2. Setup WebDriver
    try:
        driver = setup_driver()
    except Exception as e:
        print(f"[FATAL] WebDriver setup failed. Is Chrome installed? Detail: {e}")
        return

    # 3. Processing Loop
    try:
        for index, row in df.iterrows():
            url = row['URL']
            print(f"\n--- {index + 1}/{len(df)}: START -> {url} ---")

            try:
                # Check for prior success to enable resume functionality
                if str(row.get('入力結果')) in ('成功', '成功（CAPTCHAあり）'):
                    print("  [SKIP] Already processed successfully.")
                    continue
                
                driver.get(url)
                time.sleep(2) # Allow initial load

                # Input all fields and count successful fills
                successful_fills = sum(find_and_send_keys(driver, col, row[col]) for col in REQUIRED_COLS[1:])

                if successful_fills < len(REQUIRED_COLS) - 1:
                    df.loc[index, '入力結果'] = f"FAIL: {len(REQUIRED_COLS) - 1 - successful_fills} fields unidentified"
                    continue
                
                # Check for CAPTCHA presence
                try:
                    # Look for common reCAPTCHA iframe
                    driver.find_element(By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]")
                    df.loc[index, '入力結果'] = "成功（CAPTCHAあり）"
                    print("  [INFO] Input complete. CAPTCHA detected. Manual check required.")
                except NoSuchElementException:
                    df.loc[index, '入力結果'] = "成功"
                    print("  [INFO] Input complete. Ready for manual review/submission.")

                # Pause execution for manual review
                input("  [ACTION] Hit ENTER in console after manual review/submission...")
            
            except WebDriverException as e:
                df.loc[index, '入力結果'] = f"FAIL: Site/Timeout ({e.__class__.__name__})"
                print(f"  [ERROR] WebDriver Error: {e.__class__.__name__}")
            except Exception as e:
                df.loc[index, '入力結果'] = f"FAIL: Unexpected ({e.__class__.__name__})"
                print(f"  [ERROR] Unexpected Error: {e.__class__.__name__}")
    
    finally:
        # 4. Finalize
        if 'driver' in locals():
            driver.quit()

        try:
            df.to_excel(EXCEL_FILE, index=False)
            print(f"\n[DONE] Results saved to {EXCEL_FILE}")
        except Exception as e:
            print(f"[FATAL] Failed to write Excel results. Close the file if open. Detail: {e}")

if __name__ == "__main__":
    main()