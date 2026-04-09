#!/usr/bin/env python3
"""
Simple test script for the Productivity Copilot API
Run with: python test_api.py
"""

import requests
import json
import sys

API_BASE = "http://localhost:8080"
USER_ID = "00000000-0000-0000-0000-000000000001"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_chat(message):
    """Test chat endpoint"""
    print(f"Testing /chat with message: '{message}'")
    response = requests.post(
        f"{API_BASE}/chat",
        json={"message": message, "user_id": USER_ID}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response']}")
        print(f"Session ID: {data['session_id']}\n")
    else:
        print(f"Error: {response.text}\n")
    return response.status_code == 200

def test_workflow(instruction):
    """Test workflow endpoint"""
    print(f"Testing /workflow/run with instruction: '{instruction}'")
    response = requests.post(
        f"{API_BASE}/workflow/run",
        json={"instruction": instruction, "user_id": USER_ID}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Workflow steps: {data.get('workflow_steps', [])}")
        print(f"Response: {data['response']}\n")
    else:
        print(f"Error: {response.text}\n")
    return response.status_code == 200

def main():
    print("=" * 60)
    print("Productivity Copilot API Test Suite")
    print("=" * 60 + "\n")

    tests_passed = 0
    tests_total = 0

    # Test 1: Health check
    tests_total += 1
    if test_health():
        tests_passed += 1

    # Test 2: Create a task
    tests_total += 1
    if test_chat("Create a task to review the quarterly budget report by next Friday"):
        tests_passed += 1

    # Test 3: Schedule an event
    tests_total += 1
    if test_chat("Schedule a team meeting tomorrow at 2 PM for 1 hour in Conference Room B"):
        tests_passed += 1

    # Test 4: Create a note
    tests_total += 1
    if test_chat("Save a note: Discussed new feature requirements with product team. Key points: mobile-first design, offline support, and accessibility compliance"):
        tests_passed += 1

    # Test 5: List tasks
    tests_total += 1
    if test_chat("Show me all my pending tasks"):
        tests_passed += 1

    # Test 6: Semantic search
    tests_total += 1
    if test_chat("What notes do I have about product features?"):
        tests_passed += 1

    # Test 7: Multi-step workflow
    tests_total += 1
    if test_workflow("I need to prepare for the budget review meeting. Schedule it for tomorrow at 3 PM, create a task to gather the financial reports, and search my notes for previous budget discussions"):
        tests_passed += 1

    # Summary
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{tests_total}")
    print("=" * 60)

    return 0 if tests_passed == tests_total else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API. Make sure the server is running on http://localhost:8080")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
