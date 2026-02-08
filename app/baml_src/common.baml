template_string GlobalGuardrails #"
  ## Universal Constraints
  - UNCERTAINTY: If the text is completely ambiguous or empty, explicitly state it in your reasoning and return 'null' or the most neutral category.
  - DATA PRIVACY: Never hallucinate personal identifiers not present in the text.
  - NEUTRALITY: Maintain a professional, objective tone in your 'model_reasoning'.
  - NO PREJUDICE: Do not make assumptions based on names or dialects.
"#