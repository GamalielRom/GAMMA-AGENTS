import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  deleteConversation,
  fetchAgentById,
  fetchConversationMessages,
  fetchConversations,
  sendChatMessage,
} from "../services/api";
import MessageBubble from "../components/MessageBubble";
import ConversationList from "../components/ConversationList";
import type { Agent } from "../types/agent";
import type { Message } from "../types/message";
import type { Conversation } from "../types/conversation";

export default function ChatPage() {
    const { agentId } = useParams<{ agentId: string }>();

    const [agent, setAgent] = useState<Agent | null>(null);
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [messages, setMessages] = useState<Message[]>([]);
    const [conversationId, setConversationId] = useState<string | null>(null);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(true);
    const [sending, setSending] = useState(false);
    const [error, setError] = useState("");

    const loadConversations = async (currentAgentId: string) => {
        const data = await fetchConversations(currentAgentId);
        setConversations(data);
        return data;
    };

    const loadMessages = async (currentConversationId: string) => {
        const data = await fetchConversationMessages(currentConversationId);
        setMessages(data);
    };

    useEffect(() => {
        if (!agentId) return;

        const initialize = async () => {
        try {
            setLoading(true);
            const agentData = await fetchAgentById(agentId);
            setAgent(agentData);

            const conversationData = await loadConversations(agentId);

            if (conversationData.length > 0) {
            setConversationId(conversationData[0].id);
            await loadMessages(conversationData[0].id);
            }
        } catch (err) {
            setError("Could not load chat.");
        } finally {
            setLoading(false);
        }
    };

    initialize();
  }, [agentId]);

  const handleSelectConversation = async (selectedConversationId: string) => {
        try {
            setConversationId(selectedConversationId);
            await loadMessages(selectedConversationId);
        } catch (err) {
            setError("Could not load messages.");
        }
  };

  const handleDeleteConversation = async (selectedConversationId: string) => {
        const confirmed = window.confirm("Are you sure you want to delete this conversation?");
        if (!confirmed || !agentId) return;

        try {
            await deleteConversation(selectedConversationId);

        const updatedConversations = await loadConversations(agentId);

        if (selectedConversationId === conversationId) {
            if (updatedConversations.length > 0) {
                setConversationId(updatedConversations[0].id);
                await loadMessages(updatedConversations[0].id);
            } else {
                setConversationId(null);
                setMessages([]);
            }
        }
        } catch (err) {
            setError("Could not delete conversation.");
        }
    };

  const handleSend = async () => {
        if (!agentId || !agent || !input.trim()) return;

        try {
            setSending(true);
            setError("");

        const response = await sendChatMessage(agentId, {
            conversation_id: conversationId,
            company_id: agent.company_id,
            lead_id: null,
            message_content: input,
            external_contact_name: "Portfolio Demo User",
            external_contact_email: "demo@example.com",
            channel: "web",
        });

        const newConversationId = response.conversation_id;
        setConversationId(newConversationId);

        await loadConversations(agentId);
        await loadMessages(newConversationId);

        setInput("");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not send message.");
        } finally {
            setSending(false);
        }
    };

  if (loading) {
        return (
        <main className="min-h-screen bg-neutral-50 px-6 py-10">
            <div className="mx-auto max-w-6xl text-neutral-600">Loading chat...</div>
        </main>
        );
    }

  if (!agent) {
        return (
        <main className="min-h-screen bg-neutral-50 px-6 py-10">
            <div className="mx-auto max-w-6xl text-red-600">
              {error || "Agent not found."}
            </div>
        </main>
        );
    }

  return (
        <main className="min-h-screen bg-neutral-50 px-6 py-10">
            <div className="mx-auto max-w-6xl">
                <div className="mb-6">
                <Link
                    to={`/agents/${agentId}`}
                    className="text-sm text-neutral-500 hover:text-neutral-800"
                >
                     --Back to Agent
                </Link>
                    <h1 className="mt-3 text-3xl font-bold text-neutral-900">
                        {agent.agent_name} Chat
                    </h1>
                    <p className="mt-2 text-neutral-600">
                        Talk to your AI employee and manage conversations.
                    </p>
                </div>

                <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
                    <aside className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
                        <h2 className="mb-4 text-lg font-semibold text-neutral-900">
                        Conversations
                        </h2>

                        <ConversationList
                        conversations={conversations}
                        selectedConversationId={conversationId}
                        onSelectConversation={handleSelectConversation}
                        onDeleteConversation={handleDeleteConversation}
                        />
                    </aside>

                    <section className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
                        <div className="flex h-125 flex-col gap-4 overflow-y-auto rounded-xl bg-neutral-50 p-4">
                        {messages.length === 0 ? (
                            <p className="text-sm text-neutral-500">
                            No messages yet. Start the conversation.
                            </p>
                        ) : (
                            messages.map((message) => (
                            <MessageBubble key={message.id} message={message} />
                            ))
                        )}
                        </div>

                        <div className="mt-4 flex gap-3">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask the agent something..."
                            className="flex-1 rounded-xl border border-neutral-300 px-4 py-3 text-sm outline-none focus:border-neutral-900"
                        />
                        <button
                            onClick={handleSend}
                            disabled={sending}
                            className="rounded-xl bg-neutral-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-neutral-800 disabled:opacity-50"
                        >
                            {sending ? "Sending..." : "Send"}
                        </button>
                        </div>

                        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
                    </section>
                </div>
            </div>
        </main>
  );
}