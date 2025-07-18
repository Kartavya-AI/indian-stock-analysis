#!/usr/bin/env python3
"""
Script to save raw API responses from Indian Stock API to JSON files
"""

import http.client
import json
import os
import time
from urllib.parse import urlencode

def make_indian_stock_request(endpoint: str, params: dict = None) -> dict:
    """Make API request to Indian Stock API"""
    if params is None:
        params = {}
    
    try:
        conn = http.client.HTTPSConnection("stock.indianapi.in")
        headers = { 'X-Api-Key': "sk-live-efd6p1wyz4wDUWtKAGLzn4diji8ObRXgPC4d05Ir" }
        
        # Build the URL with query parameters
        url_path = f"/{endpoint}"
        if params:
            url_path += f"?{urlencode(params)}"
        
        print(f"🔍 Requesting: {url_path}")
        
        conn.request("GET", url_path, headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        # Parse JSON response
        response_text = data.decode("utf-8")
        return json.loads(response_text)
        
    except http.client.HTTPException as e:
        return {"error": f"HTTP Error: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON Decode Error: {str(e)}", "raw_response": response_text}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def save_api_response(endpoint_name: str, data: dict, params: dict = None):
    """Save API response to JSON file"""
    # Create api_responses directory if it doesn't exist
    os.makedirs("api_responses", exist_ok=True)
    
    # Create filename
    if params:
        param_str = "_".join([f"{k}-{v}" for k, v in params.items()])
        filename = f"api_responses/{endpoint_name}_{param_str}.json"
    else:
        filename = f"api_responses/{endpoint_name}.json"
    
    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved response to: {filename}")

def collect_all_api_responses():
    """Collect and save responses from all API endpoints"""
    print("🚀 Starting to collect all API responses...")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Stock Details - Test with multiple symbols
    print("\n" + "="*50)
    print("📊 COLLECTING STOCK DETAILS")
    print("="*50)
    
    stock_symbols = ["RELIANCE", "TCS", "INFY", "HDFC", "ITC"]
    for symbol in stock_symbols:
        print(f"\n🔍 Getting stock details for: {symbol}")
        params = {"name": symbol}
        data = make_indian_stock_request("stock", params)
        save_api_response("stock_details", data, {"symbol": symbol})
        time.sleep(1)
    
    # 2. Industry Search
    print("\n" + "="*50)
    print("🏭 COLLECTING INDUSTRY SEARCH")
    print("="*50)
    
    industries = ["Banking", "IT", "Pharma", "Auto", "Steel"]
    for industry in industries:
        print(f"\n🔍 Getting industry search for: {industry}")
        params = {"query": industry}
        data = make_indian_stock_request("industry_search", params)
        save_api_response("industry_search", data, {"query": industry})
        time.sleep(1)
    
    # 3. Mutual Fund Search
    print("\n" + "="*50)
    print("💰 COLLECTING MUTUAL FUND SEARCH")
    print("="*50)
    
    fund_queries = ["HDFC", "SBI", "ICICI", "Axis", "Equity"]
    for query in fund_queries:
        print(f"\n🔍 Getting mutual fund search for: {query}")
        params = {"query": query}
        data = make_indian_stock_request("mutual_fund_search", params)
        save_api_response("mutual_fund_search", data, {"query": query})
        time.sleep(1)
    
    # 4. Stock Target Price
    print("\n" + "="*50)
    print("🎯 COLLECTING STOCK TARGET PRICE")
    print("="*50)
    
    stock_ids = ["1", "2", "3", "RELIANCE", "TCS"]
    for stock_id in stock_ids:
        print(f"\n🔍 Getting target price for stock ID: {stock_id}")
        params = {"stock_id": stock_id}
        data = make_indian_stock_request("stock_target_price", params)
        save_api_response("stock_target_price", data, {"stock_id": stock_id})
        time.sleep(1)
    
    # 5. Trending Stocks
    print("\n" + "="*50)
    print("📈 COLLECTING TRENDING STOCKS")
    print("="*50)
    
    print("\n🔍 Getting trending stocks...")
    data = make_indian_stock_request("trending")
    save_api_response("trending_stocks", data)
    time.sleep(1)
    
    # 6. 52-Week High/Low
    print("\n" + "="*50)
    print("📊 COLLECTING 52-WEEK HIGH/LOW")
    print("="*50)
    
    print("\n🔍 Getting 52-week high/low data...")
    data = make_indian_stock_request("fetch_52_week_high_low_data")
    save_api_response("52_week_high_low", data)
    time.sleep(1)
    
    # 7. Historical Data
    print("\n" + "="*50)
    print("📉 COLLECTING HISTORICAL DATA")
    print("="*50)
    
    historical_tests = [
        ("RELIANCE", "1Y"),
        ("TCS", "6M"),
        ("INFY", "3M"),
        ("HDFC", "1M")
    ]
    
    for symbol, period in historical_tests:
        print(f"\n🔍 Getting historical data for: {symbol} ({period})")
        params = {"stock_name": symbol, "period": period}
        data = make_indian_stock_request("historical_data", params)
        save_api_response("historical_data", data, {"symbol": symbol, "period": period})
        time.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    print("✅ API RESPONSE COLLECTION COMPLETE!")
    print("="*60)
    print(f"⏰ Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("📁 All responses saved in 'api_responses' directory")
    print("📊 You can now examine the JSON files to see the exact data structure")

def test_single_endpoint():
    """Test a single endpoint and save response"""
    print("🔍 Single Endpoint Testing")
    
    endpoint = input("Enter endpoint (e.g., stock, trending): ").strip()
    if not endpoint:
        print("❌ No endpoint provided")
        return
    
    # Get parameters if needed
    params = {}
    while True:
        param_name = input("Enter parameter name (or press Enter to finish): ").strip()
        if not param_name:
            break
        param_value = input(f"Enter value for {param_name}: ").strip()
        if param_value:
            params[param_name] = param_value
    
    print(f"\n🚀 Testing endpoint: {endpoint}")
    if params:
        print(f"📋 Parameters: {params}")
    
    data = make_indian_stock_request(endpoint, params if params else None)
    
    # Save response
    save_api_response(f"manual_{endpoint}", data, params if params else None)
    
    # Display response
    print("\n📊 Response:")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        test_single_endpoint()
    else:
        collect_all_api_responses()
