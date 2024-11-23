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

  export const OverallStatsTable: React.FC = () => {

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
            <TableRow>
            <TableCell className="font-medium">GPT 4 Test</TableCell>
            <TableCell>82%</TableCell>
            <TableCell className="text-right">5</TableCell>
            </TableRow>
        </TableBody>
    </Table>
    );
};
