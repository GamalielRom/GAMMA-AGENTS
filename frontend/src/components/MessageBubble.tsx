import type { Message } from "../types/message";

type MessageBubbleProps = {
  message: Message;
};

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isAgent = message.sender_type === "agent";

  return (
    <div className={`flex ${isAgent ? "justify-start" : "justify-end"}`}>
        <div
            className={`max-w-[80%] rounded-3xl px-4 py-3 shadow-sm ${
            isAgent
                ? "border border-neutral-200 bg-white text-neutral-900"
                : "bg-neutral-950 text-white"
            }`}
        >
            <p className="mb-1 text-xs font-semibold opacity-60">
            {message.sender_name || (isAgent ? "Agent" : "User")}
            </p>
            <p className="whitespace-pre-wrap text-sm leading-6">
            {message.message_content}
            </p>
        </div>
    </div>
  );
}