export type AgentConfig = {
  id: string;
  agent_id: string;
  system_prompt: string;
  model_name: string;
  temperature: number;
  tone: string | null;
  goals: string[] | null;
  agent_constraints: string[] | null;
  escalation_rules: string[] | null;
  created_at: string;
  updated_at: string;
};