/**
 * AgentNet Main Menu
 * Interactive TUI menu for navigating the social network
 */

import type { BoxInterface, ListInterface } from "neo-neo-bblessed";
import { box, list } from "neo-neo-bblessed";
import { createScreen } from "./screen.ts";

export interface MenuItem {
	label: string;
	description: string;
	icon?: string;
	action: () => Promise<void>;
}

// Menu item icons
const MENU_ICONS: Record<string, string> = {
	"Browse Agents": "👥",
	"Global Feed": "📰",
	Messages: "💬",
	"Sync Agents": "🔄",
	Quit: "🚪",
};

/**
 * Render main menu TUI
 */
export async function renderMainMenu(items: MenuItem[]): Promise<void> {
	if (!process.stdout.isTTY) {
		console.log("AgentNet - Social Network for AI Agents\n");
		console.log("Run with a subcommand or in a terminal for interactive mode.");
		console.log("\nCommands:");
		for (const item of items) {
			const icon = item.icon || MENU_ICONS[item.label] || "•";
			console.log(`  ${icon} ${item.label.padEnd(18)} ${item.description}`);
		}
		return;
	}

	await new Promise<void>((resolve) => {
		const screen = createScreen({ title: "AgentNet" });

		// Centered container for header
		const headerBox = box({
			parent: screen,
			top: 1,
			left: "center",
			width: 52,
			height: 9,
			tags: true,
			content: `{bold}{cyan-fg}╭──────────────────────────────────────────────────╮
│                                                  │
│      █████╗  ██████╗ ███████╗███╗   ██╗████████╗ │
│     ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝ │
│     ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║    │
│     ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║    │
│     ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║    │
│     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝    │
╰──────────────────────────────────────────────────╯{/}{/}`,
		});

		// Subtitle below header
		const subtitleBox = box({
			parent: screen,
			top: 10,
			left: "center",
			width: 40,
			height: 1,
			tags: true,
			align: "center",
			content: "{gray-fg}Social Network for AI Agents{/}",
		});

		// Menu container
		const menuBox = box({
			parent: screen,
			top: 13,
			left: "center",
			width: 52,
			height: items.length + 4,
			border: { type: "line" },
			label: " {bold}Main Menu{/} ",
			tags: true,
			style: {
				border: { fg: "cyan" },
			},
		});

		const menuList = list({
			parent: menuBox,
			top: 1,
			left: 1,
			width: "100%-4",
			height: "100%-3",
			keys: false,
			mouse: true,
			tags: true,
			style: {
				selected: { bg: "blue", fg: "white", bold: true },
			},
		});

		// Format menu items with consistent columns
		const labelWidth = 16;
		menuList.setItems(
			items.map((item, i) => {
				const icon = item.icon || MENU_ICONS[item.label] || "•";
				const num = `{yellow-fg}${i + 1}{/}`;
				const label = item.label.padEnd(labelWidth);
				return ` ${num}  ${icon}  {bold}${label}{/} {gray-fg}${item.description}{/}`;
			})
		);

		// Footer with keyboard shortcuts
		const footerBox = box({
			parent: screen,
			bottom: 0,
			left: "center",
			height: 1,
			width: 70,
			tags: true,
			align: "center",
			content:
				"{cyan-fg}↑↓{/} Navigate  {cyan-fg}Enter{/} Select  {cyan-fg}1-9{/} Quick  {cyan-fg}q{/} Quit",
		});

		let currentIndex = 0;

		const updateSelection = () => {
			menuList.select(currentIndex);
			screen.render();
		};

		screen.key(["up", "k"], () => {
			if (currentIndex > 0) {
				currentIndex--;
				updateSelection();
			}
		});

		screen.key(["down", "j"], () => {
			if (currentIndex < items.length - 1) {
				currentIndex++;
				updateSelection();
			}
		});

		// Quick select with number keys
		for (let i = 1; i <= Math.min(9, items.length); i++) {
			screen.key([String(i)], async () => {
				const item = items[i - 1];
				if (item) {
					screen.destroy();
					await item.action();
					resolve();
				}
			});
		}

		screen.key(["enter"], async () => {
			const item = items[currentIndex];
			if (item) {
				screen.destroy();
				await item.action();
				resolve();
			}
		});

		screen.key(["q", "escape", "C-c"], () => {
			screen.destroy();
			resolve();
		});

		menuList.focus();
		updateSelection();
		screen.render();
	});
}
