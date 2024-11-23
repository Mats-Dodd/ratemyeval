"use client";

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import React from "react";

export function InputFile() {
  return (
    <span className="grid w-full max-w-sm items-center gap-4">
      <Label htmlFor="picture"></Label>
      <Input id="picture" type="file" />
    </span>
  )
}
