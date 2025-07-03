import os
import json
import re

# create path that is portable and configurable
two_up = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(two_up, 'logs', 'service.logs')

def get_latency(latency, contents, num):
    match = re.search(r'(\d+)ms', contents[num])
    return int(match.group(1)) if match else 0

def analyze(path):

    try:
        with open(path, 'r') as log:
            total_jobs = 0
            total_success = 0
            total_failure = 0
            latency = 0
            
            reason_dict = {}
            
            for line in log:
                total_jobs += 1
                
                contents = line.split(' | ')
                
                if contents[2] == 'status=success':
                    total_success += 1
                else:
                    total_failure += 1
                    
                if len(contents) == 4:
                    latency += get_latency(latency, contents, 3)
                else:
                    latency += get_latency(latency, contents, 4)
                    
                    reason = contents[3].partition('reason=')[2]
                    reason_dict[reason] = reason_dict.get(reason, 0) + 1
                    
            percent_success = total_success / total_jobs * 100
            percent_failure = total_failure / total_jobs * 100
            avg_latency = latency / total_jobs
            
            if reason_dict:
                temp = max(reason_dict.values())
                most_common_reason = [key for key in reason_dict if reason_dict[key] == temp][0]
            else:
                most_common_reason = 'no failures'
            
            data = {
                'total_jobs': total_jobs,
                'percent_success': percent_success,
                'percent_failure': percent_failure,
                'avg_latency': avg_latency,
                'most_common_reason': most_common_reason
            }
            
            json_data = json.dumps(data, indent=2)
            
            return json_data
                
                    
    except FileNotFoundError:
        print("Error: The log file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
print(analyze(path))
    
    