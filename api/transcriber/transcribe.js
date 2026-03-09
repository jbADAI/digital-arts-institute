// Starts or polls an AssemblyAI transcription job.
// POST: start a new job (body: { audio_url })
// GET:  poll status (query: ?id=xxx)
export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();

  const key = process.env.ASSEMBLYAI_API_KEY;
  if (!key) return res.status(500).json({ error: "ASSEMBLYAI_API_KEY not configured" });

  try {
    if (req.method === "POST") {
      const { audio_url } = req.body;
      const response = await fetch("https://api.assemblyai.com/v2/transcript", {
        method: "POST",
        headers: { authorization: key, "content-type": "application/json" },
        body: JSON.stringify({ audio_url, speaker_labels: true, speech_models: ["universal-3-pro"] }),
      });
      const data = await response.json();
      return res.status(response.status).json(data);
    }

    if (req.method === "GET") {
      const { id } = req.query;
      if (!id) return res.status(400).json({ error: "Missing id parameter" });
      const response = await fetch(`https://api.assemblyai.com/v2/transcript/${id}`, {
        headers: { authorization: key },
      });
      const data = await response.json();
      return res.status(response.status).json(data);
    }

    return res.status(405).json({ error: "GET or POST only" });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
