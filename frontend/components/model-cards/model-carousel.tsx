"use client";

import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
  } from "@/components/ui/carousel"
import React from "react";
import { ModelSelectCard } from "./model-select-card";


export const ModelCarousel: React.FC = () => {
    return (
        <Carousel className="w-[500px]">
            <CarouselContent>
                <CarouselItem>
                    <ModelSelectCard title={ "Model 1" } />
                </CarouselItem>
                <CarouselItem>
                    <ModelSelectCard title={ "Model 2" } />
                </CarouselItem>
                <CarouselItem>
                    <ModelSelectCard title={ "Model 3" } />
                </CarouselItem>
            </CarouselContent>
            <CarouselPrevious />
        <CarouselNext />
        </Carousel>
    );
};
