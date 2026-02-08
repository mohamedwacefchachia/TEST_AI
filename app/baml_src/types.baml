//Classification (API 1)
enum Gender {
  Male 
  Female
  Other
}

enum ContactMethod {
  Email
  Phone
}

class Theme {
  title string
  description string
}

class ClassificationOutput {
  model_reasoning string
  chosen_theme Theme
}

//Form (API 2)
class PersonalInfo {
  first_name string?
  last_name string? 
  gender Gender?
}

class ContactInfo {
  email string?
  phone string?
  preferred_contact_method ContactMethod?
  call_reasons string[]?
}

class FormOutput {
  personal_info PersonalInfo
  contact_info ContactInfo
}

//Bonus 2
class ProbabilisticClassificationOutput {
  chosen_theme Theme 
  confidence float 
}

