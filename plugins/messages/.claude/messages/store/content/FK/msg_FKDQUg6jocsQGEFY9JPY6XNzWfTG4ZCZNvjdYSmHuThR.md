---
id: msg_FKDQUg6jocsQGEFY9JPY6XNzWfTG4ZCZNvjdYSmHuThR
kind: 1010
account_id: email_notifications_github_com
created_at: 1764657633000
imported_at: 1766105345804
author_name: Cfomodz
title: "Re: [elizaOS/eliza] What to do when callback is undefined in an action handler? How to debug that? (Discussion #3257)"
thread_id: email_63c4c384db7c
reply_to: <elizaOS/eliza/repo-discussions/3257@github.com>
platform: email
platform_id: <elizaOS/eliza/repo-discussions/3257/comments/15131960@github.com>
tags: [["subject","Re: [elizaOS/eliza] What to do when callback is undefined in an action handler? How to debug that? (Discussion #3257)"],["folder","INBOX"],["cc","shawn@longtailfinancial.com, author@noreply.github.com"]]
---

The `callback` parameter in your action handler is `undefined`.

Always check if the callback exists before calling it:

```typescript
if (callback) {
  await callback({
    text: response,
    actions: ['HELLO_WORLD'],
    source: message.content.source
  });
}
```

-- 
Reply to this email directly or view it on GitHub:
https://github.com/orgs/elizaOS/discussions/3257#discussioncomment-15131960
You are receiving this because you authored the thread.

Message ID: <elizaOS/eliza/repo-discussions/3257/comments/15131960@github.com>
