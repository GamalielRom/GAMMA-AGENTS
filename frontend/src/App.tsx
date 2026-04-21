import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import AgentDetail from "./pages/AgentDetail";
import ChatPage from "./pages/ChatPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/agents/:agentId" element={<AgentDetail />} />
        <Route path="/agents/:agentId/chat" element={<ChatPage/>} />
      </Routes>
    </BrowserRouter>
  );
}