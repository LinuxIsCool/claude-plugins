---
id: msg_9xHnazXMzXrz7UW6LqmhSHx216oA9kJmCpdHNfMr8EzG
kind: 1010
account_id: email_notifications_github_com
created_at: 1764657918000
imported_at: 1766105346049
author_name: Cfomodz
title: "Re: [elizaOS/eliza] How to have chat prompt in CLI after running? (Discussion #3369)"
thread_id: email_134f9e29898f
reply_to: <elizaOS/eliza/repo-discussions/3369@github.com>
platform: email
platform_id: <elizaOS/eliza/repo-discussions/3369/comments/15131987@github.com>
tags: [["subject","Re: [elizaOS/eliza] How to have chat prompt in CLI after running? (Discussion #3369)"],["folder","INBOX"],["cc","shawn@longtailfinancial.com, author@noreply.github.com"]]
---

Add the `direct` client to your character configuration file:

```json
{
  "name": "YourAgent",
  "clients": ["direct"],
  "modelProvider": "openai",
  "settings": {
    "secrets": {
      "OPENAI_API_KEY": "your-key-here"
    }
  }
}
```

Then start your agent:

```bash
elizaos agent start --path ./character.json
```

The terminal chat prompt will appear automatically.

-- 
Reply to this email directly or view it on GitHub:
https://github.com/orgs/elizaOS/discussions/3369#discussioncomment-15131987
You are receiving this because you authored the thread.

Message ID: <elizaOS/eliza/repo-discussions/3369/comments/15131987@github.com>
