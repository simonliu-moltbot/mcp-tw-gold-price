import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime

GOLD_RATE_URL = "https://rate.bot.com.tw/gold?Lang=en-US"

def fetch_gold_passbook_twd():
    """
    Fetches the current TWD Gold Passbook rates (Buying and Selling per gram).
    Returns a dictionary with 'buying', 'selling', 'currency', 'unit', and 'timestamp'.
    """
    try:
        response = requests.get(GOLD_RATE_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the row containing "Gold Passbook"
        # The structure is complicated, let's look for the cell with text "Gold Passbook"
        # and get siblings.
        
        # Method 1: Find text "Gold Passbook"
        target_cell = soup.find(string=lambda text: "Gold Passbook" in text if text else False)
        if not target_cell:
            return {"error": "Could not find Gold Passbook data on the page."}
        
        row = target_cell.find_parent("tr")
        if not row:
            # Maybe it's inside a span or something, try finding parent td then tr
            td = target_cell.find_parent("td")
            if td:
                row = td.find_parent("tr")
        
        if not row:
             return {"error": "Could not locate the data row."}

        # The columns are: Currency/Unit, Selling, Buying
        # Note: The site might change columns order or responsiveness.
        # But typically: 
        # 1. Name (Gold Passbook)
        # 2. Selling Price (Bank Sells to Customer)
        # 3. Buying Price (Bank Buys from Customer)
        
        cells = row.find_all("td")
        
        # Check data-table attributes if available for robustness
        selling_price = None
        buying_price = None
        
        for cell in cells:
            data_table = cell.get("data-table", "").strip()
            text_val = cell.get_text(strip=True).replace(",", "")
            
            if "Selling" in data_table:
                selling_price = text_val
            elif "Buying" in data_table:
                buying_price = text_val
        
        # Fallback if data-table is missing (sometimes it is)
        if not selling_price or not buying_price:
            # Assume index 1 is Selling, index 2 is Buying based on standard layout
            # Verification needed.
            # Usually: [Name, Selling, Buying]
            if len(cells) >= 3:
                selling_price = cells[1].get_text(strip=True).replace(",", "")
                buying_price = cells[2].get_text(strip=True).replace(",", "")

        # Extract time
        time_element = soup.find("span", class_="time")
        quoted_time = time_element.get_text(strip=True) if time_element else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "unit": "1 Gram",
            "currency": "TWD",
            "selling_price": float(selling_price) if selling_price else None,
            "buying_price": float(buying_price) if buying_price else None,
            "timestamp": quoted_time,
            "source": "Bank of Taiwan"
        }

    except Exception as e:
        sys.stderr.write(f"Error fetching gold price: {e}\n")
        return {"error": str(e)}

def calculate_gold_value(grams: float, rate_type: str = "buying"):
    """
    Calculates the value of a specific amount of gold in TWD.
    rate_type: 'buying' (Bank buys from you) or 'selling' (Bank sells to you).
    """
    data = fetch_gold_passbook_twd()
    if "error" in data:
        return data

    price = data.get(f"{rate_type}_price")
    if price is None:
        return {"error": f"Could not find {rate_type} price."}

    total_value = grams * price
    return {
        "grams": grams,
        "rate_type": rate_type,
        "unit_price": price,
        "total_value_twd": round(total_value, 2),
        "timestamp": data.get("timestamp")
    }

if __name__ == "__main__":
    # Test run
    print(fetch_gold_passbook_twd())
