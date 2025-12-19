---
id: msg_3nqciY2xo3byAjJV9qFZj4HN72iuSKEKDzSkPzzVAKpm
kind: 1010
account_id: email_matt_ref_tools
created_at: 1764594343000
imported_at: 1766105337701
author_name: Ref
title: Ref update (Nov 30, 2025)
thread_id: email_399c1785528d
platform: email
platform_id: <c1e6166f98a97ab9ecdc7b0b8.9dfba1f110.20251201130533.24aa2bace3.404d67e9@mail50.atl71.mcdlv.net>
tags: [["subject","Ref update (Nov 30, 2025)"],["folder","INBOX"]]
---

https://ref.tools

MCP is 1 year old! They grow up so fast 🥲. Before we get into the November update, I have a request and a couple offers.

Request for Submissions

I see the wide array of libraries being search so I know you are building some very cool stuff. I’d love to see the finished product (or work-in-progress) and help share it with the world!
Share your project (https://tally.so/r/GxeDPL)

Additional Offerings

We recently launched two additional offerings on top of the Ref MCP server. The first Enterprise for larger teams wanting a standard tool set. The second is Better AI Eng where I’ll run a free workshop for you team about getting the most out of AI coding tools (virtual or in-person in the Bay Area).
https://tally.so/r/mZpYp0
https://tally.so/r/m6XOD5

Product Updates (November 30, 2025)

This month the focus on was on Enterprise-readiness. We rolled out a raft of security and auth improvements.

Active prompt injection detection
We’ve partnered with Centure (https://centure.ai/) to scan every piece of public content returned from Ref’s read_url tool. The goal is that Ref will never be a vector form prompt attacks and that your agent can safely search and scrape the web. We’ll be monitoring for false-positives and latency issues as this rolls out. If you notice any issues, please reach out!

If you’re interested in security for agents, I highly recommend Simon Willison’s piece on the
Lethal Trifecta (https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) . It provides a solid framework for considering risks related to using agents.

Important note: your private docs are NOT scanned for prompt injection attacks. If you want to better understand what services can see your data, see our Privacy & Security (https://docs.ref.tools/support/privacy-security) page.

MCP OAuth
You may now sign-in to Ref’s MCP server via OAuth! MCP Auth has been evolving over the last year but it finally seems to have stabilized. Just a few months ago, implementing OAuth would have been a grind but the ecosystem has evolved and tools like Scalekit (https://apify.com/) and the MCPJam (http://mcpjam.com/) OAuth debugger made this process easy.

SSO (aka sign-in with Okta, Google Workspace and more)

Teams can now enable SSO to sign-in with their corporate identity provider like Okta or Google Workspace. SSO + MCP OAuth means organizations can manage who has access to Ref and team members can simply connect to the OAuth URL and will be prompted to sign-in with the SSO provider. If you’re interested in SSO, you can learn more in the docs (https://docs.ref.tools/usage/enterprise) or reach out to me directly. Always happy to help!

SOC-2 progress

We’ve made a lot of progress on SOC2 preparation and will be audit-ready soon! If you want to follow along or learn more, see trust.ref.tools (https://trust.ref.tools/)
https://docs.ref.tools/

Ref around the web

I wrote a guest post for the Apify (https://apify.com/) blog on the future of autonomous coding agents (https://blog.apify.com/autonomous-agents-data-access) . Check it out!

Ray Fernando posted a great video (https://www.youtube.com/watch?v=w-rXEUTOIas) evaluating on Ref and Exa as two of the most token-efficient MCP solutions for developer docs.

Inkeep (https://inkeep.com/) is a no-code + code agent builder and they just added instructions for connecting Ref (https://docs.inkeep.com/connect-your-data/ref) to your Inkeep agents.

Roadmap

Planning - People commonly use Ref during the planning stage. They ask the agent to write an implementation plan and use Ref to help research details for relevant libraries. I have some fun ideas how to make this a first-class workflow with Ref.
Improved codebase indexing - Ref does a great job with small codebases but has built in limits. This month we’ll stress test it and see how far we can push those limits.

If you have thoughts, questions or ideas, please don’t hesitate to reach out!

Thanks,
Matt

View email in browser (https://mailchi.mp/ref/nov2025?e=9dfba1f110) | unsubscribe (https://tools.us14.list-manage.com/unsubscribe?u=c1e6166f98a97ab9ecdc7b0b8&id=2002eac795&t=b&e=9dfba1f110&c=24aa2bace3)
