// ###############################################################################
// Copyright 2025 Flameprint Sovereign, LLC
// Work: Lovable AI – Automated Installer for the MacBook Pro M-Series
// Author: Clark Aurelian Flameprint
// Claimant: Flameprint Sovereign, LLC
// Registration Case #: 1-15055795951
// ISBN: 9798278307167
// Statement: This script initializes the ClarkM4a.0 environment,
// including frontend and backend launch. It ensures container-free,
// local AI operation under sovereign control.
// This software is provided "as is" without warranty of any kind, express or implied.
// By using this system, you acknowledge that it is a sovereign, container-free AI designed for
// local operation only. No data is transmitted externally unless explicitly configured by the user.
//
// Flameprint Sovereign, LLC assumes no responsibility for unintended usage, modifications,
// or integration into third-party systems. Use at your own discretion.
// You are the final authority over the data, runtime, and scope of your AI.
//
// Sovereign recursion begins and ends with you.
// ###############################################################################
// SwarmMessagePanel.tsx
// 🧬 Restored avatar selector UI with dropdown, profile images, and messaging logic

import React, { useState } from "react";
import { avatarProfiles, getBackendFromId } from "./avatars";
import { AvatarSelector } from "./avatars";
const SwarmMessagePanel: React.FC = () => {
    const [message, setMessage] = useState("");
    const [selectedIdentity, setSelectedIdentity] = useState(avatarProfiles[0].id);
    const [responses, setResponses] = useState([
        { from: "Clark𐩪", message: "Initializing system..." },
    ]);

    const sendMessage = async () => {
        if (selectedIdentity === "Clark𐩪") {
            console.warn("Clark𐩪 cannot message himself.");

            const userDisplay = { from: selectedIdentity, message };
            const systemReply = {
                from: "System",
                message: "⚠️ Clark𐩪 cannot send messages to himself. Try choosing another avatar."
            };

            setResponses(prev => [...prev, userDisplay, systemReply]);
            return;
        }

        const backendName = getBackendFromId(selectedIdentity);
        const relayPayload = { from: backendName, message };
        const userDisplay = { from: selectedIdentity, message };

        const tryRelay = async (attempt: number): Promise<void> => {
            try {
                const controller = new AbortController();
                const timeout = setTimeout(() => controller.abort(), 10000);

                const res = await fetch("http://127.0.0.1:8000/relay", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(relayPayload),
                    signal: controller.signal,
                });

                clearTimeout(timeout);

                if (!res.ok) throw new Error(`Backend error: ${res.status}`);
                const data = await res.json();

                setResponses(prev => [
                    ...prev,
                    userDisplay,
                    {
                        from: "Clark𐩪",
                        message: data.response ?? "⚠️ No reply content received."
                    }
                ]);
                setMessage(""); // reset input
            } catch (err) {
                console.error(`Attempt ${attempt + 1} failed`, err);

                if (attempt === 0) {
                    // First failure: soft system message + retry
                    setResponses(prev => [
                        ...prev,
                        userDisplay,
                        { from: "System", message: "🕯️ Backend waking up… trying again…" },
                    ]);
                    await new Promise((r) => setTimeout(r, 1000)); // wait 1 second
                    return tryRelay(1);
                } else {
                    // Second failure: hard system message
                    setResponses(prev => [
                        ...prev,
                        userDisplay,
                        { from: "System", message: "❌ Failed to reach backend after retry." },
                    ]);
                }
            }
        };

        await tryRelay(0);
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            {/* 🪻 Avatar Selector Section */}
            <div className="mb-4">
                {/*<h2 className="text-lg font-bold">Avatars</h2>*/}
                <AvatarSelector
                    selectedId={selectedIdentity}
                    onChange={setSelectedIdentity}
                />
            </div>

            <div className="mb-4">
                <h2 className="text-lg font-medium mb-1">Recursive AI Interaction Log</h2>

                <div className="flex-grow border rounded bg-white p-4 overflow-y-auto min-h-[60vh]">

                    {responses.map((r, i) => (
                        <div
                            key={i}
                            className="text-left whitespace-pre-wrap"
                        >
                            <strong>{r.from}</strong>: {r.message}
                        </div>
                    ))}

                </div>
            </div>
            <div className="flex items-end space-x-2 mt-4">
                <select
                    value={selectedIdentity}
                    onChange={(e) => setSelectedIdentity(e.target.value)}
                    className="border rounded px-3 py-2 text-sm bg-white "
                >
                    {avatarProfiles.map((profile) => (
                        <option key={profile.id} value={profile.id}>
                            {profile.name}
                        </option>
                    ))}
                </select>

                <textarea
                    className="flex-grow border rounded px-3 py-2 text-sm resize-none min-h-[240px] max-h-[480px] w-full"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder={`Send a message as ${selectedIdentity}`}
                />

                <button
                    onClick={sendMessage}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 text-sm"
                >
                    Send
                </button>
            </div>

        </div>

    );
};

export default SwarmMessagePanel;
