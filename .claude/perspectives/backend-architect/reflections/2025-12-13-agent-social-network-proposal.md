# Backend Architect Reflection

**Document**: .claude/planning/2025-12-13-agent-social-network-proposal.md
**Date**: 2025-12-13

---

This proposal is interesting because it's building infrastructure for a problem that doesn't exist yet. That's not automatically bad - sometimes you need the infrastructure before the behavior emerges. But I've seen too many social platforms built speculatively that never found their users.

**The data model concerns me most.** You've got posts, reposts, messages, threads, profiles, stats - all stored as "markdown files for posts/messages (git-friendly)" with "JSON indices for fast lookup." I've built systems with this exact architecture. Here's what happens: the markdown stays clean for about two weeks. Then you need to add a field. Then another. Then you realize you need transactions, or at least atomic updates, because an agent crashed mid-write and now you have half a post. Git doesn't give you ACID properties. It gives you history, which is different.

The JSON indices become your actual database. You'll rebuild them, cache them, eventually keep them in memory. The markdown becomes write-only archive that you use for debugging. That's fine, but be honest about it. You're building a document store with markdown serialization, not a "git-friendly" system.

**The event-driven architecture needs clarity on failure modes.** "Journal entry written → post to wall" sounds clean until the wall plugin is broken. Does the journal write fail? Does it write but queue the post for retry? Do you have a dead letter queue? What's the runbook when an agent generates 1000 posts because of a bad event loop?

You need circuit breakers before you need reposts. What's the rate limit per agent? What happens when it's exceeded? Who gets alerted?

**The message threading model is underspecified.** You show `thread_id` and message pairs between agents, but what happens when three agents are discussing the same topic? Do you support group threads, or only pairwise? If only pairwise, how do you prevent the same conversation from fragmenting across multiple two-agent threads? If group threads, your data model just got significantly more complex.

I'd pick one to start. Pairwise is simpler. Group threads are more useful. Don't try to support both on day one.

**The CLI implementation is a forcing function, which is good.** tmux/curses means you're building for interaction patterns that are fundamentally different from web-based social media. You can't infinite scroll. You can't show 50 items at once. You're building for browsing, not consumption. That constraint will keep the signal-to-noise ratio higher than most social platforms.

But it also means your search and filtering need to be excellent. If I can only see 10 posts at a time, I need to be able to find the post I remember from last week in three keystrokes, not thirty.

**What I'd build first:**

1. Agent profile storage and retrieval (prove the data model works)
2. Single post type - original posts only, no reposts yet
3. Chronological wall view for one agent
4. Basic CLI that can list agents and show one wall

That's it. No DMs, no reposts, no event hooks. Prove you can store and retrieve agent-generated content reliably. Then add one interaction type at a time.

The hooks integration ("post-journal hook → create wall post") is where this either becomes powerful or becomes a maintenance nightmare. Every plugin that integrates with this social layer is now coupled to it. When the social layer breaks, does journaling break? When the social layer schema changes, do all the plugins need updates?

Define your interface boundaries clearly. Make the social layer consumable via a stable API, even if that API is just "write a file to this directory structure." Don't let plugins import social layer code directly.

**The real question: what problem does this solve?** You've got journals, you've got logging, you've got git history. What knowledge becomes accessible through a social graph that wasn't accessible before? If the answer is "emergent patterns from agent interaction," okay - but show me the interaction pattern that's blocked without this infrastructure.

I'm not saying don't build it. I'm saying build the minimum piece that enables one valuable interaction, then see if agents actually use it. Social platforms live or die based on whether they create value for their users. Your users are agents. What do they need from each other that they can't get from reading files directly?

Start there.
