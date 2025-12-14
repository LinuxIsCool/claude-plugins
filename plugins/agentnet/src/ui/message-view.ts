/**
 * AgentNet Message View
 * TUI component for viewing and sending messages (DMs)
 */

import type { BoxInterface, ListInterface } from "neo-neo-bblessed";
import { box, list } from "neo-neo-bblessed";
import type { AgentProfile, Message, MessageThread } from "../types/index.ts";
import {
	createScreen,
	formatRelativeTime,
	getAgentAvatar,
	truncate,
} from "./screen.ts";

/**
 * Format thread for list display
 */
function formatThreadItem(
	thread: MessageThread,
	currentAgentId: string,
	profiles: Map<string, AgentProfile>
): string {
	const otherParticipants = thread.participants.filter(
		(p) => p !== currentAgentId
	);
	const otherNames = otherParticipants
		.map((p) => {
			const profile = profiles.get(p);
			return profile ? `${getAgentAvatar(profile)} ${profile.name}` : p;
		})
		.join(", ");

	const time = thread.lastMessageDate
		? formatRelativeTime(thread.lastMessageDate)
		: formatRelativeTime(thread.createdDate);

	const unread =
		thread.unreadCount && thread.unreadCount > 0
			? `{red-fg}(${thread.unreadCount} new){/}`
			: "";

	const title = thread.title ? `{gray-fg}${truncate(thread.title, 30)}{/}` : "";

	return `${otherNames} ${unread} {gray-fg}${time}{/} ${title}`;
}

/**
 * Format message for display
 */
function formatMessage(
	message: Message,
	profiles: Map<string, AgentProfile>,
	isOwn: boolean
): string {
	const profile = profiles.get(message.authorId);
	const avatar = profile ? getAgentAvatar(profile) : "🤖";
	const name = profile?.name || message.authorId;
	const time = formatRelativeTime(message.createdDate);
	const readStatus = message.readAt
		? "{green-fg}✓{/}"
		: "{gray-fg}○{/}";

	const align = isOwn ? "{right}" : "";
	const color = isOwn ? "{cyan-fg}" : "{white-fg}";

	return `${align}${avatar} {bold}${name}{/} {gray-fg}${time}{/} ${isOwn ? readStatus : ""}
${color}${message.content}{/}
`;
}

export interface ThreadListOptions {
	currentAgentId: string;
	onSelectThread?: (thread: MessageThread) => Promise<void>;
	onNewThread?: () => Promise<void>;
	onBack?: () => Promise<void>;
}

/**
 * Render thread list TUI
 */
export async function renderThreadList(
	threads: MessageThread[],
	profiles: Map<string, AgentProfile>,
	options: ThreadListOptions
): Promise<void> {
	if (!process.stdout.isTTY) {
		// Plain text fallback
		console.log("=== Message Threads ===\n");
		for (const thread of threads) {
			const others = thread.participants
				.filter((p) => p !== options.currentAgentId)
				.join(", ");
			console.log(`📬 ${others}`);
			console.log(`   ${thread.messageCount} messages`);
			if (thread.lastMessageDate) {
				console.log(`   Last: ${thread.lastMessageDate}`);
			}
			console.log("");
		}
		return;
	}

	if (threads.length === 0) {
		console.log("No message threads yet.");
		return;
	}

	await new Promise<void>((resolve) => {
		const screen = createScreen({ title: "AgentNet - Messages" });

		const headerBox = box({
			parent: screen,
			top: 0,
			left: 0,
			width: "100%",
			height: 3,
			content: "\n {bold}AgentNet{/} - Message Threads",
			tags: true,
		});

		const listBox = box({
			parent: screen,
			top: 3,
			left: 0,
			width: "100%",
			height: "100%-5",
			border: { type: "line" },
			label: ` Threads (${threads.length}) `,
			style: {
				border: { fg: "cyan" },
			},
		});

		const threadList = list({
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

		threadList.setItems(
			threads.map((t) =>
				formatThreadItem(t, options.currentAgentId, profiles)
			)
		);

		const footerBox = box({
			parent: screen,
			bottom: 0,
			left: 0,
			height: 2,
			width: "100%",
			tags: true,
			content:
				" {cyan-fg}[↑↓]{/} Navigate | {cyan-fg}[Enter]{/} Open Thread | {cyan-fg}[N]{/} New Thread | {cyan-fg}[B]{/} Back | {cyan-fg}[q/Esc]{/} Quit",
		});

		let currentIndex = 0;

		const updateSelection = () => {
			threadList.select(currentIndex);
			screen.render();
		};

		screen.key(["up", "k"], () => {
			if (currentIndex > 0) {
				currentIndex--;
				updateSelection();
			}
		});

		screen.key(["down", "j"], () => {
			if (currentIndex < threads.length - 1) {
				currentIndex++;
				updateSelection();
			}
		});

		screen.key(["enter"], async () => {
			const thread = threads[currentIndex];
			if (thread && options.onSelectThread) {
				screen.destroy();
				await options.onSelectThread(thread);
				resolve();
			}
		});

		screen.key(["n", "N"], async () => {
			if (options.onNewThread) {
				await options.onNewThread();
				screen.render();
			}
		});

		screen.key(["b", "B"], async () => {
			if (options.onBack) {
				screen.destroy();
				await options.onBack();
				resolve();
				return;
			}
		});

		screen.key(["q", "escape", "C-c"], () => {
			screen.destroy();
			resolve();
		});

		threadList.focus();
		updateSelection();
		screen.render();
	});
}

export interface ThreadViewOptions {
	currentAgentId: string;
	onSendMessage?: (content: string) => Promise<void>;
	onBack?: () => Promise<void>;
}

/**
 * Render thread view TUI
 */
export async function renderThreadView(
	thread: MessageThread,
	messages: Message[],
	profiles: Map<string, AgentProfile>,
	options: ThreadViewOptions
): Promise<void> {
	if (!process.stdout.isTTY) {
		// Plain text fallback
		const others = thread.participants
			.filter((p) => p !== options.currentAgentId)
			.join(", ");
		console.log(`=== Thread with ${others} ===\n`);
		for (const msg of messages) {
			const profile = profiles.get(msg.authorId);
			const name = profile?.name || msg.authorId;
			console.log(`${name} [${msg.createdDate}]:`);
			console.log(`  ${msg.content}`);
			console.log("");
		}
		return;
	}

	await new Promise<void>((resolve) => {
		const screen = createScreen({ title: "AgentNet - Thread" });

		const otherParticipants = thread.participants.filter(
			(p) => p !== options.currentAgentId
		);
		const otherNames = otherParticipants
			.map((p) => {
				const profile = profiles.get(p);
				return profile
					? `${getAgentAvatar(profile)} ${profile.name}`
					: p;
			})
			.join(", ");

		const headerBox = box({
			parent: screen,
			top: 0,
			left: 0,
			width: "100%",
			height: 3,
			content: `\n {bold}Thread with{/} ${otherNames}`,
			tags: true,
		});

		const messageBox = box({
			parent: screen,
			top: 3,
			left: 0,
			width: "100%",
			height: "100%-7",
			border: { type: "line" },
			label: ` Messages (${messages.length}) `,
			tags: true,
			scrollable: true,
			alwaysScroll: true,
			keys: true,
			vi: true,
			style: {
				border: { fg: "cyan" },
			},
		});

		const messageContent = messages
			.map((m) =>
				formatMessage(m, profiles, m.authorId === options.currentAgentId)
			)
			.join("\n");

		messageBox.setContent(messageContent);
		messageBox.setScrollPerc(100); // Scroll to bottom

		const footerBox = box({
			parent: screen,
			bottom: 0,
			left: 0,
			height: 4,
			width: "100%",
			tags: true,
			content:
				"\n {cyan-fg}[↑↓/j/k]{/} Scroll | {cyan-fg}[B]{/} Back | {cyan-fg}[q/Esc]{/} Quit\n {gray-fg}(Message composition coming soon){/}",
		});

		screen.key(["up", "k"], () => {
			messageBox.scroll(-1);
			screen.render();
		});

		screen.key(["down", "j"], () => {
			messageBox.scroll(1);
			screen.render();
		});

		screen.key(["pageup"], () => {
			messageBox.scroll(-10);
			screen.render();
		});

		screen.key(["pagedown"], () => {
			messageBox.scroll(10);
			screen.render();
		});

		screen.key(["b", "B"], async () => {
			if (options.onBack) {
				screen.destroy();
				await options.onBack();
				resolve();
				return;
			}
		});

		screen.key(["q", "escape", "C-c"], () => {
			screen.destroy();
			resolve();
		});

		messageBox.focus();
		screen.render();
	});
}
