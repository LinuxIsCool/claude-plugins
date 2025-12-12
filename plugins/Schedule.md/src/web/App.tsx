/**
 * Schedule.md - Main React Application
 */

import React, { useState, useEffect, useCallback } from "react";
import type { ScheduleBlock, ScheduleConfig, ScheduleSummary } from "../types";
import { Header } from "./components/Header";
import { WeekView } from "./components/WeekView";
import { BlockModal } from "./components/BlockModal";
import { api, ws } from "./lib/api";

export function App() {
  const [config, setConfig] = useState<ScheduleConfig | null>(null);
  const [blocks, setBlocks] = useState<ScheduleBlock[]>([]);
  const [summary, setSummary] = useState<ScheduleSummary | null>(null);
  const [selectedBlock, setSelectedBlock] = useState<ScheduleBlock | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load initial data
  const loadData = useCallback(async () => {
    try {
      setError(null);
      const [configData, blocksData, summaryData] = await Promise.all([
        api.getConfig(),
        api.listBlocks(),
        api.getSummary(),
      ]);
      setConfig(configData);
      setBlocks(blocksData);
      setSummary(summaryData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load schedule");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();

    // Connect WebSocket for real-time updates
    ws.connect();

    const unsubBlocks = ws.on("blocks-updated", () => {
      loadData();
    });

    const unsubConfig = ws.on("config-updated", () => {
      loadData();
    });

    return () => {
      unsubBlocks();
      unsubConfig();
      ws.disconnect();
    };
  }, [loadData]);

  // Handle block click
  const handleBlockClick = useCallback((block: ScheduleBlock) => {
    setSelectedBlock(block);
  }, []);

  // Close modal
  const handleCloseModal = useCallback(() => {
    setSelectedBlock(null);
  }, []);

  // Loading state
  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          fontSize: "16px",
          color: "#6b7280",
        }}
      >
        Loading schedule...
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          gap: "16px",
        }}
      >
        <div style={{ fontSize: "16px", color: "#dc2626" }}>{error}</div>
        <button
          onClick={loadData}
          style={{
            padding: "8px 16px",
            backgroundColor: "#3b82f6",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        backgroundColor: "#f9fafb",
      }}
    >
      <Header config={config} summary={summary} />

      <main style={{ flex: 1, overflow: "hidden", padding: "16px" }}>
        <div
          style={{
            height: "100%",
            backgroundColor: "#fff",
            borderRadius: "8px",
            boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
            overflow: "hidden",
          }}
        >
          {config && (
            <WeekView
              blocks={blocks}
              config={config}
              onBlockClick={handleBlockClick}
            />
          )}
        </div>
      </main>

      {/* Block details modal */}
      {selectedBlock && config && (
        <BlockModal
          block={selectedBlock}
          config={config}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
}
