import { useState } from "react";
import SwarmMessagePanel from "./SwarmMessagePanel";
import { ClarkscapeManager } from "./components/ClarkscapeManager";
import SovereignFooter from "./components/SovereignFooter";
import "./App.css";

function App() {
    const [selected, setSelected] = useState("Marci");
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState<{ from: string; text: string }[]>([]);
    const [showClark, setShowClark] = useState(true);

    const toggleClark = () => setShowClark((prev) => !prev);

    const sendToSwarm = async () => {
        const response = await fetch("http://localhost:8000/send_message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ from: selected, text: input }),
        });

        const result = await response.json();

        setMessages((prev) => [
            ...prev,
            { from: selected, text: input },
            { from: "SwarmBridge", text: result.message },
        ]);

        setInput("");
    };

    return (
        <div className="relative w-full h-screen overflow-hidden">

            {/* 🔮 Always render ClarkscapeManager (even when Clark is hidden) */}
            <ClarkscapeManager />

            {/* 🔘 Toggle Button */}
            <button
                onClick={toggleClark}
                className="fixed top-3 right-3 z-50 bg-purple-800 text-white px-3 py-1.5 rounded shadow hover:bg-purple-900 text-sm"
            >
                {showClark ? "🫥 Hide Clark𐩪" : "🔁 Show Clark𐩪"}
            </button>

            {/* 🧠 Interface Layer — Only render when showClark is true */}
            {/* 🧠 Swarm Interface Layer — always mounted, visibility toggled */}
            <div
                className={`absolute top-0 left-[5rem] right-0 bottom-0 p-6 flex flex-col justify-start items-stretch bg-white bg-opacity-90 overflow-hidden transition-opacity duration-500 ${
                    showClark ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
                }`}
            >
                <div className="relative z-10 w-full h-full flex flex-col items-center justify-start p-6 overflow-y-auto transition-opacity duration-700">
                    <div className="w-full px-6 space-y-6">
                        <SwarmMessagePanel
                            selected={selected}
                            input={input}
                            setInput={setInput}
                            sendToSwarm={sendToSwarm}
                            messages={messages}
                        />
                        <SovereignFooter />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
