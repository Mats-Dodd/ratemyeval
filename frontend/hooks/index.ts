"use client";

import { defaultQueryFn } from "@/app/api";
import { useQuery } from "@tanstack/react-query";

export const useReadBenchMark = (test_id: string) => {
    return useQuery({
        queryKey: [ 'read-benchmark', test_id ],
        queryFn: async () => defaultQueryFn(`/benchmark/${test_id}`, "GET"),
    });
};

export const useRoot = () => {
    return useQuery({
        queryKey: [ 'root' ],
        queryFn: async () => defaultQueryFn("", "GET"),
    });
};

export const useDataSetEVal = (model1: string, model2: string) => {
    return useQuery({
        queryKey: [ 'dataset-eval' ],
        queryFn: async () => defaultQueryFn(`dataset-eval?model1=${model1}&model2=${model2}`, "GET"),
    });
};
