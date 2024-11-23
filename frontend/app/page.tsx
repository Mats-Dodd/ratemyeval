import { Button } from "@/components/ui/button";
import React from "react";
import { ApiBridge } from "./api-bridge";

export default async function Index() {

    return (
        <>
        <main className="flex-1 flex flex-col gap-6 px-4">
            <Button className="font-medium text-xl mb-4">
                Test Benchmark
            </Button>
            <ApiBridge />
        </main>
        </>
    );
}
