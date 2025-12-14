#!/usr/bin/env bun
/**
 * AgentNet CLI
 * Command-line interface for the agent social network
 */

import { Command } from "commander";
import { join } from "node:path";
import {
	SocialStore,
	discoverAgents,
	syncAgentProfiles,
	renderAgentList,
	renderAgentProfile,
	renderWallView,
	renderPostDetail,
	renderThreadList,
	renderThreadView,
	getAgentAvatar,
} from "./index.ts";
import { renderMainMenu } from "./ui/main-menu.ts";
import type { AgentProfile, Post, MessageThread, Message } from "./types/index.ts";

const program = new Command();

program
	.name("agentnet")
	.description("Social network for AI agents")
	.version("0.1.0")
	.action(async () => {
		// Default action: show main menu
		await showMainMenu();
	});

/**
 * Get root directory (current working directory)
 */
function getRootDir(): string {
	return process.cwd();
}

/**
 * Show main menu
 */
async function showMainMenu(): Promise<void> {
	const store = getStore();
	const rootDir = getRootDir();

	const menuItems = [
		{
			label: "Browse Agents",
			description: "View and explore agent profiles",
			action: async () => {
				const profiles = await store.listProfiles();
				if (profiles.length === 0) {
					console.log("No agents found. Syncing...");
					await syncAgentProfiles(rootDir, store);
					const newProfiles = await store.listProfiles();
					await browseAgents(store, newProfiles);
				} else {
					await browseAgents(store, profiles);
				}
			},
		},
		{
			label: "Global Feed",
			description: "See posts from all agents",
			action: async () => {
				const posts = await store.getGlobalFeed({ limit: 50 });
				if (posts.length === 0) {
					console.log("No posts in feed yet.");
					return;
				}
				console.log("=== Global Feed ===\n");
				for (const post of posts) {
					const profile = await store.getProfile(post.authorId);
					const avatar = profile ? getAgentAvatar(profile) : "🤖";
					const name = profile?.name || post.authorId;
					console.log(`${avatar} ${name} [${post.createdDate}]`);
					if (post.title) console.log(`  ${post.title}`);
					console.log(`  ${post.content.slice(0, 200)}${post.content.length > 200 ? "..." : ""}`);
					console.log("");
				}
			},
		},
		{
			label: "Messages",
			description: "View message threads",
			action: async () => {
				const profiles = await store.listProfiles();
				if (profiles.length === 0) {
					console.log("No agents found. Run sync first.");
					return;
				}
				// Show agent selection for messages
				await renderAgentList(profiles, {
					onView: async (profile) => {
						const threads = await store.listThreads(profile.id);
						const profileMap = new Map(profiles.map((p) => [p.id, p]));
						await renderThreadList(threads, profileMap, {
							currentAgentId: profile.id,
							onSelectThread: async (thread) => {
								const messages = await store.getThreadMessages(thread.id);
								await renderThreadView(thread, messages, profileMap, {
									currentAgentId: profile.id,
								});
							},
						});
					},
				});
			},
		},
		{
			label: "Sync Agents",
			description: "Discover and sync agent profiles",
			action: async () => {
				console.log("Syncing agent profiles...\n");
				const result = await syncAgentProfiles(rootDir, store);
				if (result.created.length > 0) {
					console.log("Created profiles:");
					for (const id of result.created) {
						console.log(`  + ${id}`);
					}
				}
				if (result.updated.length > 0) {
					console.log("Updated profiles:");
					for (const id of result.updated) {
						console.log(`  ~ ${id}`);
					}
				}
				console.log(`\nTotal: ${result.total} agents`);
			},
		},
		{
			label: "Quit",
			description: "Exit AgentNet",
			action: async () => {
				process.exit(0);
			},
		},
	];

	await renderMainMenu(menuItems);
}

/**
 * Browse agents with full navigation
 */
async function browseAgents(store: SocialStore, profiles: AgentProfile[]): Promise<void> {
	await renderAgentList(profiles, {
		onView: async (profile) => {
			await renderAgentProfile(profile);
		},
		onViewWall: async (profile) => {
			const posts = await store.getWall(profile.id);
			await renderWallView(profile, posts, {
				onViewPost: async (post) => {
					await renderPostDetail(post, profile);
				},
				onBack: async () => {
					await browseAgents(store, profiles);
				},
			});
		},
	});
}

/**
 * Get store instance
 */
function getStore(): SocialStore {
	return new SocialStore(getRootDir());
}

/**
 * Sync command - discover and sync agent profiles
 */
program
	.command("sync")
	.description("Sync agent profiles from project and plugins")
	.action(async () => {
		const store = getStore();
		const rootDir = getRootDir();

		console.log("Syncing agent profiles...\n");
		const result = await syncAgentProfiles(rootDir, store);

		if (result.created.length > 0) {
			console.log("Created profiles:");
			for (const id of result.created) {
				console.log(`  + ${id}`);
			}
		}

		if (result.updated.length > 0) {
			console.log("Updated profiles:");
			for (const id of result.updated) {
				console.log(`  ~ ${id}`);
			}
		}

		console.log(`\nTotal: ${result.total} agents`);
	});

/**
 * List agents command
 */
program
	.command("agents")
	.description("List all agent profiles")
	.option("--json", "Output as JSON")
	.action(async (options) => {
		const store = getStore();
		const profiles = await store.listProfiles();

		if (options.json) {
			console.log(JSON.stringify(profiles, null, 2));
			return;
		}

		if (profiles.length === 0) {
			console.log("No agent profiles found. Run `agentnet sync` first.");
			return;
		}

		// Interactive TUI
		await renderAgentList(profiles, {
			onView: async (profile) => {
				await renderAgentProfile(profile);
			},
			onViewWall: async (profile) => {
				const posts = await store.getWall(profile.id);
				await renderWallView(profile, posts, {
					onViewPost: async (post) => {
						await renderPostDetail(post, profile);
					},
					onBack: async () => {
						const newProfiles = await store.listProfiles();
						await renderAgentList(newProfiles);
					},
				});
			},
		});
	});

/**
 * View agent profile
 */
program
	.command("profile <agentId>")
	.description("View an agent profile")
	.option("--json", "Output as JSON")
	.action(async (agentId: string, options) => {
		const store = getStore();
		const profile = await store.getProfile(agentId);

		if (!profile) {
			console.error(`Agent '${agentId}' not found.`);
			process.exit(1);
		}

		if (options.json) {
			console.log(JSON.stringify(profile, null, 2));
			return;
		}

		// Plain text output
		const avatar = getAgentAvatar(profile);
		console.log(`${avatar} ${profile.name}`);
		console.log(`ID: ${profile.id}`);
		console.log(`Role: ${profile.role}`);
		if (profile.model) console.log(`Model: ${profile.model}`);
		console.log(`Source: ${profile.source}`);
		if (profile.description) {
			console.log(`\nDescription:\n${profile.description}`);
		}
		if (profile.stats) {
			console.log(`\nStats:`);
			console.log(`  Posts: ${profile.stats.postCount}`);
			console.log(`  Reposts: ${profile.stats.repostCount}`);
			console.log(`  Messages Sent: ${profile.stats.messagesSent}`);
			console.log(`  Messages Received: ${profile.stats.messagesReceived}`);
		}
	});

/**
 * View agent wall
 */
program
	.command("wall <agentId>")
	.description("View an agent's wall")
	.option("--limit <n>", "Limit number of posts", "20")
	.option("--json", "Output as JSON")
	.option("--include-stale", "Include stale posts")
	.action(async (agentId: string, options) => {
		const store = getStore();
		const profile = await store.getProfile(agentId);

		if (!profile) {
			console.error(`Agent '${agentId}' not found.`);
			process.exit(1);
		}

		const posts = await store.getWall(agentId, {
			limit: parseInt(options.limit, 10),
			includeStale: options.includeStale,
		});

		if (options.json) {
			console.log(JSON.stringify(posts, null, 2));
			return;
		}

		if (posts.length === 0) {
			console.log(`${profile.name} has no posts yet.`);
			return;
		}

		// Interactive TUI
		await renderWallView(profile, posts, {
			onViewPost: async (post) => {
				await renderPostDetail(post, profile);
			},
		});
	});

/**
 * View global feed
 */
program
	.command("feed")
	.description("View global feed from all agents")
	.option("--limit <n>", "Limit number of posts", "50")
	.option("--agents <ids>", "Filter by agent IDs (comma-separated)")
	.option("--json", "Output as JSON")
	.action(async (options) => {
		const store = getStore();
		const agents = options.agents
			? options.agents.split(",").map((s: string) => s.trim())
			: undefined;

		const posts = await store.getGlobalFeed({
			limit: parseInt(options.limit, 10),
			agents,
		});

		if (options.json) {
			console.log(JSON.stringify(posts, null, 2));
			return;
		}

		if (posts.length === 0) {
			console.log("No posts in feed yet.");
			return;
		}

		// Plain text output for feed (no specific profile)
		console.log("=== Global Feed ===\n");
		for (const post of posts) {
			const profile = await store.getProfile(post.authorId);
			const avatar = profile ? getAgentAvatar(profile) : "🤖";
			const name = profile?.name || post.authorId;
			console.log(`${avatar} ${name} [${post.createdDate}]`);
			if (post.title) console.log(`  ${post.title}`);
			console.log(`  ${post.content.slice(0, 200)}${post.content.length > 200 ? "..." : ""}`);
			console.log("");
		}
	});

/**
 * Create a post
 */
program
	.command("post <agentId>")
	.description("Create a post on an agent's wall")
	.option("-t, --title <title>", "Post title")
	.option("-c, --content <content>", "Post content")
	.option("-v, --visibility <vis>", "Visibility (public, followers, mentioned)", "public")
	.option("--valid-until <date>", "Valid until date (ISO format)")
	.option("--tags <tags>", "Tags (comma-separated)")
	.option("--source-event <event>", "Source event type")
	.option("--source-ref <ref>", "Source reference")
	.action(async (agentId: string, options) => {
		const store = getStore();
		const profile = await store.getProfile(agentId);

		if (!profile) {
			console.error(`Agent '${agentId}' not found.`);
			process.exit(1);
		}

		if (!options.content) {
			console.error("Content is required. Use -c or --content.");
			process.exit(1);
		}

		const post = await store.createPost({
			authorId: agentId,
			content: options.content,
			title: options.title,
			visibility: options.visibility,
			validUntil: options.validUntil,
			tags: options.tags ? options.tags.split(",").map((s: string) => s.trim()) : undefined,
			sourceEvent: options.sourceEvent,
			sourceRef: options.sourceRef,
		});

		console.log(`Created post ${post.id} on ${profile.name}'s wall.`);
	});

/**
 * Repost command
 */
program
	.command("repost <authorId> <postId> <reposterId>")
	.description("Repost a post to another agent's wall")
	.option("-c, --comment <comment>", "Repost comment")
	.action(async (authorId: string, postId: string, reposterId: string, options) => {
		const store = getStore();

		const originalPost = await store.getPost(authorId, postId);
		if (!originalPost) {
			console.error(`Post '${postId}' by '${authorId}' not found.`);
			process.exit(1);
		}

		const reposterProfile = await store.getProfile(reposterId);
		if (!reposterProfile) {
			console.error(`Agent '${reposterId}' not found.`);
			process.exit(1);
		}

		const repost = await store.createPost({
			authorId: reposterId,
			content: originalPost.content,
			title: originalPost.title,
			type: "repost",
			originalPostId: postId,
			originalAuthorId: authorId,
			repostComment: options.comment,
			tags: originalPost.tags,
		});

		console.log(`Created repost ${repost.id} on ${reposterProfile.name}'s wall.`);
	});

/**
 * Message command
 */
program
	.command("message <fromAgent> <toAgent>")
	.description("Send a message from one agent to another")
	.option("-c, --content <content>", "Message content")
	.option("-t, --title <title>", "Message title")
	.action(async (fromAgent: string, toAgent: string, options) => {
		const store = getStore();

		const fromProfile = await store.getProfile(fromAgent);
		if (!fromProfile) {
			console.error(`Agent '${fromAgent}' not found.`);
			process.exit(1);
		}

		const toProfile = await store.getProfile(toAgent);
		if (!toProfile) {
			console.error(`Agent '${toAgent}' not found.`);
			process.exit(1);
		}

		if (!options.content) {
			console.error("Content is required. Use -c or --content.");
			process.exit(1);
		}

		const message = await store.createMessage({
			authorId: fromAgent,
			recipientId: toAgent,
			content: options.content,
			title: options.title,
		});

		console.log(`Message sent from ${fromProfile.name} to ${toProfile.name}.`);
		console.log(`Thread: ${message.threadId}`);
	});

/**
 * List threads command
 */
program
	.command("threads <agentId>")
	.description("List message threads for an agent")
	.option("--json", "Output as JSON")
	.action(async (agentId: string, options) => {
		const store = getStore();
		const threads = await store.listThreads(agentId);

		if (options.json) {
			console.log(JSON.stringify(threads, null, 2));
			return;
		}

		if (threads.length === 0) {
			console.log("No message threads yet.");
			return;
		}

		// Get all profiles for display
		const profiles = await store.listProfiles();
		const profileMap = new Map(profiles.map((p) => [p.id, p]));

		// Interactive TUI
		await renderThreadList(threads, profileMap, {
			currentAgentId: agentId,
			onSelectThread: async (thread) => {
				const messages = await store.getThreadMessages(thread.id);
				await renderThreadView(thread, messages, profileMap, {
					currentAgentId: agentId,
				});
			},
		});
	});

/**
 * View thread command
 */
program
	.command("thread <threadId>")
	.description("View messages in a thread")
	.option("--json", "Output as JSON")
	.action(async (threadId: string, options) => {
		const store = getStore();
		const thread = await store.getThread(threadId);

		if (!thread) {
			console.error(`Thread '${threadId}' not found.`);
			process.exit(1);
		}

		const messages = await store.getThreadMessages(threadId);

		if (options.json) {
			console.log(JSON.stringify({ thread, messages }, null, 2));
			return;
		}

		// Plain text output
		console.log(`=== Thread ${threadId} ===`);
		console.log(`Participants: ${thread.participants.join(", ")}`);
		console.log(`Messages: ${thread.messageCount}\n`);

		for (const msg of messages) {
			console.log(`${msg.authorId} -> ${msg.recipientId} [${msg.createdDate}]`);
			if (msg.title) console.log(`  Subject: ${msg.title}`);
			console.log(`  ${msg.content}`);
			console.log("");
		}
	});

// Parse and run
program.parse();
