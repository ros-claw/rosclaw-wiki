---
id: format37_youtube_mcp
type: concept
title: format37/youtube_mcp
tags:
- youtube
- transcription
- whisper
- mcp-server
- audio-processing
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/format37/youtube_mcp
section: Server Implementations > 🔎 <a name="search"></a>Search & Data Extraction
---

> 🐍 ☁️ – MCP server that transcribes YouTube videos to text. Uses yt-dlp to download audio and OpenAI's Whisper-1 for more precise transcription than youtube captions. Provide a YouTube URL and get back the full transcript splitted by chunks for long videos.

This MCP server transcribes YouTube videos into text by downloading the audio with yt-dlp and using OpenAI's Whisper-1 model for accurate speech recognition. It provides full transcripts split into chunks for long videos, offering higher precision than YouTube's built-in captions. The tool is implemented in Python and integrates with the Model Context Protocol, making it useful for AI agents that need to process video content.

**Category:** Server Implementations > 🔎 <a name="search"></a>Search & Data Extraction
**Source:** [https://github.com/format37/youtube_mcp](https://github.com/format37/youtube_mcp)
