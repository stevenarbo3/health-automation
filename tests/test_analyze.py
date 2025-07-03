import sys
import os
import pytest
import tempfile
import json
import textwrap


# Add the project root (parent of src/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyze import get_latency, analyze


class TestGetLatency:
    
    def test_two_digits(self):
        contents = ['latency=72ms']
        assert get_latency(contents, 0) == 72
        
    def test_three_digits(self):
        contents = ['latency=383ms']
        assert get_latency(contents, 0) == 383
        
    def test_no_pattern(self):
        contents = ['latency=383']
        assert get_latency(contents, 0) == 0
        
class TestAnalyze:
    
    def setup_method(self):
        self.log_data = textwrap.dedent("""\
                        2025-07-01T18:25:30 | job_id=1 | status=success | latency=200ms
                        2025-07-01T18:25:35 | job_id=2 | status=success | latency=300ms
                        2025-07-01T18:25:40 | job_id=3 | status=success | latency=40ms
                        """)
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as fp:
            fp.write(self.log_data)
            fp.flush()
            self.json_str = analyze(fp.name)

        assert self.json_str is not None, "analyze() returned None unexpectedly"
        self.data = json.loads(self.json_str)
        
        self.tmp_path = fp.name
    
    def test_total_jobs(self):
        assert self.data['total_jobs'] == 3
        
    def test_percent_success(self):
        assert self.data['percent_success'] == 100
        
    def test_percent_failure(self):
        assert self.data['percent_failure'] == 0
        
    def test_avg_latency(self):
        assert self.data['avg_latency'] == 180
        
    def test_most_common_reason(self):
        log_data = textwrap.dedent("""\
                        2025-07-01T18:25:30 | job_id=1 | status=success | reason=Bad Request | latency=200ms
                        2025-07-01T18:25:35 | job_id=2 | status=success | reason=Internal Server Error | latency=300ms
                        2025-07-01T18:25:40 | job_id=3 | status=success | reason=Bad Request | latency=40ms
                        """)
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as fp:
            fp.write(log_data)
            fp.flush()
            json_str = analyze(fp.name)

        assert json_str is not None, "analyze() returned None unexpectedly"
        data = json.loads(json_str)
        
        assert data['most_common_reason'] == 'Bad Request'
        
    def test_no_failures(self):
        assert self.data['most_common_reason'] == 'no failures'
        
    def teardown_method(self):
        if os.path.exists(self.tmp_path):
            os.remove(self.tmp_path)
    
    
        



