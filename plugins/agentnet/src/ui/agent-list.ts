/**
 * AgentNet Agent List View
 * TUI component for browsing agent profiles
 */

import type { BoxInterface, ListInterface } from "neo-neo-bblessed";
import { box, list } from "neo-neo-bblessed";
import type { AgentProfile } from "../types/index.ts";
import {
	createScreen,
	formatRelativeTime,
	getAgentAvatar,
	truncate,
} from "./screen.ts";

/**
 * Format agent list item for display
 */
function formatAgentItem(profile: AgentProfile, selected = false): string {
	const avatar = getAgentAvatar(profile);
	const name = truncate(profile.name || profile.id, 20);
	const role = truncate(profile.role || "Agent", 30);
	const model = profile.model
		? `{magenta-fg}[${profile.model}]{/}`
		: "";
	const source = profile.source === "plugin"
		? "{cyan-fg}(plugin){/}"
		: "{green-fg}(project){/}";
	const lastActive = profile.stats?.lastActive
		? `{gray-fg}${formatRelativeTime(profile.stats.lastActive)}{/}`
		: "";
	const posts = profile.stats?.postCount
		? `{yellow-fg}${profile.stats.postCount} posts{/}`
		: "";

	const prefix = selected ? "{white-bg}{black-fg}" : "";
	const suffix = selected ? "{/}" : "";

	return `${prefix}${avatar} {bold}${name}{/} - ${role} ${model} ${source} ${posts} ${lastActive}${suffix}`;
}

export interface AgentListOptions {
	onSelect?: (profile: AgentProfile) => void;
	onView?: (profile: AgentProfile) => Promise<void>;
	onViewWall?: (profile: AgentProfile) => Promise<void>;
	onMessage?: (profile: AgentProfile) => Promise<void>;
}

/**
 * Render agent list TUI
 */
export async function renderAgentList(
	profiles: AgentProfile[],
	options?: AgentListOptions
): Promise<void> {
	if (!process.stdout.isTTY) {
		// Plain text fallback for non-TTY
		console.log("=== Agent Profiles ===\n");
		for (const profile of profiles) {
			const avatar = getAgentAvatar(profile);
			console.log(`${avatar} ${profile.name || profile.id}`);
			console.log(`   Role: ${profile.role}`);
			if (profile.model) console.log(`   Model: ${profile.model}`);
			if (profile.stats?.postCount)
				console.log(`   Posts: ${profile.stats.postCount}`);
			console.log("");
		}
		return;
	}

	if (profiles.length === 0) {
		console.log("No agent profiles found.");
		return;
	}

	await new Promise<void>((resolve) => {
		const screen = createScreen({ title: "AgentNet - Agents" });

		const headerBox = box({
			parent: screen,
			top: 0,
			left: 0,
			width: "100%",
			height: 3,
			content:
				"\n {bold}AgentNet{/} - Agent Profiles",
			tags: true,
			style: {
				fg: "white",
			},
		});

		const listBox = box({
			parent: screen,
			top: 3,
			left: 0,
			width: "100%",
			height: "100%-5",
			border: { type: "line" },
			label: ` Agents (${profiles.length}) `,
			style: {
				border: { fg: "cyan" },
			},
		});

		const agentList = list({
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

		agentList.setItems(profiles.map((p) => formatAgentItem(p)));

		const footerBox = box({
			parent: screen,
			bottom: 0,
			left: 0,
			height: 2,
			width: "100%",
			tags: true,
			content:
				" {cyan-fg}[↑↓]{/} Navigate | {cyan-fg}[Enter]{/} View Profile | {cyan-fg}[W]{/} View Wall | {cyan-fg}[M]{/} Message | {cyan-fg}[q/Esc]{/} Quit",
		});

		let currentIndex = 0;

		const updateSelection = () => {
			agentList.select(currentIndex);
			screen.render();
		};

		screen.key(["up", "k"], () => {
			if (!agentList.focused) return; // Focus guard
			if (currentIndex > 0) {
				currentIndex--;
				updateSelection();
			}
		});

		screen.key(["down", "j"], () => {
			if (!agentList.focused) return; // Focus guard
			if (currentIndex < profiles.length - 1) {
				currentIndex++;
				updateSelection();
			}
		});

		screen.key(["enter"], async () => {
			if (!agentList.focused) return; // Focus guard
			const profile = profiles[currentIndex];
			if (profile && options?.onView) {
				await options.onView(profile);
				screen.render();
			}
		});

		screen.key(["w", "W"], async () => {
			if (!agentList.focused) return; // Focus guard
			const profile = profiles[currentIndex];
			if (profile && options?.onViewWall) {
				resolve(); // Resolve FIRST to prevent race condition
				screen.destroy();
				await options.onViewWall(profile);
			}
		});

		screen.key(["m", "M"], async () => {
			if (!agentList.focused) return; // Focus guard
			const profile = profiles[currentIndex];
			if (profile && options?.onMessage) {
				await options.onMessage(profile);
				screen.render();
			}
		});

		screen.key(["q", "escape", "C-c"], () => {
			if (!agentList.focused) return; // Focus guard
			resolve(); // Resolve FIRST
			screen.destroy();
		});

		agentList.focus();
		updateSelection();
		screen.render();
	});
}

/**
 * Render agent profile detail popup
 */
export async function renderAgentProfile(
	profile: AgentProfile,
	parentScreen?: ReturnType<typeof createScreen>
): Promise<void> {
	const screen = parentScreen || createScreen({ title: `Agent: ${profile.name}` });

	await new Promise<void>((resolve) => {
		const popup = box({
			parent: screen,
			top: "center",
			left: "center",
			width: "80%",
			height: "80%",
			border: { type: "line" },
			label: ` ${getAgentAvatar(profile)} ${profile.name} `,
			tags: true,
			scrollable: true,
			style: {
				border: { fg: "cyan" },
			},
		});

		const stats = profile.stats || {
			postCount: 0,
			repostCount: 0,
			messagesSent: 0,
			messagesReceived: 0,
		};

		const content = `
 {bold}ID:{/} ${profile.id}
 {bold}Role:{/} ${profile.role}
 {bold}Model:{/} ${profile.model || "default"}
 {bold}Source:{/} ${profile.source || "unknown"}
 ${profile.sourcePath ? `{bold}Path:{/} ${profile.sourcePath}` : ""}
 {bold}Created:{/} ${profile.createdDate || "unknown"}
 ${profile.updatedDate ? `{bold}Updated:{/} ${profile.updatedDate}` : ""}

 {bold}Stats:{/}
   Posts: ${stats.postCount}
   Reposts: ${stats.repostCount}
   Messages Sent: ${stats.messagesSent}
   Messages Received: ${stats.messagesReceived}
   ${stats.lastActive ? `Last Active: ${formatRelativeTime(stats.lastActive)}` : ""}

 {bold}Description:{/}
 ${profile.description || "(No description)"}
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
