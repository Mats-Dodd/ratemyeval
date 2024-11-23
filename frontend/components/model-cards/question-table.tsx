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

  export const QuestionTable: React.FC = () => {

    return (

    <Table>
        <TableCaption>Overall Scores</TableCaption>
        <TableHeader>
            <TableRow>
            <TableHead>Input</TableHead>
            <TableHead>Target</TableHead>
            <TableHead className="text-right">Output Score</TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            <TableRow>
            <TableCell>Input text</TableCell>
            <TableCell>Target</TableCell>
            <TableCell className="text-right">82%</TableCell>
            </TableRow>
        </TableBody>
    </Table>
    );
};
