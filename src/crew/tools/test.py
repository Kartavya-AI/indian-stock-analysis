#!/usr/bin/env python3
"""
Test script for Indian Stock API tools
"""

import sys
import time
from nse_tools import (
    get_stock_details,
    get_industry_search,
    get_mutual_fund_search,
    get_stock_target_price,
    get_trending_stocks,
    get_52_week_high_low,
    get_historical_data,
    make_indian_stock_request
)

def print_separator(title):
    """Print a formatted separator with title"""
    print("\n" + "=" * 60)
    print(f" {title} ")
    print("=" * 60)

def test_api_connection():
    """Test basic API connection"""
    print_separator("TESTING API CONNECTION")
    try:
        response = make_indian_stock_request("trending")
        if "error" in response:
            print(f"❌ API Connection Failed: {response['error']}")
            return False
        else:
            print("✅ API Connection Successful")
            return True
    except Exception as e:
        print(f"❌ API Connection Error: {str(e)}")
        return False

def test_stock_details():
    """Test stock details endpoint"""
    print_separator("TESTING STOCK DETAILS")
    
    test_symbols = ["RELIANCE", "TCS", "INFY", "HDFC", "INVALID_SYMBOL"]
    
    for symbol in test_symbols:
        print(f"\n🔍 Testing symbol: {symbol}")
        try:
            result = get_stock_details(symbol)
            if "Error" in result:
                print(f"❌ {symbol}: {result[:100]}...")
            else:
                print(f"✅ {symbol}: Data retrieved successfully")
                # Print first few lines for verification
                lines = result.split('\n')[:5]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
        except Exception as e:
            print(f"❌ {symbol}: Exception - {str(e)}")
        
        time.sleep(1)  # Rate limiting

def test_industry_search():
    """Test industry search endpoint"""
    print_separator("TESTING INDUSTRY SEARCH")
    
    test_industries = ["Banking", "IT", "Pharma", "Auto", "Steel"]
    
    for industry in test_industries:
        print(f"\n🔍 Testing industry: {industry}")
        try:
            result = get_industry_search(industry)
            if "Error" in result:
                print(f"❌ {industry}: {result[:100]}...")
            else:
                print(f"✅ {industry}: Data retrieved successfully")
                # Print first few lines
                lines = result.split('\n')[:3]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
        except Exception as e:
            print(f"❌ {industry}: Exception - {str(e)}")
        
        time.sleep(1)

def test_mutual_fund_search():
    """Test mutual fund search endpoint"""
    print_separator("TESTING MUTUAL FUND SEARCH")
    
    test_funds = ["HDFC", "SBI", "ICICI", "Axis", "Equity"]
    
    for fund in test_funds:
        print(f"\n🔍 Testing mutual fund: {fund}")
        try:
            result = get_mutual_fund_search(fund)
            if "Error" in result:
                print(f"❌ {fund}: {result[:100]}...")
            else:
                print(f"✅ {fund}: Data retrieved successfully")
                # Print first few lines
                lines = result.split('\n')[:3]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
        except Exception as e:
            print(f"❌ {fund}: Exception - {str(e)}")
        
        time.sleep(1)

def test_stock_target_price():
    """Test stock target price endpoint"""
    print_separator("TESTING STOCK TARGET PRICE")
    
    test_stock_ids = ["1", "2", "3", "RELIANCE", "TCS"]
    
    for stock_id in test_stock_ids:
        print(f"\n🔍 Testing stock ID: {stock_id}")
        try:
            result = get_stock_target_price(stock_id)
            if "Error" in result:
                print(f"❌ {stock_id}: {result[:100]}...")
            else:
                print(f"✅ {stock_id}: Data retrieved successfully")
                # Print first few lines
                lines = result.split('\n')[:3]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
        except Exception as e:
            print(f"❌ {stock_id}: Exception - {str(e)}")
        
        time.sleep(1)

def test_trending_stocks():
    """Test trending stocks endpoint"""
    print_separator("TESTING TRENDING STOCKS")
    
    try:
        print("🔍 Fetching trending stocks...")
        result = get_trending_stocks()
        if "Error" in result:
            print(f"❌ Trending stocks: {result[:100]}...")
        else:
            print("✅ Trending stocks: Data retrieved successfully")
            # Print first few lines
            lines = result.split('\n')[:10]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    except Exception as e:
        print(f"❌ Trending stocks: Exception - {str(e)}")

def test_52_week_high_low():
    """Test 52-week high/low endpoint"""
    print_separator("TESTING 52-WEEK HIGH/LOW")
    
    try:
        print("🔍 Fetching 52-week high/low data...")
        result = get_52_week_high_low()
        if "Error" in result:
            print(f"❌ 52-week data: {result[:100]}...")
        else:
            print("✅ 52-week data: Data retrieved successfully")
            # Print first few lines
            lines = result.split('\n')[:10]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    except Exception as e:
        print(f"❌ 52-week data: Exception - {str(e)}")

def test_historical_data():
    """Test historical data endpoint"""
    print_separator("TESTING HISTORICAL DATA")
    
    test_cases = [
        ("RELIANCE", "1Y"),
        ("TCS", "6M"),
        ("INFY", "3M"),
        ("HDFC", "1M")
    ]
    
    for symbol, period in test_cases:
        print(f"\n🔍 Testing {symbol} for {period}")
        try:
            result = get_historical_data(symbol, period)
            if "Error" in result:
                print(f"❌ {symbol} ({period}): {result[:100]}...")
            else:
                print(f"✅ {symbol} ({period}): Data retrieved successfully")
                # Print first few lines
                lines = result.split('\n')[:5]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
        except Exception as e:
            print(f"❌ {symbol} ({period}): Exception - {str(e)}")
        
        time.sleep(1)

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Indian Stock API Tools Test Suite")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test API connection first
    if not test_api_connection():
        print("\n❌ API connection failed. Stopping tests.")
        return
    
    # Run all tests
    test_stock_details()
    test_industry_search()
    test_mutual_fund_search()
    test_stock_target_price()
    test_trending_stocks()
    test_52_week_high_low()
    test_historical_data()
    
    print_separator("TEST SUMMARY")
    print("✅ All tests completed!")
    print("📊 Check the results above for any failures")
    print(f"⏰ Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

def test_individual_tool():
    """Interactive mode to test individual tools"""
    while True:
        print_separator("INDIVIDUAL TOOL TESTING")
        print("Available tools:")
        print("1. Stock Details")
        print("2. Industry Search")
        print("3. Mutual Fund Search")
        print("4. Stock Target Price")
        print("5. Trending Stocks")
        print("6. 52-Week High/Low")
        print("7. Historical Data")
        print("8. Run All Tests")
        print("0. Exit")
        
        choice = input("\nSelect a tool to test (0-8): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            symbol = input("Enter stock symbol (e.g., RELIANCE): ").strip()
            if symbol:
                print(get_stock_details(symbol))
        elif choice == "2":
            industry = input("Enter industry (e.g., Banking): ").strip()
            if industry:
                print(get_industry_search(industry))
        elif choice == "3":
            fund = input("Enter mutual fund search term (e.g., HDFC): ").strip()
            if fund:
                print(get_mutual_fund_search(fund))
        elif choice == "4":
            stock_id = input("Enter stock ID: ").strip()
            if stock_id:
                print(get_stock_target_price(stock_id))
        elif choice == "5":
            print(get_trending_stocks())
        elif choice == "6":
            print(get_52_week_high_low())
        elif choice == "7":
            symbol = input("Enter stock symbol (e.g., RELIANCE): ").strip()
            period = input("Enter period (1Y, 6M, 3M, 1M): ").strip() or "1Y"
            if symbol:
                print(get_historical_data(symbol, period))
        elif choice == "8":
            run_all_tests()
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        test_individual_tool()
    else:
        run_all_tests()
