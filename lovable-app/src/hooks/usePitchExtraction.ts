import { useState } from "react";

interface PitchContour {
  times: number[];
  frequencies: number[];
  confidence: number[];
}

interface NoteEvent {
  start_time: number;
  end_time: number;
  pitch_midi: number;
  velocity: number;
}

interface PitchExtractionResult {
  success: boolean;
  metadata: {
    sample_rate: number;
    duration_seconds: number;
    filename: string;
  };
  pitch_contour: PitchContour;
  note_events: NoteEvent[];
  midi_data?: number[];
}

export function usePitchExtraction() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PitchExtractionResult | null>(null);

  const extractPitch = async (audioFile: File): Promise<PitchExtractionResult | null> => {
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("audio", audioFile);

      // Call the Supabase edge function
      const response = await fetch(
        `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/extract-pitch`,
        {
          method: "POST",
          body: formData,
          headers: {
            Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to extract pitch");
      }

      const data: PitchExtractionResult = await response.json();
      setResult(data);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Unknown error occurred";
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return {
    extractPitch,
    loading,
    error,
    result,
  };
}

