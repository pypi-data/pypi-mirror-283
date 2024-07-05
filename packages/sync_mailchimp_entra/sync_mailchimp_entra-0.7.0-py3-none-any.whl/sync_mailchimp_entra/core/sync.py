import automationassets  # type: ignore
from sync_mailchimp_entra.core.mailchimp import MailchimpClient
from sync_mailchimp_entra.core.graph import GraphClient


async def mailchimp_entra(list_mailchimp_id, entra_groups_ids):
    """Main synchronization function."""
    members_mailchimp_emails = MailchimpClient.get_instance().list_mailchimp_emails(
        list_mailchimp_id
    )

    members_entra_emails = []
    for entra_group_id in entra_groups_ids:
        members_entra_emails.extend(
            await GraphClient.get_instance().list_entra_emails(entra_group_id)
        )

    # Iteration on every MailChimp mail to see if it is in Entra
    for email in members_mailchimp_emails:
        if email not in members_entra_emails:
            MailchimpClient().get_instance().remove_member(list_mailchimp_id, email)
            if automationassets.get_automation_variable("DEBUG") == "1":
                print(email + " removed from MailChimp mails.")

    # Iteration on every Entra mail to see if it is in MailChimp list
    for email in members_entra_emails:
        if email not in members_mailchimp_emails:
            # Get user data from Graph
            user = await GraphClient.get_instance().get_user(email)

            # Get correct language for user
            if user.company_name == "XLM":
                language = "fr"
            else:
                language = "en"

            # Addition of user in MailChimp
            if user.given_name is None or user.surname is None:
                MailchimpClient().get_instance().add_member(
                    list_mailchimp_id, email, language=language
                )
                if automationassets.get_automation_variable("DEBUG") == "1":
                    print(email + " added to MailChimp mails.")
            else:
                MailchimpClient().get_instance().add_member(
                    list_mailchimp_id,
                    email,
                    first_name=user.given_name,
                    last_name=user.surname,
                    language=language,
                )
                if automationassets.get_automation_variable("DEBUG") == "1":
                    print(email + " added to MailChimp mails.")
