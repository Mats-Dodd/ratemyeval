"use client";

import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
import React from "react";

type OverallScore = {
    accuracy: number;
    model: string;
    stderr: number;
}

  interface IProps {
    overallEvals: OverallScore[] | undefined,
  }

  export const OverallStatsTable: React.FC<IProps> = (props) => {

    const {
        overallEvals,
    } = props;

    return (

    <Table>
        <TableCaption>Overall Scores</TableCaption>
        <TableHeader>
            <TableRow>
            <TableHead>Model</TableHead>
            <TableHead>Accuracy</TableHead>
            <TableHead className="text-right">Std Dev</TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            { overallEvals?.map((evals: OverallScore) => (
                <TableRow key={ evals.model }>
                    <TableCell className="font-medium">{ evals.model }</TableCell>
                    <TableCell>{ evals.accuracy }</TableCell>
                    <TableCell className="text-right">{ evals.stderr }</TableCell>
                </TableRow>
            ))}
        </TableBody>
    </Table>
    );
};
