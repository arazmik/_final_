#!/usr/bin/env python3
"""
Test runner script for Selenium framework
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Selenium Test Framework Runner")
    parser.add_argument("--browser", default="chrome", choices=["chrome", "firefox", "edge"],
                       help="Browser to use for tests")
    parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
    parser.add_argument("--markers", help="Run tests with specific markers (e.g., smoke, regression)")
    parser.add_argument("--parallel", type=int, help="Number of parallel workers")
    parser.add_argument("--report", choices=["html", "allure"], default="html",
                       help="Type of report to generate")
    parser.add_argument("--test-file", help="Specific test file to run")
    
    args = parser.parse_args()
    
    # Set environment variables
    env = os.environ.copy()
    env["BROWSER"] = args.browser
    if args.headless:
        env["HEADLESS"] = "true"
    
    # Build pytest command
    cmd_parts = ["python", "-m", "pytest"]
    
    if args.test_file:
        cmd_parts.append(args.test_file)
    else:
        cmd_parts.append("tests/")
    
    if args.markers:
        cmd_parts.extend(["-m", args.markers])
    
    if args.parallel:
        cmd_parts.extend(["-n", str(args.parallel)])
    
    if args.report == "html":
        cmd_parts.extend(["--html=reports/report.html", "--self-contained-html"])
    elif args.report == "allure":
        cmd_parts.append("--alluredir=allure-results")
    
    cmd_parts.extend(["-v", "--tb=short"])
    
    command = " ".join(cmd_parts)
    
    # Create necessary directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)
    
    # Run tests
    success = run_command(command, "Running Selenium Tests")
    
    if success and args.report == "allure":
        print("\nGenerating Allure report...")
        run_command("allure serve allure-results", "Serving Allure Report")
    
    if success:
        print("\n✅ Tests completed successfully!")
        if args.report == "html":
            print("📊 HTML report generated: reports/report.html")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
