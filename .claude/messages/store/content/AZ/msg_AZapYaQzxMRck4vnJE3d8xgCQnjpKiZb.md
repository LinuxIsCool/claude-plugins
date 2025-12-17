---
id: msg_AZapYaQzxMRck4vnJE3d8xgCQnjpKiZb
kind: 102
account_id: user
created_at: 1765820376389
imported_at: 1766005510801
author_name: User
thread_id: cc_dcb257e6
platform: claude-code
session_id: dcb257e6-d74b-4796-9a81-10ee1e9c3413
tags: [["event_type","UserPromptSubmit"]]
---

I was trying to push but got the following: 
ygg@pop-os ~/Workspace/sandbox/marketplaces/claude [main] 🪷 git push origin main                                                          (base) ⌚ 09:38:51
Enumerating objects: 2876, done.
Counting objects: 100% (2876/2876), done.
Delta compression using up to 24 threads
Compressing objects: 100% (2642/2642), done.
Writing objects: 100% (2861/2861), 12.40 MiB | 9.13 MiB/s, done.
Total 2861 (delta 590), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (590/590), completed with 4 local objects.
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote:
remote: - GITHUB PUSH PROTECTION
remote:   —————————————————————————————————————————
remote:     Resolve the following violations before pushing again
remote:
remote:     - Push cannot contain secrets
remote:
remote:
remote:      (?) Learn how to resolve a blocked push
remote:      https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line#resolving-a-blocked-push
remote:
remote:
remote:       —— Discord Bot Token —————————————————————————————————
remote:        locations:
remote:          - commit: 7345f6e2f6c69a378a7ce5d99d97e01e0dd79538
remote:            path: plugins/agentnet/node_modules/bun-types/docs/guides/ecosystem/discordjs.mdx:34
remote:
remote:        (?) To push, remove secret from commit(s) or follow this URL to allow the secret.
remote:        https://github.com/LinuxIsCool/claude-plugins/security/secret-scanning/unblock-secret/36tKHHxKfzuRQS93Kcd4itmVs5J
remote:
remote:
remote:
To github.com:LinuxIsCool/claude-plugins.git
 ! [remote rejected] main -> main (push declined due to repository rule violations)
error: failed to push some refs to 'github.com:LinuxIsCool/claude-plugins.git'

