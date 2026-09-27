import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    print("🚀 Starting API Test...")
    
    # 1. Test Health
    try:
        health_resp = requests.get("http://localhost:8000/health")
        print(f"Health Check: {health_resp.json()}")
    except Exception as e:
        print(f"Server is not up yet: {e}")
        return

    # 2. Upload a simple text document to test FAISS + BM25 indexing
    print("\n📚 Uploading a test document...")
    doc_content = {
        "content": "The RAG Voice Boilerplate is a powerful tool built by Montassar Chorfi. It features a Hybrid Search engine combining FAISS and BM25, and uses Conversational Memory to track chat history.",
        "metadata": {"source": "test_script"}
    }
    # Notice: The original boilerplate README uses /documents/upload for files. 
    # If there's a /documents/text endpoint, we can use it. Let's try sending to query directly to see the memory.
    
    # Let's test the conversational memory with the /query endpoint
    print("\n💬 Testing Conversational Memory & RAG...")
    
    session_id = "test_session_123"
    
    question_1 = "Who built the RAG Voice Boilerplate?"
    print(f"Q1: {question_1}")
    resp_1 = requests.post(
        f"{BASE_URL}/query", 
        params={"question": question_1, "session_id": session_id}
    )
    print(f"A1: {resp_1.json()}")
    
    time.sleep(2)
    
    question_2 = "What kind of search engine does it feature?"
    print(f"\nQ2: {question_2} (Testing context awareness)")
    resp_2 = requests.post(
        f"{BASE_URL}/query", 
        params={"question": question_2, "session_id": session_id}
    )
    print(f"A2: {resp_2.json()}")

if __name__ == "__main__":
    test_api()
