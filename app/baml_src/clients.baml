client<llm> Haiku {
  provider aws-bedrock
  options {
    model "eu.anthropic.claude-haiku-4-5-20251001-v1:0"
    region "eu-west-1" 
  }
}

// multiple parallel classifications : bonus 1
client<llm> Sonnet {
  provider aws-bedrock
  options {
    model "eu.anthropic.claude-sonnet-4-5-20250929-v1:0"
    region "eu-west-1" 
  }
}

client<llm> Opus {
  provider aws-bedrock
  options {
    model "eu.anthropic.claude-opus-4-5-20251101-v1:0"
    region "eu-west-1" 
  }
}