{
                    "issues": [
                        {
                            "id": "SEC-001",
                            "title": "Hardcoded Credentials",
                            "description": "Found hardcoded credentials in the code. This is a security risk.",
                            "original_code": "password = 'admin123'",
                            "suggested_code": "password = os.environ.get('PASSWORD')",
                            "confidence": 0.9
                        },
                        {
                            "id": "PERF-001",
                            "title": "Inefficient Loop",
                            "description": "This loop could be optimized for better performance.",
                            "original_code": "for i in range(len(items)): print(items[i])",
                            "suggested_code": "for item in items: print(item)",
                            "confidence": 0.8
                        }
                    ]
                }