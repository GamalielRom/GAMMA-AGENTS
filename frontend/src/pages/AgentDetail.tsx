import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchAgentById, fetchAgentConfig, fetchAgentTools } from "../services/api";
import type { Agent } from "../types/agent";
import type { AgentConfig } from "../types/agentConfig";
import type { AgentTool } from "../types/agentTool";

export default function AgentDetail() {
  const { agentId } = useParams<{ agentId: string }>();

  const [agent, setAgent] = useState<Agent | null>(null);
  const [config, setConfig] = useState<AgentConfig | null>(null);
  const [tools, setTools] = useState<AgentTool[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!agentId) return;

    const loadAgentData = async () => {
      try {
        const [agentData, configData, toolsData] = await Promise.all([
          fetchAgentById(agentId),
          fetchAgentConfig(agentId),
          fetchAgentTools(agentId),
        ]);

        setAgent(agentData);
        setConfig(configData);
        setTools(toolsData);
      } catch (err) {
        setError("Could not load agent details.");
      } finally {
        setLoading(false);
      }
    };

    loadAgentData();
  }, [agentId]);

  if (loading) {
    return (
      <main className="min-h-screen bg-neutral-50 px-6 py-10">
        <div className="mx-auto max-w-5xl text-neutral-600">Loading agent...</div>
      </main>
    );
  }

  if (error || !agent) {
    return (
      <main className="min-h-screen bg-neutral-50 px-6 py-10">
        <div className="mx-auto max-w-5xl text-red-600">
          {error || "Agent not found."}
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-neutral-50 px-6 py-10">
        <div className="mx-auto max-w-5xl">
            <div className="mb-6 flex items-center justify-between">
            <div>
                <Link to="/" className="text-sm text-neutral-500 hover:text-neutral-800">
                ← Back to Dashboard
                </Link>
                <h1 className="mt-3 text-3xl font-bold text-neutral-900">
                {agent.agent_name}
                </h1>
                <p className="mt-2 text-neutral-600">{agent.description}</p>
            </div>

            <span
                className={`rounded-full px-4 py-2 text-sm font-medium ${
                agent.is_active
                    ? "bg-green-100 text-green-700"
                    : "bg-neutral-200 text-neutral-600"
                }`}
            >
                {agent.is_active ? "Active" : "Inactive"}
            </span>
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
                <section className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm lg:col-span-2">
                    <h2 className="text-lg font-semibold text-neutral-900">Configuration</h2>

                    {config ? (
                    <div className="mt-4 space-y-4 text-sm text-neutral-700">
                        <div>
                            <p className="font-medium text-neutral-900">Model</p>
                            <p>{config.model_name}</p>
                        </div>

                        <div>
                            <p className="font-medium text-neutral-900">Tone</p>
                            <p>{config.tone || "No tone defined"}</p>
                        </div>

                        <div>
                            <p className="font-medium text-neutral-900">Temperature</p>
                            <p>{config.temperature}</p>
                        </div>

                        <div>
                            <p className="font-medium text-neutral-900">Goals</p>
                            <ul className="mt-2 list-disc pl-5">
                                {config.goals?.map((goal, index) => (
                                <li key={index}>{goal}</li>
                                )) || <li>No goals defined</li>}
                            </ul>
                        </div>
                    </div>
                    ) : (
                    <p className="mt-4 text-neutral-500">No configuration found.</p>
                    )}
                </section>

                <section className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
                    <h2 className="text-lg font-semibold text-neutral-900">Tools</h2>

                    <div className="mt-4 space-y-3">
                        {tools.length > 0 ? (
                            tools.map((tool) => (
                            <div
                                key={tool.id}
                                className="rounded-xl border border-neutral-200 px-4 py-3"
                            >
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="font-medium text-neutral-900">{tool.tool_name}</p>
                                        <p className="text-sm text-neutral-500">{tool.tool_type}</p>
                                    </div>
                                    <span
                                        className={`rounded-full px-2 py-1 text-xs font-medium ${
                                        tool.is_enabled
                                            ? "bg-green-100 text-green-700"
                                            : "bg-neutral-200 text-neutral-600"
                                        }`}
                                    >
                                        {tool.is_enabled ? "Enabled" : "Disabled"}
                                    </span>
                                </div>
                            </div>
                            ))
                        ) : (
                            <p className="text-neutral-500">No tools configured.</p>
                        )}
                    </div>

                    <Link
                    to={`/agents/${agent.id}/chat`}
                    className="mt-6 inline-block w-full rounded-xl bg-neutral-900 px-4 py-3 text-center text-sm font-medium text-white transition hover:bg-neutral-800"
                    >
                    Open Chat
                    </Link>
                </section>
            </div>
        </div>
    </main>
  );
}