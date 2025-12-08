import { GoogleGenAI } from "@google/genai";

let genAI: GoogleGenAI | null = null;

if (process.env.API_KEY) {
  genAI = new GoogleGenAI({ apiKey: process.env.API_KEY });
}

export const generateGameOverMessage = async (distance: number): Promise<string> => {
  if (!genAI) {
    return `You swam ${distance.toFixed(1)} meters! Did you know? Orcas are actually the largest member of the dolphin family.`;
  }

  try {
    const model = "gemini-2.5-flash";
    const prompt = `
      The player played a game as a Little Orca and swam ${distance.toFixed(1)} meters before hitting too much ocean trash.
      Generate a short, single-sentence, encouraging message. It can be a fun fact about Orcas or a gentle reminder about ocean conservation.
      Tone: Whimsical, educational, or encouraging.
      Max length: 25 words.
    `;

    const response = await genAI.models.generateContent({
      model: model,
      contents: prompt,
    });

    return response.text || "Keep swimming and keep our oceans clean!";
  } catch (error) {
    console.error("Error generating Gemini content:", error);
    return `You swam ${distance.toFixed(1)} meters! Keep the oceans clean!`;
  }
};