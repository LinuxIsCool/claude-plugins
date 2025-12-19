---
id: msg_GCLszrxPPrfjG6gw9xH3Lfegav2FgDXJFbmqAGVfzS93
kind: 1010
account_id: email_noreply_pypi_org
created_at: 1765724177000
imported_at: 1766105427516
author_name: PyPI
title: [PyPI] Your API credentials from PyPI were found on a public webpage
thread_id: email_28221241feb9
platform: email
platform_id: <0101019b1d5cc35a-42af4a6e-d1b6-4159-a687-0ba9ff005ae3-000000@us-west-2.amazonses.com>
tags: [["subject","[PyPI] Your API credentials from PyPI were found on a public webpage"],["folder","INBOX"]]
---

What happened?


A third party (Deps.dev) has informed us that a PyPI API token
associated with your account "ygg_anderson" was found to be accessible at the
following public URL. We have automatically revoked this token.

https://files.pythonhosted.org/packages/1c/c0/c1984336bb53c3fbe06748eca022013f8b404f0ca13c05981548979a9818/registry_review_mcp-2.1.0.tar.gz#sha256=4e29df7e6ac4e6b7fd235e57dc1caaffc3cfa6a0924eacdae564897bdb3f1ae7

What should I do?

First, we recommend that you inspect the public page where the token
appeared. Please investigate whether this is the result of an error on your side or if
someone else acquired and published your token.

If the token was not published by you, it means it was stolen, either from you or from
someone with access to your account on PyPI. We urge you to take all the
necessary steps to secure all your credentials.

Once you have taken the applicable steps to ensure the token will not become public
again, you're welcome to generate a new one. Log into your account and head to your
profile page to create a new API token. You will need to update your existing
integrations with the new token.

Lastly, please review the releases of all your packages. You should make
sure a third party did not use your publicly accessible token to impersonate
you and release a malicious package.

How do you know this?

This is an automated message. Our partner Deps.dev analyzes all the data it receives
for unintentional PyPI token publications and warns us every time it finds
one. We check every disclosure we recieve and take action when the token appears valid.

For more information, see our FAQ at http://pypi.org/help/#compromised-token

For help, you can send an email to admin@pypi.org to communicate with the PyPI
administrators.
