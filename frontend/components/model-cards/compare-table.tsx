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

  export const CompareTable: React.FC = () => {

    return (

    <Table>
        <TableCaption>Compare</TableCaption>
        <TableHeader>
            <TableRow>
            <TableHead>Method</TableHead>
            <TableHead>Sig@90</TableHead>
            <TableHead>Sig@95</TableHead>
            <TableHead className="text-right">Sig@99</TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            <TableRow>
            <TableCell className="font-medium">GPT 4 Test</TableCell>
            <TableCell>82%</TableCell>
            <TableCell>82%</TableCell>
            <TableCell className="text-right">5</TableCell>
            </TableRow>
        </TableBody>
    </Table>
    );
};
