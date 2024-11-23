"use client";

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card";
import React from "react";
import { CheckboxReactHookFormMultiple } from "./model-checkbox-form";

type SelectModel= {
    id: string,
    label: string,
}

interface IProps {
    title: string,
    description?: string,
    content?: SelectModel[],
    footer?: string,
}

export const ModelSelectCard: React.FC<IProps> = (props) => {
    const {
        title,
        description,
        content,
        footer
    } = props;

  return (
    <>
        <Card className="w-[950px] h-[320px]">
            <CardHeader>
                <CardTitle>{ title }</CardTitle>
                <CardDescription>{ description }</CardDescription>
            </CardHeader>
            <CardContent className="flex justify-start items-center">
                {/* <p>{ content }</p> */}
                { content !== undefined &&
                    <CheckboxReactHookFormMultiple
                        items={ content }
                    />
                }
            </CardContent>
            <CardFooter>
                <p>{ footer }</p>
            </CardFooter>
        </Card>
    </>
  );
}
