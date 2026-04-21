export type AgentTool = {
  id: string;
  agent_id: string;
  tool_name: string;
  tool_type: string;
  config: Record<string, unknown> | null;
  is_enabled: boolean;
  created_at: string;
  updated_at: string;
};