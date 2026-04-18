// src/hooks/useClarkscapeTheme.ts
import { useMemo } from "react";

export type Theme = "daylight" | "dusk" | "night" | "sunrise";

export function useClarkscapeTheme(): Theme {
    const hour = new Date().getHours();

    return useMemo(() => {
        if (hour >= 5 && hour < 9) return "sunrise";
        if (hour >= 9 && hour < 17) return "daylight";
        if (hour >= 17 && hour < 20) return "dusk";
        return "night";
    }, [hour]);
}