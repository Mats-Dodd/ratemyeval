"use client";

import React from "react";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
  } from "@/components/ui/accordion"
import { QuestionTable } from "./question-table";
import { useDataSetEVal } from "@/hooks";

interface IProps {
    selectedModels: string[];
}

export const QuestionsAccordions: React.FC<IProps> = (props) => {

    const {
        selectedModels,
    } = props;

    console.log("Selected models",selectedModels);
    const { data: questions, isLoading: loadingQuestions } = useDataSetEVal(selectedModels[0], selectedModels[1]);
    console.log("questions:",questions);

    if (loadingQuestions) {
        return (<>Loading...</>);
    }

    return (
        <>
        Questions
        { questions.map((question, index: number) => (
            <Accordion key={ index } type="single" collapsible>
            <AccordionItem value={ question.input }>
                <AccordionTrigger>{ question.input }</AccordionTrigger>
                <AccordionContent>
                    <QuestionTable />
                </AccordionContent>
            </AccordionItem>
        </Accordion>
        ))}
    </>
    );
};
