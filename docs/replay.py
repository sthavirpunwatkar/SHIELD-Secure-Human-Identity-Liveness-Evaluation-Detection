import json
import os

transcript_path = '/home/sp/.gemini/antigravity-cli/brain/5724fa97-b1d7-49ab-8f40-fdff66838f8d/.system_generated/logs/transcript_full.jsonl'
files_to_recover = ['chapters_10.tex', 'chapters_2_3_4.tex', 'chapters_6_7.tex', 'chapters_8.tex', 'chapters_9.tex', 'SHIELD_Project_Report.tex']

files_state = {f: "" for f in files_to_recover}

with open(transcript_path, 'r') as f:
    for line in f:
        try:
            step = json.loads(line)
        except:
            continue
        if 'tool_calls' in step:
            for tc in step['tool_calls']:
                name = tc.get('name', '')
                args = tc.get('args', tc.get('arguments', {}))
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except:
                        continue
                
                if 'write_to_file' in name:
                    if 'TargetFile' in args and 'CodeContent' in args:
                        basename = os.path.basename(args['TargetFile'])
                        if basename in files_to_recover:
                            files_state[basename] = args['CodeContent']
                            
                elif 'replace_file_content' in name:
                    if 'TargetFile' in args:
                        basename = os.path.basename(args['TargetFile'])
                        if basename in files_to_recover:
                            content = files_state[basename]
                            if 'ReplacementChunks' in args:
                                for chunk in args['ReplacementChunks']:
                                    if 'TargetContent' in chunk and 'ReplacementContent' in chunk:
                                        content = content.replace(chunk['TargetContent'], chunk['ReplacementContent'])
                            elif 'TargetContent' in args and 'ReplacementContent' in args:
                                content = content.replace(args['TargetContent'], args['ReplacementContent'])
                            files_state[basename] = content

for k, v in files_state.items():
    with open(f"/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs/{k}", 'w') as out:
        out.write(v)
    print(f"Restored and replayed {k} using TargetContent")
