# This file is deprecated. Please use nse_tools.py for NSE India stock market tools.
# Import all NSE tools from the new file

from .nse_tools import (
    get_stock_quote,
    get_option_chain,
    get_index_option_chain,
    get_most_active_stocks,
    get_gainers_losers,
    get_all_indices,
    get_index_constituents,
    get_52_week_stocks,
    get_pre_open_data,
    get_corporate_announcements,
    get_all_nse_tools
)

# For backward compatibility, provide the same function names
def get_all_stock_tools():
    """
    Returns a list of all NSE tools
    
    Returns:
        List of all NSE tools
    """
    return get_all_nse_tools()

def get_indian_stock_tools():
    """
    Returns a list of NSE India tools
    
    Returns:
        List of NSE India tools
    """
    return get_all_nse_tools()

# Keep the old function names for compatibility
get_fmp_tools = get_all_nse_tools  # Redirect to NSE tools
