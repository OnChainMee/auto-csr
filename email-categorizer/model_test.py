import email_categorizer

email_categorizer = email_categorizer.EmailCategorizer()
category = email_categorizer.categorize_email(
  "I don't like the color of the shirt I ordered.")

print("Email category:", category)
