import { useState, useEffect, useCallback, useRef } from "react";

export function useTimer(initialTime = 30, onTimeUp) {
    const [timeLeft, setTimeLeft] = useState(initialTime);
    const [isActive, setIsActive] = useState(false);
    const [isFinished, setIsFinished] = useState(false);

    const callbackRef = useRef(onTimeUp);

    useEffect(() => {
        callbackRef.current = onTimeUp;
    }, [onTimeUp]);

    const start = useCallback(() => {
        setIsActive(true);
        setTimeLeft(initialTime);
        setIsFinished(false);
    }, [initialTime]);

    const stop = useCallback(() => {
        setIsActive(false);
        setIsFinished(true);
    }, []);

    const pause = useCallback(() => {
        setIsActive(false);
    }, []);

    const reset = useCallback(() => {
        setIsActive(false);
        setTimeLeft(initialTime);
        setIsFinished(false);
    }, [initialTime]);

    useEffect(() => {
        if (!isActive) return;

        const interval = setInterval(() => {
            setTimeLeft((t) => {
                if (t <= 1) {
                    clearInterval(interval);

                    setIsActive(false);
                    setIsFinished(true);

                    if (callbackRef.current) {
                        callbackRef.current();
                    }

                    return 0;
                }

                return t - 1;
            });
        }, 1000);

        return () => clearInterval(interval);
    }, [isActive]);

    return {
        timeLeft,
        isActive,
        isFinished,
        start,
        stop,
        pause,
        reset,
    };
}