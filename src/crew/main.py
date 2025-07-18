#!/usr/bin/env python

import sys
from conversation_crew import ConversationCrew

def main():
    """
    Interactive main function to run the conversation crew
    """
    # Initialize the crew
    crew = ConversationCrew()
    
    print("🚀 NSE Stock Market Analysis System")
    print("📊 Ask any question about Indian stocks, IPOs, or market data")
    print("💡 Examples:")
    print("   - 'Tell me about Reliance stock'")
    print("   - 'LIC IPO performance'")
    print("   - 'Top gainers today'")
    print("   - 'Current price of TCS'")
    print("-" * 60)
    
    # Get user input
    user_question = input("🤔 Your question: ").strip()
    
    if not user_question:
        user_question = "tell me about lic ipo"  # Default question
        print(f"� Using default question: {user_question}")
    
    print(f"\n� Analyzing: {user_question}")
    print("-" * 60)
    
    try:
        # Run the crew with inputs
        result = crew.crew().kickoff(inputs={'user_question': user_question})
        
        print("\n✅ Analysis Complete!")
        print("-" * 60)
        print("📈 Result:")
        print(result)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
