---
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
description: "One-sentence summary of this post."
author: "Chris Grobauskas"
date: { { .Date | time.Format "2006-01-02" } }
tags:
  - engineering
draft: true
---

# {{ replace .File.ContentBaseName `-` ` ` | title }}

> **Key takeaway**: One sentence that captures the main point.

<!-- more -->

## Background

Why this topic matters — context for the reader.

## Main Idea

The core argument or insight.

## Example

A concrete story, case, or analogy that demonstrates the idea.

## Summary

Restate the key insight and connect it back to the bigger picture.
