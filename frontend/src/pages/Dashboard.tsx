import { useEffect, useState } from "react";
import AgentCard from "../components/AgentCard";
import Layout from "../components/Layout";
import { fetchAgents } from "../services/api";
import type { Agent } from "../types/agent";

export default function Dashboard() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadAgents = async () => {
      try {
        const data = await fetchAgents();
        setAgents(data);
      } catch {
        setError("Could not load agents.");
      } finally {
        setLoading(false);
      }
    };

    loadAgents();
  }, []);

  const activeAgents = agents.filter((agent) => agent.is_active).length;

  return (
    <Layout
      title="AI Employee Dashboard"
      subtitle="Manage your agents, inspect their configurations, and test real actions like scheduling demos."
    >
      <div className="mb-8 grid gap-4 md:grid-cols-3">
            <div className="rounded-3xl border border-neutral-200 bg-white p-5 shadow-sm">
                <p className="text-sm text-neutral-500">Total Agents</p>
                <p className="mt-2 text-3xl font-bold text-neutral-950">{agents.length}</p>
            </div>

            <div className="rounded-3xl border border-neutral-200 bg-white p-5 shadow-sm">
                <p className="text-sm text-neutral-500">Active Agents</p>
                <p className="mt-2 text-3xl font-bold text-neutral-950">{activeAgents}</p>
            </div>

            <div className="rounded-3xl border border-neutral-200 bg-white p-5 shadow-sm">
                <p className="text-sm text-neutral-500">System Status</p>
                <p className="mt-2 text-3xl font-bold text-emerald-600">Online</p>
            </div>
      </div>

      {loading && <p className="text-neutral-600">Loading agents...</p>}
      {error && <p className="text-sm font-medium text-red-600">{error}</p>}

      {!loading && !error && (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {agents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      )}
    </Layout>
  );
}