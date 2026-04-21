export type Conversation = {
  id: string;
  company_id: string;
  agent_id: string;
  lead_id: string | null;
  channel: string;
  external_contact_name: string | null;
  external_contact_email: string | null;
  status: string;
  created_at: string;
  ended_at: string | null;
};