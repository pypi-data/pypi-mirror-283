import sys

try:
    import langchain
    
    print("found langchain")
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

if not LANGCHAIN_AVAILABLE:
    print("[MaximSDK] LangChain is not available. You can't use MaximLangchainTracer.", file=sys.stderr)