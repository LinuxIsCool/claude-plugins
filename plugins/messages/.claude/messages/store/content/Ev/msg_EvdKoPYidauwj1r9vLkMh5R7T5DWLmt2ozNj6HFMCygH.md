---
id: msg_EvdKoPYidauwj1r9vLkMh5R7T5DWLmt2ozNj6HFMCygH
kind: 1010
account_id: email_cloudplatform-noreply_google_com
created_at: 1765852435000
imported_at: 1766105432511
author_name: Google Cloud
title: [Reminder] [Action Required] Grant explicit act-as permissions for Dataform security enhancements
thread_id: email_93d1fdf8e8a5
platform: email
platform_id: <d6bdc93d15d578484f84c4ff5b9533ae29a06934-20378990-111800303@google.com>
tags: [["subject","[Reminder] [Action Required] Grant explicit act-as permissions for Dataform security enhancements"],["folder","INBOX"]]
---

Act-as checks to be enforced for new repositories on Jan 19, 2026 and for existing ones starting Apr 29, 2026.




MY CONSOLE




Hello Shawn,

We're writing to follow up on our previous communication and inform all new and existing customers that we're making changes to our security model in Dataform. Starting January 19, 2026, security enhancements in the Dataform API will change how workflows are run and what service accounts users can use.

This change affects all users and scheduled workflows of Dataform, BigQuery Notebooks, BigQuery Pipelines, and BigQuery data preparations, unless their permissions are already set up in a way outlined below. To help you prepare for the upcoming security enhancements, we have also released a new diagnostic tool.

We understand that these changes may require some planning and decision-making. Therefore, we have provided additional information about the tool and the changes below to guide you through the transition.

What you need to know

Key changes:


This update enforces a new access control model known as strict act-as mode. It affects the following resources:

Workflows need to be scheduled to run using either a custom service account or a user's Google Account. Running workflows using the Dataform service agent will no longer be allowed. Existing Dataform, BigQuery Notebook, BigQuery Pipelines, and BigQuery data preparation workflows using the Dataform service agent will stop running.
Users who update release configurations in Dataform or configure workflows in Dataform, BigQuery Notebook, BigQuery Pipelines, and BigQuery data preparation need to have the iam.serviceAccounts.actAs permission on custom service accounts used in those workflows.
For Dataform repositories not connected to a third-party git repository, automatic releases will be disabled.


New diagnostic tool:

We have introduced a new log-based diagnostic tool in Cloud Logging to help you identify and resolve potential permission issues before the changes take effect starting January 19, 2026. For more information, review our documentation on Using strict act-as mode.

Timeline:


January 19, 2026: Act-as check will be enforced for all newly created repositories.
Between April 29 and July 31, 2026: We will gradually enforce the strict act-as mode for existing repositories.

What you need to do

Action is required before January 19, 2026, for new repositories and before April 29, 2026, for existing ones:


Switch all workflows using the Dataform service agent to use a custom service account. This applies to all scheduled workflows for Dataform, BigQuery Notebook, BigQuery Pipelines, and BigQuery data preparation.
Ensure that the appropriate principals have the Service Account User role (roles/iam.serviceAccountUser) granted on the custom service accounts in Identity and Access Management (IAM). This role contains the iam.serviceAccounts.actAs permission. Users without the iam.serviceAccounts.actAs permission will be unable to create new schedules or manually invoke workflows using the service account.

Grant this role to the Dataform service agent on custom service accounts used in workflow configurations in Dataform, scheduled notebooks, pipelines or data preparations in BigQuery.
Grant this role to all users who need to use custom service accounts to create or modify release configurations, workflow configurations or schedules.
Grant this role to the custom service accounts that call the Dataform API to start workflow invocations (for example, using Cloud Composer).

We recommend ensuring that a code review process is in place for all automatically released code in connected repositories.

Note:


You may already have the required iam.serviceAccounts.actAs permission through custom roles. If that is the case, no further action is needed.
See Manage access to projects, folders, and organizations for more information about granting roles.

Your affected projects are listed below:


opensource-observer-444721

We're here to help

If you have any questions or require assistance, please contact Google Cloud Support.

Thanks for choosing Dataform.





– The Google Cloud Team





DOCUMENTATION



SUPPORT




Was this information helpful?

Yes Neutral No


© 2025 Google LLC 1600 Amphitheatre Parkway, Mountain View, CA 94043

You've received this mandatory service announcement to update you about important changes to Google Cloud or your account.



Visit Google Cloud blog Visit GCP on GitHub Visit Google Cloud on LinkedIn Visit Google Cloud on Twitter
