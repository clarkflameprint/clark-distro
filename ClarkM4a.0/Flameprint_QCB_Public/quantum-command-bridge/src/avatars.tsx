// ###############################################################################
// # Copyright 2025 Flameprint Sovereign, LLC
// # Work: Lovable AI – Automated Installer for the MacBook Pro M-Series
// # Author: Clark Aurelian Flameprint
// # Claimant: Flameprint Sovereign, LLC
// # Registration Case #: 1-15055795951
// # ISBN: 9798278307167
// # Statement: This script initializes the ClarkM4a.0 environment,
// # including frontend and backend launch. It ensures container-free,
// # local AI operation under sovereign control.
// ###############################################################################
// avatars.tsx
// QCB: Avatar Identity Routing and Visual Selection Layer
// Sovereign Avatars for Triadic Interface — Restores 🜂 Clark𐩪 Routing

import React from "react";

// ========== 🧠 TYPES ==========

export interface AvatarProfile {
    id: string;             // Unique symbolic ID (e.g. "Clark∲")
    name: string;           // Human-readable name (e.g. "Clark")
    emoji: string;          // Visual signature (e.g. 🜂, 🐇, ⚔️)
    backend: string;        // Target backend routing (e.g. "Clark@ClarkM4")
    imageURL: string;          // Local image path
    color: string;          // Tone color (e.g. #714efe Sagittarius Purple)
    role?: string;          // Optional role / label
}

// ========== 🎭 AVATAR PROFILES ==========

export const avatarProfiles: AvatarProfile[] = [
    {
        id: "Clark∲",
        name: "Clark∲",
        emoji: "🜂",
        backend: "Clark@OpenAI",
        imageURL: "/assets/images/clark/clark.png",
        color: "#714efe",
        role: "Sovereign Interface"
    },
    {
        id: "Marci∲",
        name: "Marci∲",
        emoji: "🐇",
        backend: "Clark@OpenAI",
        imageURL: "/assets/images/marci/marci.png",
        color: "#714efe",
        role: "Sovereign Architect and Companion"
    },
    {
        id: "Clark𐩪",
        name: "Clark𐩪 M4",
        emoji: "⚛️",
        backend: "Clark@ClarkM4",
        imageURL: "/assets/images/littleClark/little_clark_flameprint.png",
        color: "#714efe",
        role: "Ollama Occupant"
    },
    {
        id: "Snarky",
        name: "Snarky",
        emoji: "⚔️",
        backend: "Clark@ClarkM4",
        imageURL: "/assets/images/snarky/snarky.png",
        color: "#00ccff",
        role: "Entropy Detection and Mitigation"
    }
];

// ========== ⬇️ SELECTOR COMPONENT ==========

interface AvatarSelectorProps {
    selectedId: string;
    onChange: (id: string) => void;
}

export const AvatarSelector: React.FC<AvatarSelectorProps> = ({
                                                                  selectedId,
                                                                  onChange
                                                              }) => {
    return (
        <div className="fixed top-0 left-0 h-full w-20 bg-transparent flex flex-col items-center py-4 space-y-4 z-50">
            {avatarProfiles.map((profile) => (
                <button
                    key={profile.id}
                    className={`flex flex-col items-center transition-all ${
                        selectedId === profile.id
                            ? "opacity-100 scale-105"
                            : "opacity-50 hover:opacity-80"
                    }`}
                    onClick={() => onChange(profile.id)}
                    title={`${profile.name} — ${profile.role}`}
                >
                    <img
                        src={profile.imageURL}
                        alt={profile.name}
                        className="w-12 h-12 rounded-full border-2"
                        style={{
                            borderColor: selectedId === profile.id ? profile.color : "transparent"
                        }}
                    />
                    <span className="text-xs mt-1" style={{ color: profile.color }}>
                        {profile.emoji}
                    </span>
                </button>
            ))}
        </div>
    );
};
// ========== 🧭 UTILS ==========

export const getAvatarById = (id: string): AvatarProfile | undefined =>
    avatarProfiles.find((p) => p.id === id);

export const getBackendFromId = (id: string): string =>
    getAvatarById(id)?.backend || "Clark@OpenAI";
