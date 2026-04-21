const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchAgents() {
    const response = await fetch(`${API_BASE_URL}/agents/`);

    if(!response.ok){
        throw new Error("Failed to fetch agents");
    }
    return response.json();
}

export async function fetchAgentById(agentId:string) {
    const response = await fetch(`${API_BASE_URL}/agents/${agentId}`);
    if(!response.ok){
        throw new Error("Failed to fetch the agent");
    }
    return response.json();
}

export async function fetchAgentConfig(agentId:string) {
    const response = await fetch(`${API_BASE_URL}/agents/${agentId}/config`);
    if(!response.ok){
        throw new Error("Failed to fetch agent config");
    }
    return response.json();
}
export async function fetchAgentTools(agentId:string) {
    const response = await fetch(`${API_BASE_URL}/agents/${agentId}/tools`);
    if(!response.ok){
        throw new Error("Failed to fetch the tools")
    }
    return response.json();
}

export async function fetchConversationMessages(conversationId:string) {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`)
    if(!response.ok){
        throw new Error("Failed to fetch messages");
    }
    return response.json();
}

export async function sendChatMessage(agentId:string, payload:
    {
        conversation_id: string | null;
        company_id: string;
        lead_id: string | null;
        message_content: string;
        external_contact_name: string | null;
        external_contact_email: string | null;
        channel: string;
    }
){
    const response = await fetch(`${API_BASE_URL}/agents/${agentId}/chat`, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload),
        });

    const data = await response.json().catch(() => null);

    if(!response.ok){
        console.error("Chat API error:", data);
        throw new Error(data?.detail || "Failed to send chat message");
    }
    return data;
}

export async function fetchConversations(agentId?:string) {
    const url = agentId
        ? `${API_BASE_URL}/conversations/?agent_id=${agentId}`
        : `${API_BASE_URL}/conversations/`;

    const response = await fetch(url);

    if(!response.ok){
        throw new Error("Failed to fetch conversations");
    }
    
    return response.json();
}

export async function deleteConversation(conversationId:string) {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
        method: "DELETE",
    });

    if(!response.ok){
        throw new Error("Failed to delete the conversation");   
    }

    return response.json();
}


//export {API_BASE_URL};
