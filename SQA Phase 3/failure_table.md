# Failure Table

| Test Failed | Test Purpose | Error | Correction |
| --- | --- | --- | --- |
| TC-01 to TC-15 | Validate terminal formatting | Extra transaction/history log lines printed | Removed `_info()` logging from `run()` |
| TC-01 to TC-15 | Validate login formatting | Login prompts printed inline due to inline `input()` | Modified `_prompt()` to separate `print()` and `input()` |
| TC-03 to TC-15 | Validate menu interaction formatting | Menu selection prompt printed inline with response | Separated menu prompt printing from `input()` |
| TC-01 to TC-15 | Validate box formatting | Section closing border width incorrect (`_W + 2`) | Corrected `_section_end()` to use `_W` only |