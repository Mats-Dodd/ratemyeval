import React from "react";
import { ModelCard } from "@/components/model-cards/model-card";

export default async function Index() {

    return (
        <>
        <main className="flex-1 flex flex-col gap-6 px-4">
            {/* <Button className="font-medium text-xl mb-4">
                Test Benchmark
            </Button> */}
            <div className="flex flex-row gap-4">
                <ModelCard
                    title={ "Browse Models" }
                    description={ "Browse a list of supported models to test their benchmarks" }
                    content={
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                    }
                />
                <ModelCard
                    title={"Add a Model"}
                    description={"Add your own model to benchmark its performance against other models"}
                    content={
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                    }
                />
            </div>
        </main>
        </>
    );
}
