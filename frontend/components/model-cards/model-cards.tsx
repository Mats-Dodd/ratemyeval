"use client";

import React, { useReducer } from "react";
import { ModelCard } from "./model-card";
import { ModelSelectCard } from "./model-select-card";

export const ModelCards: React.FC = () => {

    const [ isBrowseCardOpen, toggleBrowseCardOpen ] = useReducer(prev => !prev, false);

    const [ isAddCardOpen, toggleAddCardOpen ] = useReducer(prev => !prev, false);

    return (
        <div className="flex flex-col items-center justify-center gap-6">
        <div className="flex flex-row items-center justify-center gap-4">
            <ModelCard
                    title={ "Browse Models" }
                    description={ "Browse a list of supported models to test their benchmarks" }
                    content={
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                    }
                    toggle={ toggleBrowseCardOpen }
                    isModelSelectCardOpen={ isBrowseCardOpen }
                />
                <ModelCard
                    title={"Add dataset"}
                    description={"Add your own dataset to benchmark its performance"}
                    content={
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                    }
                    toggle={ toggleAddCardOpen }
                    isModelSelectCardOpen={ isAddCardOpen }
                />
        </div>
        <div>
        { isBrowseCardOpen &&
            <>
                <ModelSelectCard
                    title={"Select Models"}
                    content={
                    [
                        {
                          id: "gpt_4",
                          label: "GPT 4",
                        },
                        {
                          id: "claude_3_sonnet",
                          label: "Claude 3 Sonnet",
                        },
                        {
                          id: "gemini_1_5_flash",
                          label: "Gemini 1 5 Flash",
                        },
                        {
                          id: "grok_beta",
                          label: "Grok Beta",
                        },
                        {
                          id: "grok_vision_beta",
                          label: "Grok Vision Beta",
                        },
                      ]
                    }
                />
            </>
        }
        </div>
        </div>
  );
}
