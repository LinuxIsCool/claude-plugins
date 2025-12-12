/**
 * TimeBlock component - displays a single schedule block in the grid
 */

import React from "react";
import type { ScheduleBlock, ScheduleConfig } from "../../types";
import { timeToMinutes, formatTimeDisplay, getDurationMinutes, formatDuration } from "../../utils/time";

interface TimeBlockProps {
  block: ScheduleBlock;
  config: ScheduleConfig;
  dayStartHour: number;
  hourHeight: number;
  onClick?: (block: ScheduleBlock) => void;
}

export function TimeBlock({
  block,
  config,
  dayStartHour,
  hourHeight,
  onClick,
}: TimeBlockProps) {
  // Calculate position and height
  const startMinutes = timeToMinutes(block.startTime);
  const endMinutes = timeToMinutes(block.endTime);
  const dayStartMinutes = dayStartHour * 60;

  const top = ((startMinutes - dayStartMinutes) / 60) * hourHeight;
  const height = ((endMinutes - startMinutes) / 60) * hourHeight;

  // Get color from category or block override
  const category = config.categories[block.category];
  const color = block.color || category?.color || "#6b7280";

  // Duration for tooltip
  const duration = getDurationMinutes(block.startTime, block.endTime);

  return (
    <div
      className="time-block"
      style={{
        position: "absolute",
        top: `${top}px`,
        left: "4px",
        right: "4px",
        height: `${Math.max(height - 2, 20)}px`,
        backgroundColor: color,
        borderRadius: "4px",
        padding: "4px 6px",
        cursor: "pointer",
        overflow: "hidden",
        fontSize: "12px",
        color: "#fff",
        boxShadow: "0 1px 3px rgba(0,0,0,0.2)",
        transition: "transform 0.1s, box-shadow 0.1s",
      }}
      onClick={() => onClick?.(block)}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "scale(1.02)";
        e.currentTarget.style.boxShadow = "0 4px 8px rgba(0,0,0,0.3)";
        e.currentTarget.style.zIndex = "10";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "scale(1)";
        e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.2)";
        e.currentTarget.style.zIndex = "1";
      }}
      title={`${block.title}\n${formatTimeDisplay(block.startTime)} - ${formatTimeDisplay(block.endTime)}\n${formatDuration(duration)}${block.location ? `\n${block.location}` : ""}`}
    >
      <div
        style={{
          fontWeight: 600,
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}
      >
        {block.title}
      </div>
      {height > 40 && (
        <div
          style={{
            fontSize: "10px",
            opacity: 0.9,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {formatTimeDisplay(block.startTime)} - {formatTimeDisplay(block.endTime)}
        </div>
      )}
      {height > 60 && block.location && (
        <div
          style={{
            fontSize: "10px",
            opacity: 0.8,
            marginTop: "2px",
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {block.location}
        </div>
      )}
    </div>
  );
}
