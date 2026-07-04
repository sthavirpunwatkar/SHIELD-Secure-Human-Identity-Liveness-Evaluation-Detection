import re

file_path = "frontend/lib/services/challenge_service.dart"

with open(file_path, "r") as f:
    content = f.read()

# Remove the early return that blocks verdict processing
bad_code = """
    if (_state == ChallengeState.allPassed || _state == ChallengeState.failed) {
      return;
    }
"""

good_code = """
    if (_state == ChallengeState.allPassed || _state == ChallengeState.failed) {
      // Allow verdict to still be processed to get final score, but ignore other messages
      if (type == 'verdict') {
        _handleVerdict(json);
      }
      return;
    }
"""

content = content.replace(bad_code.strip(), good_code.strip())

with open(file_path, "w") as f:
    f.write(content)
print("challenge_service.dart patched")
