#!/usr/bin/env python3
"""
Simple test script for Indian Stock API tools (without CrewAI dependencies)
"""

import sys
import time
import http.client
import json
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
        
        conn.request("GET", url_path, headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        # Parse JSON response
        response_text = data.decode("utf-8")
        return json.loads(response_text)
        
    except http.client.HTTPException as e:
        return {"error": f"Indian Stock API request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse Indian Stock API response"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def print_separator(title):
    """Print a formatted separator with title"""
    print("\n" + "=" * 60)
    print(f" {title} ")
    print("=" * 60)

def test_stock_details(symbol: str):
    """Test stock details endpoint"""
    print(f"🔍 Testing stock details for: {symbol}")
    
    endpoint = "stock"
    params = {"name": symbol.upper()}
    
    data = make_indian_stock_request(endpoint, params)
    
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return False
    
    if not data:
        print(f"❌ No data found for {symbol}")
        return False
    
    print(f"✅ Successfully retrieved data for {symbol}")
    
    # Print the complete raw data to see the actual structure
    print("\n=== COMPLETE RAW DATA ===")
    print(json.dumps(data, indent=2))
    print("=== END RAW DATA ===\n")
    
    return True

def test_trending_stocks():
    """Test trending stocks endpoint"""
    print("🔍 Testing trending stocks...")
    
    data = make_indian_stock_request("trending")
    
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return False
    
    if not data:
        print("❌ No trending data found")
        return False
    
    print("✅ Successfully retrieved trending stocks")
    
    if isinstance(data, list):
        print(f"   Found {len(data)} trending stocks")
        for i, stock in enumerate(data[:5]):  # Show first 5
            if isinstance(stock, dict):
                symbol = stock.get('symbol', 'N/A')
                price = stock.get('price', 'N/A')
                change = stock.get('change_percent', 'N/A')
                print(f"   {i+1}. {symbol}: ₹{price} ({change}%)")
    
    return True

def test_52_week_high_low():
    """Test 52-week high/low endpoint"""
    print("🔍 Testing 52-week high/low data...")
    
    data = make_indian_stock_request("fetch_52_week_high_low_data")
    
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return False
    
    if not data:
        print("❌ No 52-week data found")
        return False
    
    print("✅ Successfully retrieved 52-week data")
    
    if isinstance(data, dict):
        if 'high' in data and isinstance(data['high'], list):
            print(f"   52-Week Highs: {len(data['high'])} stocks")
        if 'low' in data and isinstance(data['low'], list):
            print(f"   52-Week Lows: {len(data['low'])} stocks")
    elif isinstance(data, list):
        print(f"   Found {len(data)} records")
    
    return True

def test_industry_search(query: str):
    """Test industry search endpoint"""
    print(f"🔍 Testing industry search for: {query}")
    
    endpoint = "industry_search"
    params = {"query": query}
    
    data = make_indian_stock_request(endpoint, params)
    
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return False
    
    if not data:
        print(f"❌ No data found for industry: {query}")
        return False
    
    print(f"✅ Successfully retrieved industry data for {query}")
    
    if isinstance(data, list):
        print(f"   Found {len(data)} companies in {query}")
        for i, company in enumerate(data[:3]):  # Show first 3
            if isinstance(company, dict):
                name = company.get('company_name', 'N/A')
                symbol = company.get('symbol', 'N/A')
                print(f"   {i+1}. {name} ({symbol})")
    
    return True

def test_historical_data(symbol: str, period: str = "1Y"):
    """Test historical data endpoint"""
    print(f"🔍 Testing historical data for {symbol} ({period})...")
    
    endpoint = "historical_data"
    params = {"stock_name": symbol.upper(), "period": period}
    
    data = make_indian_stock_request(endpoint, params)
    
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return False
    
    if not data:
        print(f"❌ No historical data found for {symbol}")
        return False
    
    print(f"✅ Successfully retrieved historical data for {symbol}")
    
    if isinstance(data, list):
        print(f"   Found {len(data)} historical records")
        if len(data) > 0 and isinstance(data[0], dict):
            latest = data[-1]  # Most recent
            print(f"   Latest: {latest.get('date', 'N/A')} - Close: ₹{latest.get('close', 'N/A')}")
    
    return True

def run_basic_tests():
    """Run basic API tests"""
    print("🚀 Starting Basic Indian Stock API Tests")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Stock Details
    print_separator("STOCK DETAILS TEST")
    total_tests += 1
    if test_stock_details("RELIANCE"):
        tests_passed += 1
    time.sleep(1)
    
    # Test 2: Trending Stocks
    print_separator("TRENDING STOCKS TEST")
    total_tests += 1
    if test_trending_stocks():
        tests_passed += 1
    time.sleep(1)
    
    # Test 3: 52-Week High/Low
    print_separator("52-WEEK HIGH/LOW TEST")
    total_tests += 1
    if test_52_week_high_low():
        tests_passed += 1
    time.sleep(1)
    
    # Test 4: Industry Search
    print_separator("INDUSTRY SEARCH TEST")
    total_tests += 1
    if test_industry_search("Banking"):
        tests_passed += 1
    time.sleep(1)
    
    # Test 5: Historical Data
    print_separator("HISTORICAL DATA TEST")
    total_tests += 1
    if test_historical_data("TCS", "1M"):
        tests_passed += 1
    
    # Summary
    print_separator("TEST SUMMARY")
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    print(f"⏰ Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API endpoints or connection.")

def test_single_endpoint():
    """Interactive single endpoint testing"""
    while True:
        print_separator("SINGLE ENDPOINT TESTING")
        print("Available endpoints:")
        print("1. Stock Details")
        print("2. Trending Stocks")
        print("3. 52-Week High/Low")
        print("4. Industry Search")
        print("5. Historical Data")
        print("6. Raw API Test")
        print("0. Exit")
        
        choice = input("\nSelect an endpoint to test (0-6): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            symbol = input("Enter stock symbol (e.g., RELIANCE): ").strip()
            if symbol:
                test_stock_details(symbol)
        elif choice == "2":
            test_trending_stocks()
        elif choice == "3":
            test_52_week_high_low()
        elif choice == "4":
            industry = input("Enter industry (e.g., Banking): ").strip()
            if industry:
                test_industry_search(industry)
        elif choice == "5":
            symbol = input("Enter stock symbol (e.g., TCS): ").strip()
            period = input("Enter period (1Y, 6M, 3M, 1M): ").strip() or "1Y"
            if symbol:
                test_historical_data(symbol, period)
        elif choice == "6":
            endpoint = input("Enter endpoint (e.g., trending): ").strip()
            if endpoint:
                print(f"🔍 Testing raw endpoint: {endpoint}")
                result = make_indian_stock_request(endpoint)
                print(f"📊 Result: {json.dumps(result, indent=2)[:500]}...")
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        test_single_endpoint()
    else:
        run_basic_tests()
