import http.client
import json
from typing import Dict, List, Optional
import os
from urllib.parse import urlencode

# Try to import CrewAI tool decorator, fallback if not available
try:
    from crewai.tools import tool
except ImportError:
    # Fallback decorator for testing without CrewAI
    def tool(func):
        """Fallback tool decorator for testing"""
        func.is_tool = True
        return func

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback for pydantic if not available
    BaseModel = object
    Field = lambda **kwargs: None


# Indian Stock API Helper Functions
def make_indian_stock_request(endpoint: str, params: Dict = None) -> Dict:
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


# 1. Stock Details
@tool
def get_stock_details(symbol: str) -> str:
    """
    Get comprehensive stock details from Indian Stock API.
    
    Args:
        symbol: Stock symbol (e.g., RELIANCE, TCS, INFY)
    
    Returns:
        Detailed stock information including price, company info, financials, peer comparison, and key executives.
    """
    # sample_input = "{\"symbol\": \"TCS\"}"
    endpoint = "stock"
    print(symbol)
    params = {"name": symbol.upper()}
    
    data = make_indian_stock_request(endpoint, params)
    
    if "error" in data:
        return f"Error fetching stock data for {symbol}: {data['error']}"
    
    if not data:
        return f"No stock data found for {symbol.upper()}"
    
    try:
        result = f"📈 COMPREHENSIVE STOCK ANALYSIS: {symbol.upper()}\n"
        result += "=" * 60 + "\n\n"
        
        if isinstance(data, dict):
            # 🏢 COMPANY OVERVIEW
            result += "🏢 COMPANY OVERVIEW\n"
            result += "-" * 30 + "\n"
            result += f"Company Name: {data.get('companyName', 'N/A')}\n"
            result += f"Industry: {data.get('industry', 'N/A')}\n"
            
            company_profile = data.get('companyProfile', {})
            if isinstance(company_profile, dict):
                result += f"BSE Code: {company_profile.get('exchangeCodeBse', 'N/A')}\n"
                result += f"NSE Code: {company_profile.get('exchangeCodeNse', 'N/A')}\n"
                result += f"ISIN: {company_profile.get('isInId', 'N/A')}\n"
                
                # Company description (first 300 chars for better context)
                description = company_profile.get('companyDescription', '')
                if description:
                    result += f"Description: {description[:300]}...\n"
            
            # 💰 CURRENT MARKET DATA
            result += "\n💰 CURRENT MARKET DATA\n"
            result += "-" * 30 + "\n"
            current_price = data.get('currentPrice', {})
            if isinstance(current_price, dict):
                bse_price = current_price.get('BSE', 'N/A')
                nse_price = current_price.get('NSE', 'N/A')
                result += f"BSE Price: ₹{bse_price}\n"
                result += f"NSE Price: ₹{nse_price}\n"
            
            percent_change = data.get('percentChange', 'N/A')
            year_high = data.get('yearHigh', 'N/A')
            year_low = data.get('yearLow', 'N/A')
            result += f"Today's Change: {percent_change}%\n"
            result += f"52 Week High: ₹{year_high}\n"
            result += f"52 Week Low: ₹{year_low}\n"
            
            # 📊 TECHNICAL ANALYSIS
            stock_technical_data = data.get('stockTechnicalData', [])
            if isinstance(stock_technical_data, list) and stock_technical_data:
                result += "\n📊 TECHNICAL ANALYSIS (Moving Averages)\n"
                result += "-" * 30 + "\n"
                for tech_data in stock_technical_data:
                    if isinstance(tech_data, dict):
                        days = tech_data.get('days', 'N/A')
                        nse_price = tech_data.get('nsePrice', 'N/A')
                        result += f"  MA {days} Days: ₹{nse_price}\n"
            
            # 👥 KEY EXECUTIVES
            if isinstance(company_profile, dict):
                officers = company_profile.get('officers', {}).get('officer', [])
                if isinstance(officers, list) and officers:
                    result += "\n👥 KEY EXECUTIVES\n"
                    result += "-" * 30 + "\n"
                    for officer in officers[:5]:  # Top 5 executives
                        if isinstance(officer, dict):
                            first_name = officer.get('firstName', '')
                            last_name = officer.get('lastName', '')
                            title_info = officer.get('title', {})
                            if isinstance(title_info, dict):
                                title = title_info.get('Value', 'N/A')
                            else:
                                title = 'N/A'
                            result += f"  • {first_name} {last_name} - {title}\n"
            
            # 🏭 PEER COMPARISON
            if isinstance(company_profile, dict):
                peer_companies = company_profile.get('peerCompanyList', [])
                if isinstance(peer_companies, list) and peer_companies:
                    result += "\n🏭 PEER COMPARISON\n"
                    result += "-" * 30 + "\n"
                    for i, peer in enumerate(peer_companies):
                        if isinstance(peer, dict):
                            name = peer.get('companyName', 'N/A')
                            price = peer.get('price', 'N/A')
                            change = peer.get('percentChange', 'N/A')
                            market_cap = peer.get('marketCap', 'N/A')
                            pe_ratio = peer.get('priceToEarningsValueRatio', 'N/A')
                            result += f"  {i+1}. {name}\n"
                            result += f"     Price: ₹{price} ({change}%)\n"
                            result += f"     Market Cap: ₹{market_cap} Cr | P/E: {pe_ratio}\n"
                            result += "\n"
            
            # 📈 FINANCIAL HIGHLIGHTS
            financials = data.get('financials', [])
            if isinstance(financials, list) and financials:
                result += "\n📈 FINANCIAL HIGHLIGHTS\n"
                result += "-" * 30 + "\n"
                
                for i, financial_year in enumerate(financials[:3]):  # Last 3 years
                    if isinstance(financial_year, dict):
                        fiscal_year = financial_year.get('FiscalYear', 'N/A')
                        result += f"\nFiscal Year {fiscal_year}:\n"
                        
                        # Income statement highlights
                        inc_data = financial_year.get('stockFinancialMap', {}).get('INC', [])
                        if isinstance(inc_data, list):
                            for item in inc_data:
                                if isinstance(item, dict):
                                    key = item.get('key', '')
                                    display_name = item.get('displayName', '')
                                    value = item.get('value', '')
                                    
                                    # Key financial metrics
                                    if key in ['TotalRevenue', 'NetIncome', 'DilutedNormalizedEPS', 'OperatingIncome']:
                                        if value and value != 'N/A':
                                            if key == 'DilutedNormalizedEPS':
                                                result += f"  {display_name}: ₹{value}\n"
                                            else:
                                                result += f"  {display_name}: ₹{value} Cr\n"
                        
                        # Balance sheet highlights
                        bal_data = financial_year.get('stockFinancialMap', {}).get('BAL', [])
                        if isinstance(bal_data, list):
                            for item in bal_data:
                                if isinstance(item, dict):
                                    key = item.get('key', '')
                                    display_name = item.get('displayName', '')
                                    value = item.get('value', '')
                                    
                                    if key in ['TotalAssets', 'TotalEquity', 'TotalDebt']:
                                        if value and value != 'N/A':
                                            result += f"  {display_name}: ₹{value} Cr\n"
                        
                        if i < 2:  # Add separator except for last year
                            result += "  " + "-" * 25 + "\n"
        
        result += "\n" + "=" * 60
        return result
        
    except Exception as e:
        return f"Error parsing stock data: {str(e)}"


# 2. Industry Search
@tool
def get_industry_search(query: str) -> str:
    """
    Search for stocks by industry from Indian Stock API.
    
    Args:
        query: Industry name to search for (e.g., "Banking", "IT", "Pharma")
    
    Returns:
        Comprehensive list of stocks in the specified industry with trading recommendations.
    """
    endpoint = "industry_search"
    params = {"query": query}
    
    data = make_indian_stock_request(endpoint, params)
    
    if "error" in data:
        return f"Error fetching industry data for {query}: {data['error']}"
    
    if not data:
        return f"No industry data found for {query}"
    
    try:
        result = f"🔍 INDUSTRY SEARCH RESULTS: '{query.upper()}'\n"
        result += "=" * 60 + "\n\n"
        
        if isinstance(data, list):
            # Group stocks by rating for better organization
            bullish_stocks = []
            neutral_stocks = []
            bearish_stocks = []
            na_stocks = []
            
            for stock in data:
                if isinstance(stock, dict):
                    trends = stock.get('activeStockTrends', {})
                    if isinstance(trends, dict):
                        overall_rating = trends.get('overallRating', 'N/A')
                        if overall_rating and 'Bullish' in str(overall_rating):
                            bullish_stocks.append(stock)
                        elif overall_rating and 'Bearish' in str(overall_rating):
                            bearish_stocks.append(stock)
                        elif overall_rating and overall_rating not in ['N/A', None, 'NA']:
                            neutral_stocks.append(stock)
                        else:
                            na_stocks.append(stock)
            
            # Display bullish stocks first
            if bullish_stocks:
                result += "🟢 BULLISH RECOMMENDATIONS\n"
                result += "-" * 30 + "\n"
                for i, stock in enumerate(bullish_stocks[:8]):  # Top 8 bullish
                    result += _format_industry_stock(stock, i + 1)
                result += "\n"
            
            # Display neutral stocks
            if neutral_stocks:
                result += "🟡 NEUTRAL RECOMMENDATIONS\n"
                result += "-" * 30 + "\n"
                for i, stock in enumerate(neutral_stocks[:5]):  # Top 5 neutral
                    result += _format_industry_stock(stock, i + 1)
                result += "\n"
            
            # Display bearish stocks
            if bearish_stocks:
                result += "🔴 BEARISH RECOMMENDATIONS\n"
                result += "-" * 30 + "\n"
                for i, stock in enumerate(bearish_stocks[:5]):  # Top 5 bearish
                    result += _format_industry_stock(stock, i + 1)
                result += "\n"
            
            # Summary statistics
            total_stocks = len(data)
            result += f"📊 SUMMARY STATISTICS\n"
            result += "-" * 30 + "\n"
            result += f"Total Stocks Found: {total_stocks}\n"
            result += f"Bullish Recommendations: {len(bullish_stocks)}\n"
            result += f"Neutral Recommendations: {len(neutral_stocks)}\n"
            result += f"Bearish Recommendations: {len(bearish_stocks)}\n"
            result += f"No Rating Available: {len(na_stocks)}\n"
        
        result += "\n" + "=" * 60
        return result
        
    except Exception as e:
        return f"Error parsing industry data: {str(e)}"


def _format_industry_stock(stock: dict, index: int) -> str:
    """Helper function to format individual stock information"""
    if not isinstance(stock, dict):
        return ""
    
    result = f"{index}. {stock.get('commonName', 'N/A')}\n"
    result += f"   NSE: {stock.get('exchangeCodeNsi', 'N/A')} | BSE: {stock.get('exchangeCodeBse', 'N/A')}\n"
    result += f"   Industry: {stock.get('mgIndustry', 'N/A')}\n"
    result += f"   Sector: {stock.get('mgSector', 'N/A')}\n"
    
    # Trading trends
    trends = stock.get('activeStockTrends', {})
    if isinstance(trends, dict):
        short_term = trends.get('shortTermTrends', 'N/A')
        long_term = trends.get('longTermTrends', 'N/A')
        overall = trends.get('overallRating', 'N/A')
        result += f"   Trends: Short-term: {short_term} | Long-term: {long_term}\n"
        result += f"   Overall Rating: {overall}\n"
    
    result += "   " + "-" * 40 + "\n"
    return result


# 3. Mutual Fund Search
@tool
def get_mutual_fund_search(query: str) -> str:
    """
    Search for mutual funds from Indian Stock API.
    
    Args:
        query: Mutual fund name or type to search for (e.g., "Equity", "Debt", "Hybrid", "SBI", "HDFC")
    
    Returns:
        Comprehensive list of mutual funds organized by category and plan type.
    """
    endpoint = "mutual_fund_search"
    params = {"query": query}
    
    data = make_indian_stock_request(endpoint, params)
    
    if "error" in data:
        return f"Error fetching mutual fund data for {query}: {data['error']}"
    
    if not data:
        return f"No mutual fund data found for {query}"
    
    try:
        result = f"💰 MUTUAL FUND SEARCH RESULTS: '{query.upper()}'\n"
        result += "=" * 60 + "\n\n"
        
        if isinstance(data, list):
            # Group funds by category and plan type
            direct_growth_funds = []
            direct_dividend_funds = []
            regular_growth_funds = []
            regular_dividend_funds = []
            other_funds = []
            
            for fund in data:
                if isinstance(fund, dict):
                    scheme_name = fund.get('schemeName', '').lower()
                    
                    if 'direct' in scheme_name and 'growth' in scheme_name:
                        direct_growth_funds.append(fund)
                    elif 'direct' in scheme_name and ('dividend' in scheme_name or 'payout' in scheme_name):
                        direct_dividend_funds.append(fund)
                    elif 'regular' in scheme_name and 'growth' in scheme_name:
                        regular_growth_funds.append(fund)
                    elif 'regular' in scheme_name and ('dividend' in scheme_name or 'payout' in scheme_name):
                        regular_dividend_funds.append(fund)
                    else:
                        other_funds.append(fund)
            
            # Display Direct Growth Plans first (most popular)
            if direct_growth_funds:
                result += "🎯 DIRECT GROWTH PLANS (Recommended)\n"
                result += "-" * 30 + "\n"
                for i, fund in enumerate(direct_growth_funds[:10]):  # Top 10
                    result += _format_mutual_fund(fund, i + 1)
                result += "\n"
            
            # Display Regular Growth Plans
            if regular_growth_funds:
                result += "📈 REGULAR GROWTH PLANS\n"
                result += "-" * 30 + "\n"
                for i, fund in enumerate(regular_growth_funds[:8]):  # Top 8
                    result += _format_mutual_fund(fund, i + 1)
                result += "\n"
            
            # Display Direct Dividend Plans
            if direct_dividend_funds:
                result += "💵 DIRECT DIVIDEND PLANS\n"
                result += "-" * 30 + "\n"
                for i, fund in enumerate(direct_dividend_funds[:5]):  # Top 5
                    result += _format_mutual_fund(fund, i + 1)
                result += "\n"
            
            # Display Regular Dividend Plans
            if regular_dividend_funds:
                result += "🏦 REGULAR DIVIDEND PLANS\n"
                result += "-" * 30 + "\n"
                for i, fund in enumerate(regular_dividend_funds[:5]):  # Top 5
                    result += _format_mutual_fund(fund, i + 1)
                result += "\n"
            
            # Summary statistics
            total_funds = len(data)
            result += f"📊 SEARCH SUMMARY\n"
            result += "-" * 30 + "\n"
            result += f"Total Funds Found: {total_funds}\n"
            result += f"Direct Growth Plans: {len(direct_growth_funds)}\n"
            result += f"Regular Growth Plans: {len(regular_growth_funds)}\n"
            result += f"Direct Dividend Plans: {len(direct_dividend_funds)}\n"
            result += f"Regular Dividend Plans: {len(regular_dividend_funds)}\n"
            result += f"Other Plans: {len(other_funds)}\n"
            
            # Investment tip
            result += f"\n💡 INVESTMENT TIP\n"
            result += "-" * 30 + "\n"
            result += "Direct Growth plans typically offer better returns due to lower expense ratios.\n"
            result += "Consider Direct plans if you don't need distributor services.\n"
        
        result += "\n" + "=" * 60
        return result
        
    except Exception as e:
        return f"Error parsing mutual fund data: {str(e)}"


def _format_mutual_fund(fund: dict, index: int) -> str:
    """Helper function to format individual mutual fund information"""
    if not isinstance(fund, dict):
        return ""
    
    scheme_name = fund.get('schemeName', 'N/A')
    
    # Extract fund house name (usually the first few words)
    fund_house = ""
    if scheme_name != 'N/A':
        words = scheme_name.split()
        if len(words) >= 2:
            fund_house = f"{words[0]} {words[1]}"
        elif len(words) == 1:
            fund_house = words[0]
    
    # Determine plan type
    plan_type = "Other"
    if 'direct' in scheme_name.lower():
        if 'growth' in scheme_name.lower():
            plan_type = "Direct Growth"
        elif any(word in scheme_name.lower() for word in ['dividend', 'payout']):
            plan_type = "Direct Dividend"
    elif 'regular' in scheme_name.lower():
        if 'growth' in scheme_name.lower():
            plan_type = "Regular Growth"
        elif any(word in scheme_name.lower() for word in ['dividend', 'payout']):
            plan_type = "Regular Dividend"
    
    result = f"{index}. {fund_house} - {plan_type}\n"
    result += f"   Full Name: {scheme_name[:80]}{'...' if len(scheme_name) > 80 else ''}\n"
    result += f"   ISIN: {fund.get('isin', 'N/A')}\n"
    result += f"   Scheme Type: {fund.get('schemeType', 'N/A')}\n"
    result += f"   Category ID: {fund.get('categoryId', 'N/A')}\n"
    result += "   " + "-" * 50 + "\n"
    return result


# 4. Stock Target Price
@tool
def get_stock_target_price(stock_id: str) -> str:
    """
    Get stock target price from Indian Stock API.
    
    Args:
        stock_id: Stock ID (required)
    
    Returns:
        Stock target price and analyst recommendations.
    """
    endpoint = "stock_target_price"
    params = {"stock_id": stock_id}
    
    data = make_indian_stock_request(endpoint, params)
    
    if "error" in data:
        return f"Error fetching target price for stock ID {stock_id}: {data['error']}"
    
    if not data:
        return f"No target price data found for stock ID {stock_id}"
    
    try:
        result = f"Stock Target Price for ID {stock_id}:\n\n"
        
        if isinstance(data, dict):
            result += f"Company Name: {data.get('company_name', 'N/A')}\n"
            result += f"Symbol: {data.get('symbol', 'N/A')}\n"
            result += f"Current Price: ₹{data.get('current_price', 'N/A')}\n"
            result += f"Target Price: ₹{data.get('target_price', 'N/A')}\n"
            result += f"Upside Potential: {data.get('upside_potential', 'N/A')}%\n"
            result += f"Analyst Rating: {data.get('analyst_rating', 'N/A')}\n"
            result += f"Number of Analysts: {data.get('analyst_count', 'N/A')}\n"
            result += f"High Target: ₹{data.get('high_target', 'N/A')}\n"
            result += f"Low Target: ₹{data.get('low_target', 'N/A')}\n"
            result += f"Mean Target: ₹{data.get('mean_target', 'N/A')}\n"
        
        return result
        
    except Exception as e:
        return f"Error parsing target price data: {str(e)}"


# 5. Trending Stocks
@tool
def get_trending_stocks() -> str:
    """
    Get trending stocks from Indian Stock API.
    
    Returns:
        List of trending stocks.
    """
    endpoint = "trending"
    
    data = make_indian_stock_request(endpoint)
    
    if "error" in data:
        return f"Error fetching trending stocks: {data['error']}"
    
    if not data:
        return "No trending stocks data found"
    
    try:
        result = "Trending Stocks:\n\n"
        
        if isinstance(data, list):
            for i, stock in enumerate(data[:10]):  # Top 10
                result += f"{i+1}. {stock.get('symbol', 'N/A')}\n"
                result += f"   Company: {stock.get('company_name', 'N/A')}\n"
                result += f"   Price: ₹{stock.get('price', 'N/A')}\n"
                result += f"   Change: {stock.get('change', 'N/A')} ({stock.get('change_percent', 'N/A')}%)\n"
                result += f"   Volume: {stock.get('volume', 'N/A')}\n"
                result += f"   Trend: {stock.get('trend', 'N/A')}\n"
                result += "-" * 40 + "\n"
        
        return result
        
    except Exception as e:
        return f"Error parsing trending stocks data: {str(e)}"


# 6. 52 Week High Low Data
@tool
def get_52_week_high_low() -> str:
    """
    Get 52-week high and low data from Indian Stock API.
    
    Returns:
        Stocks at 52-week highs and lows.
    """
    endpoint = "fetch_52_week_high_low_data"
    
    data = make_indian_stock_request(endpoint)
    
    if "error" in data:
        return f"Error fetching 52-week high/low data: {data['error']}"
    
    if not data:
        return "No 52-week high/low data found"
    
    try:
        result = "52-Week High/Low Data:\n\n"
        
        if isinstance(data, dict):
            if 'high' in data:
                result += "52-Week Highs:\n"
                for i, stock in enumerate(data['high'][:5]):  # Top 5
                    result += f"{i+1}. {stock.get('symbol', 'N/A')} - ₹{stock.get('price', 'N/A')}\n"
                result += "\n"
            
            if 'low' in data:
                result += "52-Week Lows:\n"
                for i, stock in enumerate(data['low'][:5]):  # Top 5
                    result += f"{i+1}. {stock.get('symbol', 'N/A')} - ₹{stock.get('price', 'N/A')}\n"
        
        return result
        
    except Exception as e:
        return f"Error parsing 52-week high/low data: {str(e)}"


# 7. Historical Data
@tool
def get_historical_data(symbol: str, period: str = "1Y") -> str:
    """
    Get historical data for a stock from Indian Stock API.
    
    Args:
        symbol: Stock symbol (e.g., RELIANCE, TCS)
        period: Time period (e.g., 1Y, 6M, 3M, 1M)
    
    Returns:
        Historical price data for the stock.
    """
    endpoint = "historical_data"
    params = {"stock_name": symbol.upper(), "period": period}
    
    data = make_indian_stock_request(endpoint, params)
    
    if "error" in data:
        return f"Error fetching historical data for {symbol}: {data['error']}"
    
    if not data:
        return f"No historical data found for {symbol.upper()}"
    
    try:
        result = f"Historical Data for {symbol.upper()} ({period}):\n\n"
        
        if isinstance(data, list):
            # Show last 10 data points
            for i, point in enumerate(data[-10:]):
                result += f"{i+1}. Date: {point.get('date', 'N/A')}\n"
                result += f"   Open: ₹{point.get('open', 'N/A')}\n"
                result += f"   High: ₹{point.get('high', 'N/A')}\n"
                result += f"   Low: ₹{point.get('low', 'N/A')}\n"
                result += f"   Close: ₹{point.get('close', 'N/A')}\n"
                result += f"   Volume: {point.get('volume', 'N/A')}\n"
                result += "-" * 30 + "\n"
        
        return result
        
    except Exception as e:
        return f"Error parsing historical data: {str(e)}"


# Helper function to get all Indian Stock API tools
def get_all_indian_stock_tools():
    """
    Get all Indian Stock API tools as a list.
    
    Returns:
        List of all Indian Stock API tools.
    """
    return [
        get_stock_details,
        get_industry_search,
        get_mutual_fund_search,
        get_stock_target_price,
        get_trending_stocks,
        get_52_week_high_low,
        get_historical_data
    ]


# For backward compatibility, keep the old function name
def get_all_nse_tools():
    """
    Get all Indian Stock API tools (for backward compatibility).
    
    Returns:
        List of all Indian Stock API tools.
    """
    return get_all_indian_stock_tools()


# Example usage
if __name__ == "__main__":
    # Test the tools
    print("=== Testing Stock Details ===")
    print(get_stock_details("RELIANCE"))
    
    print("\n=== Testing Industry Search ===")
    print(get_industry_search("Banking"))
    
    print("\n=== Testing Trending Stocks ===")
    print(get_trending_stocks())
    
    print("\n=== Testing 52-Week High/Low ===")
    print(get_52_week_high_low())
