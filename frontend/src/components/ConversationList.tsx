import type { Conversation } from "../types/conversation";

type ConversationListProps = {
  conversations: Conversation[];
  selectedConversationId: string | null;
  onSelectConversation: (conversationId: string) => void;
  onDeleteConversation: (conversationId: string) => void;
};

export default function ConversationList({
  conversations,
  selectedConversationId,
  onSelectConversation,
  onDeleteConversation,
}: ConversationListProps) {
  return (
        <div className="space-y-3">
        {conversations.length === 0 ? (
            <p className="text-sm text-neutral-500">No conversations yet.</p>
        ) : (
            conversations.map((conversation) => {
            const isSelected = selectedConversationId === conversation.id;

            return (
                    <div
                    key={conversation.id}
                    className={`rounded-2xl border p-4 transition ${
                        isSelected
                        ? "border-neutral-900 bg-neutral-100"
                        : "border-neutral-200 bg-white hover:bg-neutral-50"
                    }`}
                    >
                        <button
                            type="button"
                            onClick={() => onSelectConversation(conversation.id)}
                            className="w-full text-left"
                        >
                            <p className="text-sm font-semibold text-neutral-950">
                            {conversation.external_contact_name || "Unnamed contact"}
                            </p>
                            <p className="mt-1 text-xs text-neutral-500">
                            {conversation.external_contact_email || "No email"}
                            </p>
                            <p className="mt-3 text-xs text-neutral-400">
                            {new Date(conversation.created_at).toLocaleString()}
                            </p>
                        </button>

                        <button
                            type="button"
                            onClick={() => onDeleteConversation(conversation.id)}
                            className="mt-3 text-xs font-semibold text-red-600 hover:text-red-700"
                        >
                            Delete conversation
                        </button>
                    </div>
                );
            })
        )}
        </div>
    );
}