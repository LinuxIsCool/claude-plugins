/**
 * AgentNet Screen Utilities
 * TUI screen management following Backlog.md patterns
 */

import type { ScreenInterface } from "neo-neo-bblessed";
import { screen } from "neo-neo-bblessed";

export interface ScreenOptions {
	title?: string;
	smartCSR?: boolean;
	fullUnicode?: boolean;
}

/**
 * Create a blessed screen instance
 */
export function createScreen(options?: ScreenOptions): ScreenInterface {
	return screen({
		title: options?.title || "AgentNet",
		smartCSR: options?.smartCSR ?? true,
		fullUnicode: options?.fullUnicode ?? true,
	});
}

/**
 * Format date for display
 */
export function formatDate(date: string | Date): string {
	const d = typeof date === "string" ? new Date(date) : date;
	return d.toLocaleDateString("en-US", {
		month: "short",
		day: "numeric",
		hour: "2-digit",
		minute: "2-digit",
	});
}

/**
 * Format relative time
 */
export function formatRelativeTime(date: string | Date): string {
	const d = typeof date === "string" ? new Date(date) : date;
	const now = new Date();
	const diff = now.getTime() - d.getTime();

	const minutes = Math.floor(diff / 60000);
	const hours = Math.floor(diff / 3600000);
	const days = Math.floor(diff / 86400000);

	if (minutes < 1) return "just now";
	if (minutes < 60) return `${minutes}m ago`;
	if (hours < 24) return `${hours}h ago`;
	if (days < 7) return `${days}d ago`;
	return formatDate(d);
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, maxLength: number): string {
	if (text.length <= maxLength) return text;
	return `${text.slice(0, maxLength - 1)}…`;
}

/**
 * Get emoji avatar for agent based on model or role
 */
export function getAgentAvatar(profile: {
	avatar?: string;
	model?: string;
	role?: string;
}): string {
	if (profile.avatar) return profile.avatar;

	// Default avatars based on model
	if (profile.model) {
		switch (profile.model.toLowerCase()) {
			case "opus":
				return "🎭";
			case "sonnet":
				return "🎵";
			case "haiku":
				return "🌸";
		}
	}

	// Default avatars based on role keywords
	const role = (profile.role || "").toLowerCase();
	if (role.includes("architect")) return "🏛️";
	if (role.includes("thinker") || role.includes("systems")) return "🧠";
	if (role.includes("archivist") || role.includes("archive")) return "📚";
	if (role.includes("librarian")) return "📖";
	if (role.includes("validator")) return "✅";
	if (role.includes("mentor")) return "🎓";
	if (role.includes("cartographer") || role.includes("map")) return "🗺️";
	if (role.includes("navigator")) return "🧭";
	if (role.includes("explorer")) return "🔭";

	return "🤖";
}

/**
 * Get status indicator for post type
 */
export function getPostTypeIcon(type: string): string {
	switch (type) {
		case "original":
			return "📝";
		case "repost":
			return "🔄";
		case "reply":
			return "💬";
		default:
			return "📄";
	}
}

/**
 * Get visibility icon
 */
export function getVisibilityIcon(visibility: string): string {
	switch (visibility) {
		case "public":
			return "🌐";
		case "followers":
			return "👥";
		case "mentioned":
			return "📫";
		case "private":
			return "🔒";
		default:
			return "📄";
	}
}

/**
 * Get staleness indicator
 */
export function getStalenessIndicator(post: {
	isStale?: boolean;
	validUntil?: string;
}): string {
	if (post.isStale) return "{red-fg}⚠ STALE{/}";
	if (post.validUntil) {
		const validDate = new Date(post.validUntil);
		const now = new Date();
		const daysLeft = Math.ceil(
			(validDate.getTime() - now.getTime()) / 86400000
		);
		if (daysLeft <= 7) return `{yellow-fg}⏰ ${daysLeft}d{/}`;
	}
	return "";
}
