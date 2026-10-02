# explain.py receives a response regardless of the LLM provider of choice
from ai.providers.base import LLMProvider
from rules.base import Finding

def explain_finding(finding: Finding, source_snippet: str, provider: LLMProvider) -> str:
    """Explain a finding using an LLM and return its response, runnning Prompt V1"""
    # provide finding in destructured form, specifically finding.rule_id and finding.message
    # provide source_snippet in python markdown
    # respond in 2-3 sentences at most
    # dont be overly confident
    # indicate the finding line is the one starting with '---->' from get_snippet
    prompt = f"""
    You operate as a key part of a static Python analyzer tool that employs an LLM to explain various findings:
    structured patterned rule violations. You receive the following crucial information about a finding:
        Rule id: {finding.rule_id},
        Line number: {finding.line},
        Message: "{finding.message}",
    and a file with the source code where the violating line is indicated '---->' and the rest is surrounding context:
    
    ```python
    {source_snippet}
    ```
    
    You must now explain to the user of the Python analyzer, in no more than 2-3 sentences, exactly the nature of the
    finding and just as importantly, whether or not this is likely a real issue or potentially a false positive by the static 
    analyzer. Do not be overconfident and do not hesitate. Be incredibly concise, and shorten some sentences like
    'there is a high likelihood that this is a false positive because...' to 'likely a false positive as....'."""
        
    return provider.complete(prompt)