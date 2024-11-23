import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card";
import React, { ReactNode } from "react";

interface IProps {
    title: string,
    description?: string,
    content?: ReactNode,
    footer?: string,
}

export const ModelCard: React.FC<IProps> = (props) => {
    const {
        title,
        description,
        content,
        footer
    } = props;

  return (
    <>
        <Card className="w-[300px]">
            <CardHeader>
                <CardTitle>{ title }</CardTitle>
                <CardDescription>{ description }</CardDescription>
            </CardHeader>
            <CardContent className="flex justify-center items-center">
                <p>{ content }</p>
            </CardContent>
            <CardFooter>
                <p>{ footer }</p>
            </CardFooter>
        </Card>
    </>
  );
}
