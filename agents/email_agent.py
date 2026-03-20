from utils.email_sender import send_email

class EmailAgent:

    def notify(self, email, name, status, reason):

        if not email:
            print(f"No email found for {name}")
            return False

        # If name extraction fails
        if not name or name.lower() == "candidate":
            name = "Candidate"

        if status == "Shortlisted":

            subject = "Interview Invitation"

            body = f"""
Dear {name},

We are pleased to inform you that your application has been shortlisted.

We would like to invite you to the next stage of our recruitment process. Our team will contact you shortly with the details of the interview.

Thank you for your interest and time.

Best regards,
Recruitment Team
"""

        else:

            subject = "Application Status Update"

            body = f"""
Dear {name},

Thank you for your application.

After careful consideration, we regret to inform you that your application has not been shortlisted at this time.

Reason: {reason}

We appreciate your interest and encourage you to apply for future opportunities with us.

Best regards,
Recruitment Team
"""

        email_status = send_email(email, subject, body)

        if email_status:
            print(f"Email successfully sent to {name} - {email}")
        else:
            print(f"Failed to send email to {name} - {email}")

        return email_status