import json
import glob
import os

transcript_path = '/home/sp/.gemini/antigravity-cli/brain/5724fa97-b1d7-49ab-8f40-fdff66838f8d/.system_generated/logs/transcript_full.jsonl'
files_to_recover = ['chapters_10.tex', 'chapters_2_3_4.tex', 'chapters_6_7.tex', 'chapters_8.tex', 'chapters_9.tex', 'SHIELD_Project_Report.tex']

recovered = {}

with open(transcript_path, 'r') as f:
    for line in f:
        try:
            step = json.loads(line)
        except:
            continue
        if 'tool_calls' in step:
            for tc in step['tool_calls']:
                if 'name' in tc and tc['name'].endswith('write_to_file'):
                    args = tc.get('args', tc.get('arguments', {}))
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except:
                            continue
                    if 'TargetFile' in args and 'CodeContent' in args:
                        basename = os.path.basename(args['TargetFile'])
                        if basename in files_to_recover:
                            recovered[basename] = args['CodeContent']

print(f"Recovered {len(recovered)} files.")
for k, v in recovered.items():
    with open(f"/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs/{k}", 'w') as out:
        out.write(v)
    print(f"Restored {k}")
