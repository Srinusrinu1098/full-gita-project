"use client";

import axios from "axios";
import React, { useState, useEffect, useRef } from "react";

const ELEVENLABS_API_KEY = process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY;

const playVoice = async (text) => {
  try {
    const response = await fetch(
      "https://api.elevenlabs.io/v1/text-to-speech/vzov6y10x6nsGNFg883S",
      {
        method: "POST",
        headers: {
          "xi-api-key": ELEVENLABS_API_KEY,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
          model: "eleven_multilingual_v2",
          voice: "Rachel",
          format: "mp3",
        }),
      }
    );

    const blob = await response.blob();
    const audioUrl = URL.createObjectURL(blob);
    const audio = new Audio(audioUrl);
    audio.play();
  } catch (err) {
    console.error("ElevenLabs TTS error:", err);
  }
};

const FullHeightChat = () => {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "🌸 Welcome, dear soul. Wisdom from the Bhagavad Gita awaits you. Share your mood ✨",
    },
  ]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!prompt.trim()) return;
    setLoading(true);

    setMessages((prev) => [...prev, { sender: "user", text: prompt }]);
    setPrompt("");

    const loaderId = Date.now();
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: "", id: loaderId, isLoading: true },
    ]);

    try {
      const response = await axios.post(
        "https://full-gita-project-1.onrender.com/get_gita_wisdom",
        { text: prompt }
      );

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loaderId
            ? { ...msg, text: response.data.response, isLoading: false }
            : msg
        )
      );

      // auto-play ElevenLabs voice for bot message
      playVoice(response.data.response);
    } catch (error) {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loaderId
            ? {
                ...msg,
                text: "⚠️ Something went wrong. Please try again.",
                isLoading: false,
              }
            : msg
        )
      );
    }
    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen w-full max-w-3xl mx-auto bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100 text-gray-900 rounded-xl shadow-2xl overflow-hidden">
      {/* Header */}
      <div className="text-center py-4 bg-gradient-to-r from-purple-200 via-blue-200 to-pink-200 shadow-md">
        <h1 className="text-lg font-semibold text-gray-800">🌿 Mood Swinger</h1>
        <p className="text-sm text-gray-600 italic">
          Find calmness with the Gita ✨
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, idx) => (
          <div
            key={msg.id || idx}
            className={`flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-4 py-3 rounded-2xl max-w-xl text-sm leading-relaxed shadow-md transition-all duration-300 ${
                msg.sender === "user"
                  ? "bg-blue-500 text-white rounded-br-none"
                  : "bg-white/80 text-gray-800 rounded-bl-none backdrop-blur-sm"
              }`}
            >
              {msg.isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="animate-spin text-gray-500 text-xl">⏳</div>
                  <h1 className="text-gray-700 text-sm">
                    {" "}
                    Please wait 10-15 seconds for the voice, after getting
                    response 😌
                  </h1>
                </div>
              ) : (
                <div
                  dangerouslySetInnerHTML={{ __html: msg.text }}
                  className="prose"
                />
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="sticky bottom-0 w-full border-t border-gray-300 bg-white/70 backdrop-blur-md px-4 py-3">
        <div className="flex items-end gap-3 max-w-4xl mx-auto">
          <textarea
            className="flex-1 px-4 py-3 rounded-2xl border border-gray-300 bg-white/70 backdrop-blur-sm text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none max-h-32"
            rows={1}
            placeholder="✨ Share your mood..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            className="w-12 h-12 rounded-full flex items-center justify-center shadow-md
             bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:scale-105 transition
             disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed"
            onClick={handleSend}
            disabled={prompt.length === 0}
            type="button"
          >
            {loading ? <div className="animate-spin">⏳</div> : "➡️"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default FullHeightChat;
