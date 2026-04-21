import { Link } from "react-router-dom";
import type { Agent } from "../types/agent";

type AgentCardProps = {
  agent: Agent;
};

export default function AgentCard({ agent }: AgentCardProps) {
  return (
    <Link
      to={`/agents/${agent.id}`}
      className="group block rounded-3xl border border-neutral-200 bg-white p-5 shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-md"
    >
      <div className="flex items-start justify-between gap-4">
            <div>
                <p className="text-xs font-medium uppercase tracking-[0.18em] text-neutral-500">
                    {agent.agent_type}
                </p>
                <h3 className="mt-2 text-xl font-semibold text-neutral-950">
                    {agent.agent_name}
                </h3>
            </div>

            <span
            className={`rounded-full px-3 py-1 text-xs font-semibold ${
                agent.is_active
                ? "bg-emerald-100 text-emerald-700"
                : "bg-neutral-200 text-neutral-600"
            }`}
            >
            {agent.is_active ? "Active" : "Inactive"}
            </span>
      </div>

      <p className="mt-4 line-clamp-3 text-sm leading-6 text-neutral-600">
        {agent.description || "No description available."}
      </p>

      <div className="mt-6 flex items-center justify-between">
            <span className="rounded-full bg-neutral-100 px-3 py-1 text-xs font-medium text-neutral-700">
            Status: {agent.status}
            </span>

            <span className="text-sm font-medium text-neutral-900 transition group-hover:translate-x-1">
            View agent --^
            </span>
      </div>
    </Link>
  );
}