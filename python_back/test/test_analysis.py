from python_back.src.analysis import Analysis

test_config = {
    'user': 'waf',
    'password': 'cam',
    'host': '127.0.0.1',
    'database': 'wafcam',
    'raise_on_warnings': True
}

if __name__ == '__main__':
    analysis = Analysis(test_config)
    analysis.start_analysis(5000)
