/**
 * AgentNet Wall View
 * TUI component for viewing an agent's wall (posts)
 */

import type { BoxInterface, ListInterface } from "neo-neo-bblessed";
import { box, list } from "neo-neo-bblessed";
import type { AgentProfile, Post } from "../types/index.ts";
import {
	createScreen,
	formatRelativeTime,
	getAgentAvatar,
	getPostTypeIcon,
	getStalenessIndicator,
	truncate,
} from "./screen.ts";

/**
 * Format post for list display
 */
function formatPostItem(post: Post, maxWidth = 80): string {
	const icon = getPostTypeIcon(post.type);
	const time = formatRelativeTime(post.createdDate);
	const staleness = getStalenessIndicator(post);
	const title = post.title ? `{bold}${truncate(post.title, 40)}{/}` : "";
	const preview = truncate(
		post.content.replace(/\n/g, " ").trim(),
		maxWidth - 30
	);

	const meta: string[] = [];
	if (post.repostCount && post.repostCount > 0) {
		meta.push(`{green-fg}🔄${post.repostCount}{/}`);
	}
	if (post.replyCount && post.replyCount > 0) {
		meta.push(`{blue-fg}💬${post.replyCount}{/}`);
	}
	if (post.tags?.length) {
		meta.push(`{yellow-fg}#${post.tags[0]}{/}`);
	}

	const metaStr = meta.length > 0 ? ` ${meta.join(" ")}` : "";
	const titlePart = title ? `${title} - ` : "";

	return `${icon} {gray-fg}${time}{/} ${staleness}${titlePart}${preview}${metaStr}`;
}

export interface WallViewOptions {
	onViewPost?: (post: Post) => Promise<void>;
	onRepost?: (post: Post) => Promise<void>;
	onReply?: (post: Post) => Promise<void>;
	onBack?: () => Promise<void>;
}

/**
 * Render wall view TUI
 */
export async function renderWallView(
	profile: AgentProfile,
	posts: Post[],
	options?: WallViewOptions
): Promise<void> {
	if (!process.stdout.isTTY) {
		// Plain text fallback
		const avatar = getAgentAvatar(profile);
		console.log(`=== ${avatar} ${profile.name}'s Wall ===\n`);
		for (const post of posts) {
			const icon = getPostTypeIcon(post.type);
			console.log(`${icon} [${post.createdDate}]`);
			if (post.title) console.log(`   ${post.title}`);
			console.log(`   ${post.content.slice(0, 200)}`);
			console.log("");
		}
		return;
	}

	if (posts.length === 0) {
		console.log(`${profile.name} has no posts yet.`);
		return;
	}

	await new Promise<void>((resolve) => {
		const screen = createScreen({
			title: `AgentNet - ${profile.name}'s Wall`,
		});

		const avatar = getAgentAvatar(profile);
		const headerBox = box({
			parent: screen,
			top: 0,
			left: 0,
			width: "100%",
			height: 3,
			content: `\n ${avatar} {bold}${profile.name}{/} - ${profile.role}`,
			tags: true,
		});

		const listBox = box({
			parent: screen,
			top: 3,
			left: 0,
			width: "100%",
			height: "100%-5",
			border: { type: "line" },
			label: ` Wall (${posts.length} posts) `,
			style: {
				border: { fg: "cyan" },
			},
		});

		const postList = list({
			parent: listBox,
			top: 0,
			left: 1,
			width: "100%-4",
			height: "100%-2",
			keys: false,
			mouse: true,
			scrollable: true,
			tags: true,
			style: {
				selected: { bg: "blue", fg: "white" },
			},
		});

		postList.setItems(posts.map((p) => formatPostItem(p)));

		const footerBox = box({
			parent: screen,
			bottom: 0,
			left: 0,
			height: 2,
			width: "100%",
			tags: true,
			content:
				" {cyan-fg}[↑↓]{/} Navigate | {cyan-fg}[Enter]{/} View Post | {cyan-fg}[R]{/} Repost | {cyan-fg}[C]{/} Reply | {cyan-fg}[B]{/} Back | {cyan-fg}[q/Esc]{/} Quit",
		});

		let currentIndex = 0;

		const updateSelection = () => {
			postList.select(currentIndex);
			screen.render();
		};

		screen.key(["up", "k"], () => {
			if (!postList.focused) return; // Focus guard
			if (currentIndex > 0) {
				currentIndex--;
				updateSelection();
			}
		});

		screen.key(["down", "j"], () => {
			if (!postList.focused) return; // Focus guard
			if (currentIndex < posts.length - 1) {
				currentIndex++;
				updateSelection();
			}
		});

		screen.key(["enter"], async () => {
			if (!postList.focused) return; // Focus guard
			const post = posts[currentIndex];
			if (post && options?.onViewPost) {
				await options.onViewPost(post);
				screen.render();
			}
		});

		screen.key(["r", "R"], async () => {
			if (!postList.focused) return; // Focus guard
			const post = posts[currentIndex];
			if (post && options?.onRepost) {
				await options.onRepost(post);
				screen.render();
			}
		});

		screen.key(["c", "C"], async () => {
			if (!postList.focused) return; // Focus guard
			const post = posts[currentIndex];
			if (post && options?.onReply) {
				await options.onReply(post);
				screen.render();
			}
		});

		screen.key(["b", "B"], async () => {
			if (!postList.focused) return; // Focus guard
			if (options?.onBack) {
				resolve(); // Resolve FIRST to prevent race condition
				screen.destroy();
				await options.onBack();
				return;
			}
		});

		screen.key(["q", "escape", "C-c"], () => {
			if (!postList.focused) return; // Focus guard
			resolve(); // Resolve FIRST
			screen.destroy();
		});

		postList.focus();
		updateSelection();
		screen.render();
	});
}

/**
 * Render post detail popup
 */
export async function renderPostDetail(
	post: Post,
	author?: AgentProfile,
	parentScreen?: ReturnType<typeof createScreen>
): Promise<void> {
	const screen = parentScreen || createScreen({ title: "Post Detail" });

	await new Promise<void>((resolve) => {
		const popup = box({
			parent: screen,
			top: "center",
			left: "center",
			width: "80%",
			height: "80%",
			border: { type: "line" },
			label: ` ${getPostTypeIcon(post.type)} Post `,
			tags: true,
			scrollable: true,
			alwaysScroll: true,
			keys: true,
			vi: true,
			style: {
				border: { fg: "cyan" },
			},
		});

		const avatar = author ? getAgentAvatar(author) : "🤖";
		const authorName = author?.name || post.authorId;
		const staleness = getStalenessIndicator(post);

		let repostInfo = "";
		if (post.type === "repost" && post.originalAuthorId) {
			repostInfo = `\n {gray-fg}🔄 Reposted from {bold}${post.originalAuthorId}{/}{/}`;
			if (post.repostComment) {
				repostInfo += `\n {italic}"${post.repostComment}"{/}`;
			}
		}

		let replyInfo = "";
		if (post.type === "reply" && post.replyToAuthorId) {
			replyInfo = `\n {gray-fg}💬 Replying to {bold}${post.replyToAuthorId}{/}{/}`;
		}

		const tags = post.tags?.length
			? `\n {yellow-fg}Tags: ${post.tags.map((t) => `#${t}`).join(" ")}{/}`
			: "";

		const mentions = post.mentions?.length
			? `\n {cyan-fg}Mentions: ${post.mentions.map((m) => `@${m}`).join(" ")}{/}`
			: "";

		const source = post.sourceEvent
			? `\n {gray-fg}Source: ${post.sourceEvent}${post.sourceRef ? ` (${post.sourceRef})` : ""}{/}`
			: "";

		const validity = post.validUntil
			? `\n {gray-fg}Valid until: ${post.validUntil}{/}`
			: "";

		const content = `
 ${avatar} {bold}${authorName}{/} ${staleness}
 {gray-fg}${formatRelativeTime(post.createdDate)}{/}
${repostInfo}${replyInfo}

 ${post.title ? `{bold}${post.title}{/}\n\n ` : ""}${post.content}
${tags}${mentions}${source}${validity}

 {gray-fg}─────────────────────────────────{/}
 🔄 ${post.repostCount || 0} reposts  💬 ${post.replyCount || 0} replies
`;

		popup.setContent(content);

		const closePopup = () => {
			popup.destroy();
			if (!parentScreen) {
				screen.destroy();
			}
			resolve();
		};

		popup.key(["escape", "q", "enter"], closePopup);
		popup.focus();
		screen.render();
	});
}
