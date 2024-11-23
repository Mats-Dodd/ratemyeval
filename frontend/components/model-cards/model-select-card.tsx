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
    customClasses: string,
    align: "start" | "end",
    submit: boolean,
}

export const ModelSelectCard: React.FC<IProps> = (props) => {
    const {
        title,
        description,
        content,
        footer,
        customClasses,
        align,
        submit,
    } = props;

  return (
    <>
        <Card className={`w-[470px] h-[320px] ${customClasses}`}>
            <CardHeader>
                <CardTitle className={`flex flex-${align}`}>{ title }</CardTitle>
                <CardDescription>{ description }</CardDescription>
            </CardHeader>
            <CardContent className="flex justify-start items-center">
                {/* <p>{ content }</p> */}
                { content !== undefined &&
                    <CheckboxReactHookFormMultiple
                        items={ content }
                        submit={ submit }
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
