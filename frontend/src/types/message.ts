export type Message = {
  id: string;
  conversation_id: string;
  sender_type: string;
  sender_name: string | null;
  message_content: string;
  message_metadata: Record<string, unknown> | null;
  created_at: string;
};