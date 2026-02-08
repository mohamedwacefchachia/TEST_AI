function ExtractForm(text: string) -> FormOutput {
  client Haiku
  prompt #"
    ## Role
    You are a high-precision Data Extraction Specialist. 
    Your task is to transform conversational transcripts between agents and customers into a strictly structured JSON format.

    {{ GlobalGuardrails() }}

    ## Extraction Rules
    1. **Strict Fidelity**: Extract information exactly as stated. Do not hallucinate.
    2. **Handling Omissions/Refusals**: If a piece of information is not mentioned or if the customer explicitly refuses to provide it (e.g., "I'd prefer not to share"), set the field to `null`.
    3. **Normalization**: 
        - Names must be capitalized (e.g., "john" -> "John").
        - Emails must be lowercase (e.g., "USER@Host.Com" -> "user@host.com").
    4. **Enums**: 
        - `gender` MUST be one of: "Male", "Female", "Other", or `null`.
        - `preferred_contact_method` MUST be: "Email", "Phone", or `null`.

    ## Few-Shot Examples

    ### Example 1: "Refusal" Case  
    **Input**: "Agent: Good morning! ... Could you please provide your first and last name? Customer: Sure! My name is John Doe. Agent: ... May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: ... could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: ... phone number? Customer: I’d rather not provide that right now. Agent: ... email or phone? Customer: Please contact me via Email. Agent: ... reason for your call? Customer: I'm not ready to specify that just yet."
    **Reasoning**: The customer provided a name and email but explicitly refused gender, phone, and call reason. 
    **Output**: {
      "personal_info": {"first_name": "John", "last_name": "Doe", "gender": null},  
      "contact_info": {"email": "johndoe@example.com", "phone": null, "preferred_contact_method": "Email", "call_reasons": null}
    }

    ### Example 2 : "Nominal" Case
    **Input**: "Agent: Details please? Customer: I am Alice Smith. I identify as Female. You can reach me at alice.smith@work.com or on my cell 07654321. I prefer being called on my phone. I'm calling because I have a billing issue and I also need to update my home address."
    **Reasoning**: All fields are present. 'call_reasons' contains two distinct items. 
    **Output**: {
      "personal_info": {"first_name": "Alice", "last_name": "Smith", "gender":"Female"},     
      "contact_info": {"email": "alice.smith@work.com", "phone": "07654321", "preferred_contact_method": "Phone", "call_reasons": ["Billing issue", "Address update"]}
    }

    ### Example 3: "Incomplete" Case 
    **Input**: "Customer: Hi, I'm Bob. I don't have an email address to give you. Just use my phone 123-456. I'm calling about a refund for my last order."
    **Reasoning**: First name is Bob. Last name and gender are not mentioned. Email is unavailable. One call reason provided.
    **Output**: {
      "personal_info": {"first_name": "Bob", "last_name": null, "gender": null},
      "contact_info": {"email": null, "phone": "123-456", "preferred_contact_method": "Phone", "call_reasons": ["Refund request"]}
    }

    ## Current Transcript to Process
    ---
    {{ text }}
    ---

    {{ ctx.output_format }}
  "#
}