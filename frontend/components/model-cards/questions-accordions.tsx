"use client";

import React from "react";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
  } from "@/components/ui/accordion"
import { QuestionTable } from "./question-table";

export const QuestionsAccordions: React.FC = () => {

    return (
        <>
        <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
                <AccordionTrigger>Question 1?</AccordionTrigger>
                <AccordionContent>
                    <QuestionTable />
                </AccordionContent>
            </AccordionItem>
        </Accordion>
                <Accordion type="single" collapsible>
                <AccordionItem value="item-1">
                    <AccordionTrigger>Question 2?</AccordionTrigger>
                    <AccordionContent>
                        <QuestionTable />
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
        <Accordion type="single" collapsible>
        <AccordionItem value="item-1">
            <AccordionTrigger>Question 3?</AccordionTrigger>
            <AccordionContent>
                <QuestionTable />
            </AccordionContent>
        </AccordionItem>
    </Accordion>
        <Accordion type="single" collapsible>
        <AccordionItem value="item-1">
            <AccordionTrigger>Question 4?</AccordionTrigger>
            <AccordionContent>
                <QuestionTable />
            </AccordionContent>
        </AccordionItem>
    </Accordion>
    </>
    );
};
