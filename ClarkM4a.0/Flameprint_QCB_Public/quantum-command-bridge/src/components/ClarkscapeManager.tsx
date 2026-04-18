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
// src/components/ClarkscapeManager.tsx
import React, { useEffect, useState } from "react";
import { useClarkscapeTheme } from "../hooks/useClarkscapeTheme";

export const ClarkscapeManager: React.FC = () => {
    const theme = useClarkscapeTheme();
    const [imageIndex, setImageIndex] = useState(0);

    const imageCount: Record<string, number> = {
        daylight: 3,
        dusk: 7,
        night: 16,
        sunrise: 3
    };

    useEffect(() => {
        const interval = setInterval(() => {
            setImageIndex((prev) => (prev + 1) % imageCount[theme]);
        }, 10000); // rotate every 10 seconds

        return () => clearInterval(interval);
    }, [theme]);

    const imagePath = `/assets/clarkscapes/${theme}/${imageIndex + 1}.png`;

    return (
        <div
            className="fixed inset-0 z-[-10] bg-cover bg-center transition-all duration-1000 ease-in-out"
            style={{
                backgroundImage: `url(${imagePath})`,
            }}
        />
    );
};
